from profiler.event import TraceEvent, DefineRegion, RegionProfile
from typing import Dict
from abc import ABC, abstractproperty
import logging
import sys
import collections
import json
import pprint
import os

logger = logging.getLogger(__name__)
#_format = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
#logging.basicConfig(level=logging.DEBUG, format=_format)

# class to represent as a tree the timing
# information in the RegionProfile events
# for now just deal with total times, since that
# is all we need for the initial chart
class SinglePETTimingNode:
    def __init__(self, id, pet, name):
        self._id = id
        self._pet = pet
        self._name = name
        self._total = 0
        self._min = sys.maxsize
        self._max = 0
        self._mean = 0
        self._count = 0
        self._children = []  # List[SinglePETTimingTreeNode]

    @property
    def name(self):
        return self._name

    @property
    def pet(self):
        return self._pet

    @pet.setter
    def pet(self, value):
        self._pet = value

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, value):
        self._total = value

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, value):
        self._min = value

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value):
        self._max = value

    @property
    def mean(self):
        return self._mean

    @mean.setter
    def mean(self, value):
        self._mean = value

    @property
    def children(self):
        return self._children

    # add child node to the node with give parentid
    def add_child(self, parentid, child: "SinglePETTimingNode"):
        if self._id == parentid:
            self._children.append(child)
            return True
        else:
            for c in self._children:
                if c.add_child(parentid, child):
                    return True
        return False


class MultiPETTimingNode:
    def __init__(self):
        self._children: dict[
            str, MultiPETTimingNode
        ] = {}  # sub-regions in the timing tree  { name -> MultiPETTimingNode }
        self._pet_count = (
            0  # the number of PETs reporting timing information for this node
        )
        self._count_each = -1  # how many times each PET called into this region
        self._counts_match = True  # if counts_each is not the same for all reporting PETs, then this is False
        self._total_sum = 0  # sum of all totals
        self._total_min = sys.maxsize  # min of all totals
        self._total_min_pet = -1  # PET with min total
        self._total_max = 0  # max of all totals
        self._total_max_pet = -1  # PET with max total
        self._contributing_nodes = (
            {}
        )  # map of contributing SinglePETTimingNodes (key = PET)

    @property
    def pet_count(self):
        return self._pet_count

    @property
    def count_each(self):
        return self._count_each

    @property
    def counts_match(self):
        return self._counts_match

    @property
    def total_sum(self):
        return self._total_sum

    @property
    def total_sum_s(self):
        return nano_to_sec(self._total_sum())

    @property
    def total_mean(self):
        return self._total_sum / self._pet_count

    @property
    def total_mean_s(self):
        return nano_to_sec(self.total_mean)

    @property
    def total_min(self):
        return self._total_min

    @property
    def total_min_s(self):
        return nano_to_sec(self._total_min)

    @property
    def total_min_pet(self):
        return self._total_min_pet

    @property
    def total_max(self):
        return self._total_max

    @property
    def total_max_s(self):
        return nano_to_sec(self._total_max)

    @property
    def total_max_pet(self):
        return self._total_max_pet

    @property
    def children(self):
        return self._children

    # Returns a list of the SinglePETTimingNodes that were
    # used to create the timing statistics in this node.
    @property
    def contributing_nodes(self):
        # return self._region_nodes
        return self._contributing_nodes
        # return collections.OrderedDict(sorted(self._contributing_nodes.items()))

    def _merge_children(self, other: SinglePETTimingNode):
        for c in other.children:
            rs = self._children.setdefault(c.name, MultiPETTimingNode())
            rs.merge(c)

    # Update the statistics by adding a new
    # SinglePETTimingNode tree.  This will be called once
    # for all SinglePETTimingNode trees in the trace
    # to end up with one MultiPETTimingNode tree that
    # summarizes all the PET timings.
    def merge(self, other: SinglePETTimingNode):
        self._pet_count += 1
        if self._pet_count == 1:
            self._count_each = other.count
        elif self._count_each != other.count:
            self._counts_match = False

        self._total_sum += other.total
        if self._total_min > other.min:
            self._total_min = other.min
            self._total_min_pet = other.pet
        if self._total_max < other.max:
            self._total_max = other.max
            self._total_max_pet = other.pet

        self._contributing_nodes[other.pet] = other

        self._merge_children(other)

    # retrieve timings across pets with this
    # node as the root
    # returns a tuple (xvals, yvals) where:
    #  xvals is a list of pets  [0, 1, 2, 3 ....]
    #  yvals is a dict { 'region1': [t0, t1, t2, ...], 'region2': [t0, t1, t2, ..] }
    def load_balance(self):

        # x values are list of PETs from lowest to highest
        contributing_pets = sorted(self.contributing_nodes.keys())
        lowpet = min(contributing_pets)
        highpet = max(contributing_pets)
        pets = [*range(lowpet, highpet + 1)]

        # y values { region -> [time_pet0, time_pet1, ....] }
        child_regions = {}
        for name, child in self.children.items():
            totals = [0.0] * (highpet - lowpet + 1)  # total times
            for pet, cn in child.contributing_nodes.items():
                totals[pet - lowpet] = round(nano_to_sec(cn.total), 5)
            child_regions[str(name)] = totals

        return (pets, child_regions)


# an abstract class that all analyses will extend
# examples include LoadBalance, MemoryProfile, etc.
class Analysis(ABC):
    def __init__(self):
        pass

    @abstractproperty
    def process_event(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} requires a process_event method"
        )

    @abstractproperty
    def finish(self):
        raise NotImplementedError(f"{self.__class__.__name__} requires a finish method")


class LoadBalance(Analysis):

    # rootRegionName is the name of the region to be used as
    # the root for the load balance plot
    # if None, then use the top level
    # outdir = output location  TODO:  consider moving outdir to Analysis class since it is a common param
    def __init__(self, rootRegionName, outdir):
        self._rootRegionName = rootRegionName
        self._outdir = outdir
        # two level mapping
        # { pet -> { region_id -> region name } }
        self._regionIdToNameMap = {}

        # map pet -> root of timing tree
        self._timingTrees = {}

    def process_event(self, event: TraceEvent):

        if isinstance(event, DefineRegion):
            pet = event.pet
            regionid = event.get("id")
            name = event.get("name")
            # logger.debug(f"found DefineRegion pet = {pet}, id = {regionid}, name = {name}")
            self._regionIdToNameMap.setdefault(pet, {})[regionid] = name

        if isinstance(event, RegionProfile):
            pet = event.pet
            regionid = event.get("id")
            parentid = event.get("parentid")

            if regionid == 1:
                # special case for outermost timed region
                name = "ROOT"
            else:
                map = self._regionIdToNameMap[pet]
                name = map[regionid]  # should already be there

            # logger.debug(f"found RegionProfile pet = {pet}, id = {regionid}, parentid = {parentid}, name = {name}")

            node = SinglePETTimingNode(regionid, pet, name)
            node.total = event.get("total")
            node.count = event.get("count")
            node.min = event.get("min")
            node.max = event.get("max")

            # add child to the timing tree for the given pet
            root = self._timingTrees.setdefault(
                pet, SinglePETTimingNode(0, pet, "TOP_LEVEL")
            )
            if not root.add_child(parentid, node):
                raise RuntimeError(
                    f"{self.__class__.__name__} child not added to tree pet = {pet}, regionid = {regionid}, parentid = {parentid}, name = {name}"
                )

    def finish(self):
        # all events have been processed, so now we have a complete
        # list of timing trees, one per PET in self._timingTrees

        # merge all the SinglePETTimingNodes into a single tree
        multiPETTree = MultiPETTimingNode()
        for pet, t in self._timingTrees.items():
            multiPETTree.merge(t)

        # collect load balance timing results for all levels of the full tree
        results = {}
        self._full_tree_load_balance("", multiPETTree, results)

        # format into dictionary suitable for JSON output
        jsondict = {}
        for r in results:
            (xvals, yvals) = results[r]
            yvalsjson = [{"name": n, "data": totals} for n, totals in yvals.items()]
            jsondict[r] = {"xvals": xvals, "yvals": yvalsjson}

        outfile = os.path.join(self._outdir, "load_balance.json")
        logger.debug(f"Writing load balance JSON to file: {outfile}")
        with open(outfile, "w") as outfile:
            json.dump(jsondict, outfile)
        logger.debug(f"Finished writing load balance JSON file")

        pass

    def _full_tree_load_balance(
        self, prefix: str, node: MultiPETTimingNode, results: Dict[str, tuple]
    ):
        for name, child in node.children.items():
            name = prefix + "/" + str(name)
            if len(child.children) > 0:
                results[name] = child.load_balance()
            self._full_tree_load_balance(name, child, results)


# move this to utility layer
def nano_to_sec(nanos):
    return nanos / (1000 * 1000 * 1000)
