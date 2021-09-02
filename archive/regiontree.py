import unittest
import sys
import collections

class RegionNodeTestCase(unittest.TestCase):
    #def setUp(self):
    #    self.widget = Widget('The widget')
    def test_create(self):
        rn = RegionNode()
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
        rn1 = RegionNode()
        rn1.pet = 1; rn1.count = 5; rn1.total = 5000; rn1.min = 900; rn1.max = 1100; rn1._mean = 1000; rn1.name = "r1"

        rn2 = RegionNode()
        rn2.pet = 2; rn2.count = 5; rn2.total = 5500; rn2.min = 800; rn2.max = 1050; rn2._mean = 998; rn2.name = "r2"

        rn1.add_child(rn2)
        rnx = rn1.get_child("r2")

        self.assertEquals(5500, rnx.total)

    def test_merge(self):

        rn1p1 = RegionNode()
        rn1p1.pet = 1; rn1p1.count = 5; rn1p1.total = 5000; rn1p1.min = 900; rn1p1.max = 1100; rn1p1._mean = 1000; rn1p1.name = "r1"

        rn1p2 = RegionNode()
        rn1p2.pet = 2; rn1p2.count = 5; rn1p2.total = 5500; rn1p2.min = 800; rn1p2.max = 1050; rn1p2._mean = 998; rn1p2.name = "r1"

        rn2p2 = RegionNode()
        rn2p2.pet = 2; rn2p2.count = 2; rn2p2.total = 200; rn2p2.min = 95; rn2p2.max = 105; rn2p2._mean = 100; rn2p2.name = "r2"
        rn1p2.add_child(rn2p2)

        rs = RegionSummary()
        rs.merge(rn1p1)

        self.assertEquals(1, rs.pet_count)
        self.assertEquals(5, rs.count_each)
        self.assertEquals(5000, rs.total_sum)
        self.assertEquals(900, rs.total_min)
        self.assertEquals(1, rs.total_min_pet)
        self.assertEquals(1100, rs.total_max)
        self.assertEquals(1, rs.total_max_pet)
        self.assertEquals(0, len(rs.children))

        rs.merge(rn1p2)
        self.assertEquals(2, rs.pet_count)
        self.assertEquals(5, rs.count_each)
        self.assertEquals(5000+5500, rs.total_sum)
        self.assertEquals(800, rs.total_min)
        self.assertEquals(2, rs.total_min_pet)
        self.assertEquals(1100, rs.total_max)
        self.assertEquals(1, rs.total_max_pet)
        self.assertEquals(1, len(rs.children))


class RegionNode:

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

    def add_child(self, other:'RegionNode'):
        self._children[other.name] = other

    def get_child(self, name):
        return self._children.get(name)

    #def get_self_or_descendant(self, local_id):
    #    if self._local_id == local_id:
    #        return self
    #    else:
    #        for c in self._children:
    #            r = self._children[c].get_self_or_descendant(local_id)
    #            if r is not None:
    #                return r
    #    return None

    def add_to_tree(self, node:'RegionNode', parent_id):
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
    return nanos / (1000*1000*1000)

class RegionSummary:

    def __init__(self):
        self._children = {}
        self._pet_count = 0
        self._count_each = -1
        self._counts_match = True
        self._total_sum = 0       # sum of all totals
        self._total_min = sys.maxsize     # min of all totals
        self._total_min_pet = -1  # PET with min total
        self._total_max = 0       # max of all totals
        self._total_max_pet = -1  # PET with max total
        self._region_nodes = {}   # map of contributing region nodes (key = PET)

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

    @property
    def contributing_nodes(self):
        #return self._region_nodes
        return collections.OrderedDict(sorted(self._region_nodes.items()))


    def _merge_children(self, other:RegionNode):
        for c in other.children:
            rs = self._children.setdefault(c, RegionSummary())
            rs.merge(other.children[c])

    def merge(self, other:RegionNode):
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

        self._region_nodes[other.pet] = other

        self._merge_children(other)



if __name__ == '__main__':
    unittest.main()
