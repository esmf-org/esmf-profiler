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


def region_definitions(mapping, trace):
    if not len(mapping):
        mapping = [
            RegionDefinition(x.get("name"), x.get("pet"), x.get("id"))
            for x in filter(lambda x: x.type == "define_region", trace)
        ]


def get_name(petId, _id, haystack):
    return list(filter(lambda x: x.pet == petId and x.id == _id, haystack))[0].name  # type: ignore


@print_execution_time
def main():

    with cProfile.Profile() as pr:
        include = ["region_profile", "define_region"]
        exclude = []

        logger.info("creating trace")

        trace = Trace.from_path("./tests/fixtures/test-traces", include, exclude)

        region_profiles = filter(lambda x: x.type == "region_profile", trace)
        define_regions = [
            RegionDefinition(x.get("name"), x.get("pet"), x.get("id"))
            for x in filter(lambda x: x.type == "define_region", trace)
        ]
        print(get_name(1, 24, define_regions))

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
