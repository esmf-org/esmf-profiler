from typing import List, cast
from profiler.trace import RegionProfile, RegionProfiles, Trace


def main():
    trace = Trace.from_directory("./tests/fixtures")
    trace = cast(
        List[RegionProfile], list(trace.filter(lambda x: isinstance(x, RegionProfile)))
    )
    profiles = RegionProfiles(trace)._create_tree()
    for item in profiles:
        print(item)

    # summary = RegionSummary(trace)
    # print(summary.pet_count())
    # print(summary.count_each())
    # for msg in trace:

    #     print(msg)


if __name__ == "__main__":
    main()
