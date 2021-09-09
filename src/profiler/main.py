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

        trace = Trace.from_path("./tests/fixtures/test-traces", include, exclude)
        lookup = Lookup(trace)

        region_profiles = filter(lambda x: x.type == "region_profile", trace)

        print(lookup.find(1, 24))
        print(lookup.find(1, 24))
        print(lookup.find(1, 24))

        # for region in define_regions:
        #     print(region)
        # for item in define_regions:
        #     print(item)
        exit()
        print(list(define_regions)[0])
        print("*" * 10)
        print(list(region_profiles))
        exit(0)

        logger.info("creating tree")

        profiles = RegionProfiles(list(trace))._create_tree()
        result = []
        for profile in profiles:
            result.append(profile.toJson())
        print(json.dumps(result))

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
