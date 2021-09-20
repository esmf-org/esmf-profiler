""" Main point of execution

    Notes:

    * Remove any 'print_execution_time' calls before going to prod
"""

import cProfile
import json
import logging
import pstats
import io

from profiler.utils import print_execution_time
from profiler.analyses import Analysis, LoadBalance
from profiler.trace import Trace

logger = logging.getLogger(__name__)
_format = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=_format)


@print_execution_time
def main():

    _path = "./tests/fixtures/test-traces/atm-ocn"
    #_path = "./tests/fixtures/test-traces-large-tmp"

    # the only requested analysis is a load balance at the root level
    analyses = [LoadBalance(None)]

    logger.info(f"Processing trace: {_path}")
    trace = Trace.from_path(_path, analyses)
    logger.debug(f"Processing trace complete")

    # indicate to the analyses that all events have been processed
    logger.info(f"Finishing analyses")
    for analysis in analyses:
        analysis.finish()
        # analysis.toJSON()
    logger.info(f"Finishing analyses complete")

if __name__ == "__main__":
    main()
