import functools
from collections import namedtuple

from profiler.utils import print_execution_time

RegionDefinition = namedtuple("RegionDefinition", "name pet id")


class Lookup:
    def __init__(self, trace):
        self._trace = trace

    def find(self, petId, _id):
        # TODO error handle for no results, empty array
        # TODO typehint
        data = self.data # I think this is needed for caching... it was being called as method for some reason.
        
        return list(filter(lambda x: x.pet == petId and x.id == _id, data))[0].name

    @functools.cached_property  # Make sure this is being cached correctly
    def data(self):
        return [
            RegionDefinition(x.get("name"), x.get("pet"), x.get("id"))
            for x in filter(lambda x: x.type == "define_region", self._trace)  # type: ignore
        ]
