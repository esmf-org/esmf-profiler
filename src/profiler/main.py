import cProfile
import datetime
import io
import json
import pstats
import time
from pstats import SortKey
from typing import List, cast

from profiler.trace import (
    RegionProfile,
    RegionProfiles,
    RegionSummary,
    Trace,
    TraceEvent,
)


def st_time(func):
    """
    st decorator to calculate the total time of a func
    """

    def st_func(*args, **keyArgs):
        t1 = time.time()
        r = func(*args, **keyArgs)
        t2 = time.time()
        print("Function=%s, Time=%s" % (func.__name__, t2 - t1))
        return r

    return st_func


def log(msg: str):
    print(f"{datetime.datetime.now()}: {msg}")


@st_time
def main():

    with cProfile.Profile() as pr:
        include = ["region_profile"]
        exclude = []

        log("creating trace")

        trace = cast(
            List[RegionProfile],
            list(
                Trace.from_path("./tests/fixtures/test-traces-large", include, exclude)
            ),
        )

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
