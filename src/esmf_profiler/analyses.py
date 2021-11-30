#pylint: disable=invalid-name

import collections
import logging
import queue
import sys
import threading
from abc import ABC, abstractmethod
from typing import Dict

import bt2

logger = logging.getLogger(__name__)


# class to represent as a tree the timing
# information in the RegionProfile events
# for now just deal with total times, since that
# is all we need for the initial chart
class SinglePETTimingNode:
    def __init__(self, _id, pet, name):
        self._id = _id
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
    def add_child(
        self, parentid, child: "SinglePETTimingNode"
    ):  # pylint: disable=protected-access
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
        return nano_to_sec(self._total_sum)

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
            sorted(
                self._children.items(), key=lambda item: item[1].total_sum, reverse=True
            )
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

    def _merge_children(
        self, other: SinglePETTimingNode
    ):  # pytlint: disable=invalid-name
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

    DEFAULT_NUM_THREADS = 1  # default number of threads for analysis processing

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
    MESSAGE_BUFFER_SIZE = 100

    # Maximum number of outstanding batches of
    # messages allowed.  When reached, the trace
    # read will block until the queue has open slots.
    MESSAGE_QUEUE_MAXSIZE = 100

    def __init__(self, num_threads: int = Analysis.DEFAULT_NUM_THREADS):
        super().__init__()
        self._num_threads = num_threads
        self._queues = []
        self._threads = []
        self._msg_buffers = []

        self._region_id_to_name_map = {}  # { pet -> { region_id -> region name } }
        self._timing_trees = {}  # { pet -> root of timing tree }

        # start listener threads
        for i in range(num_threads):
            t, q = self._start()
            self._queues.append(q)
            self._threads.append(t)
            self._msg_buffers.append([])
            logger.debug("%s: Started listener thread %s", self.__class__.__name__, i)

    def _start(self):

        q = queue.Queue(maxsize=LoadBalance.MESSAGE_QUEUE_MAXSIZE)

        def _listen_buffer():
            while True:
                msg_buffer = q.get(block=True)
                if msg_buffer is None:
                    q.task_done()
                    return
                for msg in msg_buffer:
                    self._handle_event(msg)
                q.task_done()

        # this implementation is for single messages instead of batches
        # def _listen():
        #    while True:
        #        msg = q.get(block=True)
        #        if msg is None:
        #            q.task_done()
        #            return
        #        self._handle_event(msg)
        #        q.task_done()

        t = threading.Thread(target=_listen_buffer, daemon=True)
        t.start()
        return t, q

    def _join(self):
        for i in range(self._num_threads):
            logger.debug(
                "%s: Waiting for thread %s to join", self.__class__.__name__, i
            )

            # queue up any remaining messages in the buffer
            self._queues[i].put(self._msg_buffers[i], block=True)
            # signal we are done
            self._queues[i].put(None, block=True)

            self._queues[i].join()
            self._threads[i].join()
            logger.debug("%s: Thread %s join complete", self.__class__.__name__, i)

    def debug_log_queues(self):
        for i in range(self._num_threads):
            logger.debug(
                "%s \tQueue for thread %s size is {self._queues[i].qsize()}",
                self.__class__.__name__,
                self._queues[i].qsize(),
            )

    def process_event(self, msg: bt2._EventMessageConst):

        # determine which thread
        if self._num_threads > 1:
            pet = int(msg.event.packet.context_field["pet"])
            i = pet % self._num_threads
        else:
            i = 0

        self._msg_buffers[i].append(msg)
        if len(self._msg_buffers[i]) == LoadBalance.MESSAGE_BUFFER_SIZE:
            self._queues[i].put(self._msg_buffers[i], block=True)
            self._msg_buffers[i] = []

    # this implementation for handling single messages instead of batches
    # def process_event(self, msg: bt2._EventMessageConst):
    #    self._event_queue.put(msg, block=True)

    def _handle_event(self, msg: bt2._EventMessageConst):

        if msg.event.name == "define_region":
            pet = int(msg.event.packet.context_field["pet"])
            regionid = int(msg.event.payload_field["id"])
            name = str(msg.event.payload_field["name"])
            self._region_id_to_name_map.setdefault(pet, {})[regionid] = name

        elif msg.event.name == "region_profile":
            pet = int(msg.event.packet.context_field["pet"])
            regionid = int(msg.event.payload_field["id"])
            parentid = int(msg.event.payload_field["parentid"])

            if regionid == 1:
                # special case for outermost timed region
                name = "TOP"
            else:
                _map = self._region_id_to_name_map[pet]
                name = _map[regionid]  # should already be there

            node = SinglePETTimingNode(regionid, pet, name)
            node.total = int(msg.event.payload_field["total"])
            node.count = int(msg.event.payload_field["count"])
            node.min = int(msg.event.payload_field["min"])
            node.max = int(msg.event.payload_field["max"])

            # add child to the timing tree for the given pet
            root = self._timing_trees.setdefault(
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

        logger.info("Completing analysis: %s", self.__class__.__name__)

        # merge all the SinglePETTimingNodes into a single tree
        multiPETTree = MultiPETTimingNode()
        for _, t in self._timing_trees.items():
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
