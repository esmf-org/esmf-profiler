import cProfile
import json
import logging
import pstats
import io
from pstats import SortKey
from typing import List, cast

from profiler.utils import print_execution_time

from profiler.trace import RegionProfile, RegionProfiles, Trace

log = logging.getLogger(__name__)
_format = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
logging.basicConfig(level=logging.INFO, format=_format)


@print_execution_time
def main():

    with cProfile.Profile() as pr:
        include = ["region_profile"]
        exclude = []

        log.info("creating trace")

        trace = cast(
            List[RegionProfile],
            list(
                Trace.from_path("./tests/fixtures/test-traces-large", include, exclude)
            ),
        )

        log.info("creating tree")

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
