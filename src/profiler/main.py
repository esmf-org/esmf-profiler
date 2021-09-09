""" Main point of execution

    Notes:

    * Remove any 'print_execution_time' calls before going to prod
"""

import cProfile
from collections import namedtuple
import json
import logging
import pstats
import io
from pstats import SortKey

from profiler.utils import print_execution_time

from profiler.trace import RegionProfiles, Trace

logger = logging.getLogger(__name__)
_format = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
logging.basicConfig(level=logging.INFO, format=_format)


RegionDefinition = namedtuple("RegionDefinition", "name pet id")
mapping = []


class Lookup:
    def __init__(self, trace):
        self._trace = trace
        self._data = []

    def find(self, petId, _id):
        return list(filter(lambda x: x.pet == petId and x.id == _id, self.data))[0].name

    @property
    @print_execution_time
    def data(self):
        if not len(self._data):
            self._data = [
                RegionDefinition(x.get("name"), x.get("pet"), x.get("id"))
                for x in filter(lambda x: x.type == "define_region", self._trace)  # type: ignore
            ]
        return self._data


@print_execution_time
def main():

    with cProfile.Profile() as pr:
        include = ["region_profile", "define_region"]
        exclude = []

        logger.info("creating trace")
        trace = Trace.from_path("./tests/fixtures/test-traces-large", include, exclude)
        logger.debug("complete")

        logger.info("filtering region profiles")
        region_profiles = filter(lambda x: x.type == "region_profile", trace)
        logger.debug("complete")

        logger.info("creating lookup table for region profiles")
        lookup = Lookup(trace)
        logger.debug("complete")

        logger.debug(f"performing 1 verification lookups")
        print(lookup.find(1, 24))
        logger.debug("complete")

        logger.info(f"creating tree from list of region profiles")
        profiles = RegionProfiles(list(region_profiles), lookup)._create_tree()
        logger.debug(f"complete; {len(profiles)} processed")

        logger.info(f"merging profiles to JSON")
        result = []
        for profile in profiles:
            result.append(profile.toJson())
        logger.debug("complete")

        logger.info(f"writing results to file")
        with open("results.json", "w") as _file:
            _file.write(json.dumps(result))
        logger.debug(f"complete")

        # summary = RegionSummary(cast(List[TraceEvent], trace))
        # print(summary.pet_count())
        # print(summary.count_each())

        s = io.StringIO()
        sortby = SortKey.TIME
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())


if __name__ == "__main__":
    main()
