""" Main point of execution

    Notes:

    * Remove any 'print_execution_time' calls before going to prod
"""

import cProfile
import json
import logging
import pstats
import io
import argparse
import os
from pathlib import Path

from profiler.utils import print_execution_time
from profiler.analyses import Analysis, LoadBalance
from profiler.trace import Trace

logger = logging.getLogger(__name__)
_format = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=_format)

def main():

    parser = argparse.ArgumentParser(description='ESMF Profiler')
    parser.add_argument('-t', '--tracedir', help='directory containing the ESMF trace', required=True)
    parser.add_argument('-n', '--name', help='name to use for the generated profile', required=True)
    parser.add_argument('-o', '--outdir', help='path to output directory', required=True)
    args = vars(parser.parse_args())

    tracedir = args["tracedir"]
    if not os.path.isdir(tracedir):
        print(f"tracedir does not exist: {tracedir}")
        return

    outdir = args["outdir"]
    outdatadir = os.path.join(outdir, "data")
    Path(outdatadir).mkdir(parents=True, exist_ok=True)

    if not os.path.isdir(outdatadir):
        print(f"Failed to create output directory: {outdir}")
        return

    #_path = "./tests/fixtures/test-traces/atm-ocn-concurrent"
    #_path = "./tests/fixtures/test-traces-large"

    # the only requested analysis is a load balance at the root level
    analyses = [LoadBalance(None, outdatadir)]

    logger.info(f"Processing trace: {tracedir}")
    trace = Trace.from_path(tracedir, analyses)
    logger.debug(f"Processing trace complete")

    # indicate to the analyses that all events have been processed
    logger.info(f"Finishing analyses")
    for analysis in analyses:
        analysis.finish()
        # analysis.toJSON()
    logger.debug(f"Finishing analyses complete")

if __name__ == "__main__":
   main()
