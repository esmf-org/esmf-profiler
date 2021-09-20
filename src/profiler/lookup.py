import functools
from collections import namedtuple

from profiler.utils import print_execution_time

RegionDefinition = namedtuple("RegionDefinition", "name pet id")


class Lookup:
    def __init__(self, trace):
        self._trace = trace
        self._data = None

    def find(self, petId, _id):
        # TODO error handle for no results, empty array
        # TODO typehint
        data = (
            self.data
        )  # I think this is needed for caching... it was being called as method for some reason.

        value = list(filter(lambda x: x.pet == petId and x.id == _id, data))
        return value[0].name if len(value) else ""

      # Make sure this is being cached correctly
    def data(self):
        if self._data is None:
            self._data = [
            RegionDefinition(x.get("name"), x.get("pet"), x.get("id"))
            for x in filter(lambda x: x.type == "define_region", self._trace)  # type: ignore
        ]
