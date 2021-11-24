import threading
from typing import Dict
from abc import ABC, abstractmethod
import logging
import sys
import collections
import bt2
import queue

logger = logging.getLogger(__name__)


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

        # only the root maintains a cache (self._id = 0)
        self._child_cache = {}  # id -> SinglePetTimingTreeNode
        if self._id == 0:
            self._child_cache[self._id] = self

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
    # must be called only from root SinglePETTimingNode
    def add_child(self, parentid, child: "SinglePETTimingNode"):
        self._child_cache[parentid]._children.append(child)
        self._child_cache[child._id] = child
        return True


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

    # sort children by total time
    # works recursively down the tree
    def sort_children(self):
        sd = collections.OrderedDict(
            sorted(self._children.items(), key=lambda item: item[1].total_sum, reverse=True)
        )
        self._children = sd

        for c in self._children:
            self._children[c].sort_children()

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

    @abstractmethod
    def process_event(self, msg: bt2._EventMessageConst):
        raise NotImplementedError(
            f"{self.__class__.__name__} requires a process_event method"
        )

    @abstractmethod
    def finish(self):
        raise NotImplementedError(f"{self.__class__.__name__} requires a finish method")


class LoadBalance(Analysis):

    # Number of messages to buffer from the trace
    # before handling them in a batch
    MESSAGE_BUFFER_SIZE = 2500

    # Maximum number of outstanding batches of
    # messages allowed.  When reached, the trace
    # read will block until the queue has open slots.
    MESSAGE_QUEUE_MAXSIZE = 100

    def __init__(self):
        self._event_queue = queue.Queue(maxsize=LoadBalance.MESSAGE_QUEUE_MAXSIZE)
        self._thread = None
        self._msg_buffer = []

        self._regionIdToNameMap = {}  # { pet -> { region_id -> region name } }
        self._timingTrees = {}        # { pet -> root of timing tree }

        # start thread that listens for events
        self._start()

    def _start(self):

        def _listen_buffer():
            while True:
                msg_buffer = self._event_queue.get(block=True)
                for msg in msg_buffer:
                    if msg is None:
                        self._event_queue.task_done()
                        return
                    self._handle_event(msg)

                self._event_queue.task_done()

        # this implementation is for single messages instead of batches
        # def _listen():
        #    while True:
        #        msg = self._event_queue.get(block=True)
        #        if msg is None:
        #            self._event_queue.task_done()
        #            return
        #        self._handle_event(msg)
        #        self._event_queue.task_done()

        self._thread = threading.Thread(target=_listen_buffer, daemon=True)
        self._thread.start()

    def _join(self):
        logger.debug(f"{self.__class__.__name__}: Waiting for queue to join")
        self.process_event(None)  # signal we are done
        self._event_queue.join()
        self._thread.join()
        logger.debug(f"{self.__class__.__name__}: Queue join complete")

    def queue_size(self):
        return self._event_queue.qsize()

    def process_event(self, msg: bt2._EventMessageConst):
        self._msg_buffer.append(msg)
        if len(self._msg_buffer) == LoadBalance.MESSAGE_BUFFER_SIZE or msg is None:
            self._event_queue.put(self._msg_buffer, block=True)
            self._msg_buffer = []

    # this implementation for handling single messages instead of batches
    # def process_event(self, msg: bt2._EventMessageConst):
    #    self._event_queue.put(msg, block=True)

    def _handle_event(self, msg: bt2._EventMessageConst):

        if msg.event.name == "define_region":
            pet = int(msg.event.packet.context_field["pet"])
            regionid = int(msg.event.payload_field["id"])
            name = str(msg.event.payload_field["name"])
            self._regionIdToNameMap.setdefault(pet, {})[regionid] = name

        elif msg.event.name == "region_profile":
            pet = int(msg.event.packet.context_field["pet"])
            regionid = int(msg.event.payload_field["id"])
            parentid = int(msg.event.payload_field["parentid"])

            if regionid == 1:
                # special case for outermost timed region
                name = "TOP"
            else:
                map = self._regionIdToNameMap[pet]
                name = map[regionid]  # should already be there

            node = SinglePETTimingNode(regionid, pet, name)
            node.total = int(msg.event.payload_field["total"])
            node.count = int(msg.event.payload_field["count"])
            node.min = int(msg.event.payload_field["min"])
            node.max = int(msg.event.payload_field["max"])

            # add child to the timing tree for the given pet
            root = self._timingTrees.setdefault(
                pet, SinglePETTimingNode(0, pet, "TOP_LEVEL")
            )
            if not root.add_child(parentid, node):
                raise RuntimeError(
                    f"{self.__class__.__name__} child not added to tree pet = {pet}, regionid = {regionid}, parentid = {parentid}, name = {name}"
                )

    def finish(self):

        # wait for message handling thread to complete
        self._join()

        # all events have been processed, so now we have a complete
        # list of timing trees, one per PET in self._timingTrees

        logger.info(f"Completing analysis: {self.__class__.__name__}")

        # merge all the SinglePETTimingNodes into a single tree
        multiPETTree = MultiPETTimingNode()
        for pet, t in self._timingTrees.items():
            multiPETTree.merge(t)

        multiPETTree.sort_children()

        # collect load balance timing results for all levels of the full tree
        results = {}
        self._full_tree_load_balance("", multiPETTree, results)

        # format into dictionary suitable for JSON output
        jsondict = {}
        for r in results:
            (xvals, yvals) = results[r]
            yvalsjson = [{"name": n, "data": totals} for n, totals in yvals.items()]
            jsondict[r] = {"xvals": xvals, "yvals": yvalsjson}

        return jsondict

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
