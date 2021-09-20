import json
import textwrap
from abc import ABC, abstractproperty
from collections import namedtuple
from statistics import mean
from typing import Any, Generator, Iterator, List
import logging

import bt2
from profiler.lookup import Lookup

from profiler.utils import print_execution_time

from profiler.analyses import Analysis
from profiler.event import TraceEvent, RegionProfile, DefineRegion

logger = logging.getLogger(__name__)
_format = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=_format)




Node = namedtuple("Node", ["petId", "id", "parentId"])
TreeNode = namedtuple("TreeNode", "node children")


class RegionProfiles:
    def __init__(self, profiles: Iterator[RegionProfile], lookup: Lookup):
        self._profiles = profiles
        self._lookup = lookup

    def __iter__(self):
        yield from self.profiles

    def __str__(self):
        return self.toJson()

    def toJson(self):
        return json.dumps(self, cls=RegionProfilesEncoder)

    def profiles(self):
        return list(self._profiles)

    def petIds(self):
        return list(set(map(lambda x: x.get("pet"), self.profiles)))

    def parentIds(self):
        return list(set(self._filter_unique_values("parentId", [])))

    @print_execution_time
    def _create_tree(self, level: int = 1):
        logger.debug(f"generating tree with level: {level}")
        profiles = list(
            set(
                [
                    Node(
                        int(profile.get("pet")),
                        int(profile.get("id")),
                        int(profile.get("parentId")),
                    )
                    for profile in self.profiles
                ]
            )
        )

        output = []
        for petId in self.petIds:
            _profiles = list(filter(lambda x: x.petId == petId, profiles))
            output.append(self._populate_tree_from_map(self._build_tree_map(_profiles)))
        return output

    def _create_tree_json(self):
        return json.dumps(
            self._create_tree(),
            cls=TraceEventEncoder,
        )

    def _populate_tree_from_map(self, tree_map: List[Node]):
        return self._fetch_objs(tree_map)

    def _build_tree_map(self, profiles: List[Node]):
        return self._build_tree_from_root(profiles)

    def _fetch_objs(self, tree):
        for leaf in tree:
            leaf["node"] = list(
                filter(lambda x: x.get("id") == leaf["node"].id, self.profiles)
            )[0]
            if len(leaf["children"]):
                self._fetch_objs(leaf["children"])
        return tree

    def _build_tree_from_root(self, nodes: List[Node], root: Node = None):

        nodes = list(filter(lambda x: x.petId == 0, nodes))
        root = (
            list(filter(lambda x: x.parentId == 0, nodes))[0] if root is None else root
        )
        out = []
        for node in nodes:
            if node.parentId == root.id:
                children = self._build_tree_from_root(nodes, node)
                out.append({"node": node, "children": children})
        return out

    @staticmethod
    def _flatten(t):
        return [item for sublist in t for item in sublist]

    @print_execution_time
    def _filter_unique_values(self, key: str, skip_values: List[Any] = []):
        return set(
            [
                profile.get(key)
                for profile in self.profiles
                if profile.get(key) not in skip_values
            ]
        )


class RegionSummary:
    def __init__(self, region_profiles: List["TraceEvent"]):
        self._profiles = region_profiles
        self._children = {}
        self._pet_count = len(region_profiles)

    @property
    def profiles(self):
        return list(self._profiles)

    def _totals(self):
        # TODO Cache this
        return [profile.get("total") for profile in self.profiles]

    def _count(self):
        # TODO Cache this
        return [profile.get("count") for profile in self.profiles]

    def _pet_ids(self):
        # TODO Cache this
        return [profile.get("pet") for profile in self.profiles]

    def pet_count(self):
        return len(self.profiles)

    def count_each(self):
        return max(self._count())

    def min(self):
        return min(self._totals())

    def max(self):
        return max(self._totals())

    def mean(self):
        return mean(self._totals())

    def min_pet_id(self):
        # QUESTION can't there be multiple id's that share the same value?
        return dict(zip(self._totals(), self._pet_ids()))[self.min()]

    def max_pet_id(self):
        return dict(zip(self._totals(), self._pet_ids()))[self.max()]


class Trace:
    def __init__(self, msgs: Generator[TraceEvent, None, None]):
        self._msgs = msgs

    def __iter__(self):
        yield from self._msgs

    def filter(self, fx):
        yield from filter(fx, self._msgs)

    @staticmethod
    # TODO handle errors
    # TODO gathering and mapping regions names with define_region should be cached (functools lib)
    def from_path_old(
        _path: str, include: List[str], exclude: List[str], lookup: Lookup = None
    ):
        # TODO good cache option
        requiredInclude = ["define_region"]  # any events we need for every run
        logger.debug(
            f"fetching traces from path: {_path} include=[{include}] exclude=[{exclude}]"
        )
        hasInclude = len(include)
        hasExclude = len(exclude)
        include = include + requiredInclude  # Yuck, refactor, see TODO's
        results = []
        for msg in bt2.TraceCollectionMessageIterator(_path):
            if type(msg) is bt2._EventMessageConst:

                event = msg.event.name
                if (
                    (hasInclude and event in include)
                    or (hasExclude and event not in exclude)
                    or (not hasInclude and hasExclude)
                ):
                    results.append(TraceEvent.Of(msg))
        return results

    @staticmethod
    def from_path(_path: str, analyses: List[Analysis]):
        logger.debug(f"fetching traces from path: {_path}")

        # hard code for now - eventually query each Analysis
        # for what events need to be included
        includes = ["define_region", "region_profile"]
        tmp_count = 0

        for msg in bt2.TraceCollectionMessageIterator(_path):
            if type(msg) is bt2._EventMessageConst:

                tmp_count += 1
                if tmp_count % 10000 == 0:
                    logger.debug(f"Processed {tmp_count} events")

                eventName = msg.event.name
                if (eventName in includes):
                    event = TraceEvent.Of(msg)
                    # allow each analysis to process the event
                    # however it needs to
                    for analysis in analyses:
                        analysis.process_event(event)



        logger.debug(f"exiting from_path")
