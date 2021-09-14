""" Main point of execution

    Notes:

    * Remove any 'print_execution_time' calls before going to prod
"""

import cProfile
import json
import logging
import pstats
import io
from pstats import SortKey
from profiler.lookup import Lookup

from profiler.utils import print_execution_time

from profiler.trace import RegionProfile, RegionProfiles, Trace

logger = logging.getLogger(__name__)
_format = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=_format)


@print_execution_time
def main():
    """main

    HIGH PRI
    TODO pytest for mission critical
    TODO remove the write to file or put as option
    TODO I doubt the algo for levels/depth is right.. worked on a small scale, need to test for bigger
    TODO filters api (team req)
    TODO depth api (team req)
    TODO pipe out huge JSON and see how browser chokes (team req)
    TODO prob gonna need CLI sooner than later

    LOW PRI
    TODO get the Ids for the DTO and the source matching (ie petId shouldn't be converted to petid or pet)
    TODO Go over region summary.  Not implemented, but will need to be.  Boilerplate is there, needs testing.
    """

    with cProfile.Profile() as pr:
        _path = "./tests/fixtures/test-traces-large"

        include = ["region_profile", "define_region"]
        assert (
            "define_region" in include
        )  # TODO Until i have time to figure out something better
        exclude = []

        logger.info("creating trace")
        trace = Trace.from_path(_path, include, exclude)
        logger.debug("complete")

        logger.info("creating lookup table for region profiles")
        lookup = Lookup(trace)

        region_profiles = list(filter(lambda x: isinstance(x, RegionProfile), trace))
        for item in region_profiles:
            attribs = {"name": lookup.find(item.get("pet"), item.get("id"))}
            item._attributes = attribs
        logger.debug("complete")

        logger.info(f"creating tree from list of region profiles")
        tree = RegionProfiles(iter(region_profiles), lookup)._create_tree_json()
        print(tree)
        exit()

        # s = io.StringIO()
        # sortby = SortKey.TIME
        # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        # ps.print_stats()
        # print(s.getvalue())


if __name__ == "__main__":
    main()
