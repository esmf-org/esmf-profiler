from event import TraceEvent, DefineRegion, RegionProfile
from abc import ABC, abstractproperty
import logging

logger = logging.getLogger(__name__)

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
        raise NotImplementedError(
            f"{self.__class__.__name__} requires a finish method"
        )


class LoadBalance(Analysis):

    # rootRegionName is the name of the region to be used as
    # the root for the load balance plot
    # if None, then use the top level
    def __init__(self, rootRegionName):
        self._rootRegionName = rootRegionName
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
            #logger.debug(f"found DefineRegion pet = {pet}, id = {regionid}, name = {name}")
            self._regionIdToNameMap.setdefault(pet, {})[regionid] = name


        if isinstance(event, RegionProfile):
            pet = event.pet
            regionid = event.get("id")
            total = event.get("total")
            parentid = event.get("parentid")

            if regionid == 1:
                # special case for outermost timed region
                name = "ROOT"
            else:
                map = self._regionIdToNameMap[pet]
                name = map[regionid]  # should already be there

            #logger.debug(f"found RegionProfile pet = {pet}, id = {regionid}, parentid = {parentid}, name = {name}, total time = {total}")

            node = SinglePETTimingNode(id, name)
            node.total = total

            # add child to the timing tree for the given pet
            root = self._timingTrees.setdefault(pet, SinglePETTimingNode(0,""))
            root.add_child(parentid, node)

    def finish(self):
        # all events have been processed, so now we have a complete
        # list of timing trees, one per PET in self._timingTrees

        # use the information from the user to select which
        # node will be the root node of focus for the load balance plot

        if self._rootRegionName is None or self._rootRegionName == "":
            # use the first level regions in the timing trees
            pass

        else:
            # find the root by searching the tree?
            raise NotImplementedError(
                f"{self.__class__.__name__} load balance only implemented for root level"
            )

    def toJSON(self):
        # return JSON format for Javascript Charts
        pass


# class to represent as a tree the timing
# information in the RegionProfile events
# for now just deal with total times, since that
# is all we need for the initial chart
class SinglePETTimingNode():

    def __init__(self, id, name):
        self._id = id
        self._name = name
        self._total = 0
        self._children = []  # List[SinglePETTimingTreeNode]

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, value):
        self._total = value

    # add child node to the node with give parentid
    def add_child(self, parentid, child: 'SinglePETTimingNode'):
        if self._id == parentid:
            self._children.append(child)
            return True
        else:
            for c in self._children:
                if c.add_child(parentid, child):
                    return True
        return False
