import unittest
import sys
import collections


class TimingTreeTestCase(unittest.TestCase):
    # def setUp(self):
    #    self.widget = Widget('The widget')
    def test_create(self):
        rn = SinglePETTimingNode(1)
        rn.pet = 444
        rn.count = 100
        rn.max = 50
        rn.min = 10
        rn.total = 99
        rn.mean = 55
        rn.name = "test"
        self.assertEqual(100, rn.count, "incorrect count")
        self.assertEqual(50, rn.max, "incorrect max")
        self.assertEqual(10, rn.min, "incorrect max")
        self.assertEqual(99, rn.total, "incorrect max")
        self.assertEqual(55, rn.mean, "incorrect max")
        self.assertEqual("test", rn.name, "wrong name")
        self.assertEqual(444, rn.pet, "wrong pet")

    def test_child(self):
        rn1 = SinglePETTimingNode(1)
        rn1.pet = 1
        rn1.count = 5
        rn1.total = 5000
        rn1.min = 900
        rn1.max = 1100
        rn1._mean = 1000
        rn1.name = "r1"

        rn2 = SinglePETTimingNode(1)
        rn2.pet = 2
        rn2.count = 5
        rn2.total = 5500
        rn2.min = 800
        rn2.max = 1050
        rn2._mean = 998
        rn2.name = "r2"

        rn1.add_child(rn2)
        rnx = rn1.get_child("r2")

        self.assertEqual(5500, rnx.total)

    def test_merge(self):

        rn1p1 = SinglePETTimingNode(1)
        rn1p1.pet = 1
        rn1p1.count = 5
        rn1p1.total = 5000
        rn1p1.min = 900
        rn1p1.max = 1100
        rn1p1._mean = 1000
        rn1p1.name = "r1"

        rn1p2 = SinglePETTimingNode(2)
        rn1p2.pet = 2
        rn1p2.count = 5
        rn1p2.total = 5500
        rn1p2.min = 800
        rn1p2.max = 1050
        rn1p2._mean = 998
        rn1p2.name = "r1"

        rn2p2 = SinglePETTimingNode(3)
        rn2p2.pet = 2
        rn2p2.count = 2
        rn2p2.total = 200
        rn2p2.min = 95
        rn2p2.max = 105
        rn2p2._mean = 100
        rn2p2.name = "r2"
        rn1p2.add_child(rn2p2)

        rs = MultiPETTimingNode()
        rs.merge(rn1p1)

        self.assertEqual(1, rs.pet_count)
        self.assertEqual(5, rs.count_each)
        self.assertEqual(5000, rs.total_sum)
        self.assertEqual(900, rs.total_min)
        self.assertEqual(1, rs.total_min_pet)
        self.assertEqual(1100, rs.total_max)
        self.assertEqual(1, rs.total_max_pet)
        self.assertEqual(0, len(rs.children))

        rs.merge(rn1p2)
        self.assertEqual(2, rs.pet_count)
        self.assertEqual(5, rs.count_each)
        self.assertEqual(5000 + 5500, rs.total_sum)
        self.assertEqual(800, rs.total_min)
        self.assertEqual(2, rs.total_min_pet)
        self.assertEqual(1100, rs.total_max)
        self.assertEqual(1, rs.total_max_pet)
        self.assertEqual(1, len(rs.children))


#
# These nodes form a "timing tree" for a single PET (process).
# In general, a trace will have timing information for multiple
# PETs, so you will end up with multiple timing trees, one per PET.
#
# A textual version of a single PET timing tree is in the
# ESMF reference manual:
#
# http://earthsystemmodeling.org/docs/nightly/develop/ESMF_refdoc/node6.html#SECTION060132100000000000000
#
class SinglePETTimingNode:
    def __init__(self, id):
        self._local_id = id
        self._pet = -1
        self._count = -1
        self._total = -1
        self._min = -1
        self._max = -1
        self._mean = -1
        self._name = ""
        self._children = {}

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def pet(self):
        return self._pet

    @pet.setter
    def pet(self, value):
        self._pet = value

    @property
    def local_id(self):
        return self._local_id

    @local_id.setter
    def local_id(self, value):
        self._local_id = value

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, value):
        self._total = value

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

    def add_child(self, other: "SinglePETTimingNode"):
        self._children[other.name] = other

    def get_child(self, name):
        return self._children.get(name)

    # def get_self_or_descendant(self, local_id):
    #    if self._local_id == local_id:
    #        return self
    #    else:
    #        for c in self._children:
    #            r = self._children[c].get_self_or_descendant(local_id)
    #            if r is not None:
    #                return r
    #    return None

    def add_to_tree(self, node: "SinglePETTimingNode", parent_id):
        if self._local_id == parent_id:
            self.add_child(node)
            return True
        else:
            for c in self._children:
                if self._children[c].add_to_tree(node, parent_id):
                    return True
        return False

    @property
    def children(self):
        return self._children


def nano_to_sec(nanos):
    return nanos / (1000 * 1000 * 1000)


#
# This class aggregates multiple SinglePETTimingNodes into
# a single tree with timing statistics.
#
# An example of a MultiPETTimingNode tree in the ESMF Reference Manual:
#
# http://earthsystemmodeling.org/docs/nightly/develop/ESMF_refdoc/node6.html#SECTION060132200000000000000
#
class MultiPETTimingNode:
    def __init__(self):
        self._children = {}  # sub-regions in the timing tree
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
        self._single_pet_nodes = (
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

    #
    # Returns a list of the SinglePETTimingNodes that were
    # used to create the timing statistics in this node.
    @property
    def contributing_nodes(self):
        # return self._region_nodes
        return collections.OrderedDict(sorted(self._single_pet_nodes.items()))

    def _merge_children(self, other: SinglePETTimingNode):
        for c in other.children:
            rs = self._children.setdefault(c, MultiPETTimingNode())
            rs.merge(other.children[c])

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

        self._single_pet_nodes[other.pet] = other

        self._merge_children(other)


if __name__ == "__main__":
    unittest.main()
