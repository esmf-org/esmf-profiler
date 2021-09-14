import functools

import json
import textwrap
from abc import ABC, abstractmethod, abstractproperty
from collections import defaultdict, namedtuple
from statistics import mean
from typing import Any, Dict, Generator, Iterator, List
import logging

import bt2
from profiler.lookup import Lookup

from profiler.utils import print_execution_time

logger = logging.getLogger(__name__)
_format = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=_format)


class TraceEvent(ABC):
    def __init__(self, msg: bt2._EventMessageConst):
        self._msg = msg
        self._attributes = {}

    def __repr__(self):
        return f"<{self.__class__.__name__} {textwrap.shorten(str(self.payload), width=50)}>"

    def __str__(self):
        return self.toJSON()

    def toJSON(self):
        return json.dumps(self, cls=TraceEventEncoder)

    @abstractproperty
    def type(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} requires a 'type' property"
        )

    @property
    def keys(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} requires a 'keys' property"
        )

    @property
    def name(self):
        if "name" in self._attributes:
            return self._attributes["name"]
        return ""

    def get(self, key):
        try:
            if str(key).lower() in self.keys:
                return self.payload[str(key).lower()]
        except KeyError:
            if key in dir(self):
                return getattr(self, key)

        raise AttributeError(f"Key '{key}' does not exist on {self.__class__.__name__}")

    @functools.cached_property
    def payload(self):
        return self._msg.event.payload_field

    @functools.cached_property
    def pet(self):
        return self._msg.event.packet.context_field["pet"]

    @functools.cached_property
    def nodename(self):
        return self._msg.event.packet.context_field["nodename"]

    @staticmethod
    def Of(msg: bt2._EventMessageConst):
        """Of Convnience constructor

        Args:
            msg (bt2._EventMessageConst):

        Returns:
            Obj:
        """
        event_type = msg.event.name
        __map = {
            "define_region": lambda msg: DefineRegion(msg),
            "regionid_enter": lambda msg: RegionIdEnter(msg),
            "regionid_exit": lambda msg: RegionIdExit(msg),
            "region_profile": lambda msg: RegionProfile(msg),
            "comp": lambda msg: Comp(msg),
        }

        return __map[event_type](msg)


class TraceEventEncoder(json.JSONEncoder):
    casting = [
        bt2._UnsignedIntegerFieldConst,
        bt2._DoublePrecisionRealFieldConst,
        bt2._StringFieldConst,
        bt2._UnsignedEnumerationFieldConst,
    ]

    def default(self, obj):
        if type(obj) in self.casting:
            return str(obj)
        if isinstance(obj, TraceEvent):
            result = {}
            for key in obj.keys:
                result[key] = obj.get(key)
            return result
        return json.JSONEncoder.default(self, obj)


class RegionProfilesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, RegionProfiles):
            results = []
            for item in obj:
                results.append(item.toJSON())
            return results
        return json.JSONEncoder.default(self, obj)


class Comp(TraceEvent):
    @property
    def type(self):
        return "comp"

    @property
    def keys(self):
        return [
            "vmid",
            "baseid",
            "name",
            "IPM",
            "RPM",
            "FPM",
        ]


class RegionIdEnter(TraceEvent):
    @property
    def type(self):
        return "regionid_enter"

    @property
    def keys(self):
        return ["regionid"]


class RegionIdExit(TraceEvent):
    @property
    def type(self):
        return "regionid_exit"

    @property
    def keys(self):
        return ["regionid"]


class DefineRegion(TraceEvent):
    @property
    def type(self):
        return "define_region"

    @property
    def keys(self):
        return [
            "name",
            "pet",
            "id",
            "type",
            "vmid",
            "baseid",
            "method",
            "phase",
        ]


class RegionProfile(TraceEvent):
    @property
    def type(self):
        return "region_profile"

    @property
    def keys(self):
        return [
            "id",
            "parentid",
            "total",
            "count",
            "max",
            "min",
            "mean",
            "pet",
            "name",
        ]


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

    @functools.cached_property
    def profiles(self):
        return list(self._profiles)

    @functools.cached_property
    def petIds(self):
        return list(set(map(lambda x: x.get("pet"), self.profiles)))

    @functools.cached_property
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

        logger.debug("determining log levels")
        return self._populate_tree_from_map(self._build_tree_map(profiles))

    def _create_tree_json(self):
        return json.dumps(
            self._create_tree(),
            cls=TraceEventEncoder,
        )

    def _populate_tree_from_map(self, tree_map: list[Node]):
        return self._fetch_objs(tree_map)

    def _build_tree_map(self, profiles: list[Node]):
        return self._build_tree_from_root(profiles)

    def _fetch_objs(self, tree):
        for leaf in tree:
            leaf["node"] = list(
                filter(lambda x: x.get("id") == leaf["node"].id, self.profiles)
            )[0]
            if len(leaf["children"]):
                self._fetch_objs(leaf["children"])
        return tree

    def _build_tree_from_root(self, nodes: list[Node], root: Node = None):

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

    def _build_pet_tree(self, petIds, profiles: List[RegionProfile], accum: Dict = {}):
        logging.debug(f"remaining PETIDS:{len(petIds)} EVENTS:{len(profiles)}")
        if len(petIds) < 20:
            logging.debug(f"PETIDS REMAINING: {str(petIds)}")
        if len(petIds) > 0 and len(profiles) > 0:
            petId = list(petIds)[0]
            filtered = list(filter(lambda x: x.get("pet") == petId, profiles))
            accum[petId] = filtered
            remainder = list([x for x in set(profiles) if x not in set(filtered)])
            return self._build_pet_tree(list(petIds)[1:], remainder, accum)
        return accum

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
    def from_path(
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
