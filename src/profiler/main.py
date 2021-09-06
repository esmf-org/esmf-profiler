import cProfile
from typing import List, cast
from profiler.trace import RegionProfile, RegionProfiles, Trace
import datetime


def stamp():
    return datetime.datetime.now()


def main():

    with cProfile.Profile() as pr:
        include = ["region_profile"]
        exclude = []
        trace = cast(
            List[RegionProfile],
            list(
                Trace.from_directory(
                    "./tests/fixtures/test-traces-large", include, exclude
                )
            ),
        )

        # Can filter in instructor
        # trace = cast(
        #     List[RegionProfile], list(trace.filter(lambda x: isinstance(x, RegionProfile)))
        # )
        # print(f"{stamp()}: creating tree")
        # profiles = RegionProfiles(list(trace))._create_tree()
        # # print(profiles.values())
        # obj = dict(
        #     zip(
        #         profiles.keys(),
        #         [profile.toJson().replace("\\", "") for profile in profiles.values()],
        #     )
        # )
        # print(f"{stamp()}: complete")
        # print(json.dumps(obj))

        # summary = RegionSummary(trace)
        # print(summary.pet_count())
        # print(summary.count_each())

        pr.print_stats()


if __name__ == "__main__":
    main()
