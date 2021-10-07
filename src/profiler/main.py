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
import datetime
import subprocess
import glob

from profiler.utils import print_execution_time
from profiler.analyses import Analysis, LoadBalance
from profiler.trace import Trace

logger = logging.getLogger(__name__)
_format = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
logging.basicConfig(level=logging.DEBUG, format=_format)


def handle_args():
    parser = argparse.ArgumentParser(description='ESMF Profiler')
    parser.add_argument('-t', '--tracedir', help='directory containing the ESMF trace', required=True)
    parser.add_argument('-n', '--name', help='name to use for the generated profile', required=True)
    parser.add_argument('-o', '--outdir', help='path to output directory', required=True)
    parser.add_argument('-p', '--push', help='git url of remote repository where to push profile', required=False)
    args = vars(parser.parse_args())
    return args


# output some general JSON data
# to be used on the site
def write_site_json(data, dir):
    outfile = os.path.join(dir, "site.json")
    logger.debug(f"Writing site JSON to file: {outfile}")
    with open(outfile, "w") as outfile:
        json.dump(data, outfile)
    logger.debug(f"Finished writing site JSON file")


def push_to_repo(url, outdir, name):
    logger.debug(f"Pushing to repository: {url}")

    tmpdir = "./.pushtmp"
    Path(tmpdir).mkdir(parents=True, exist_ok=True)
    if not os.path.isdir(tmpdir):
        print(f"Cannot push to remote repo.  Failed to create temporary directory: {tmpdir}")
        return

    # TODO: this deletes/reclones every time which can be inefficient if the repo is large
    # instead we want to check whether it exists already and see if we can git pull
    cmd = ["rm", "-rf", "tmprepo"]
    logger.debug(f"CMD: {' '.join(cmd)}")
    stat = subprocess.run(cmd, cwd=tmpdir)

    cmd = ["git", "clone", url, "tmprepo"]
    logger.debug(f"CMD: {' '.join(cmd)}")
    stat = subprocess.run(cmd, cwd=tmpdir)

    cmd = ["whoami"]
    logger.debug(f"CMD: {' '.join(cmd)}")
    stat = subprocess.run(cmd, cwd=tmpdir, capture_output=True, text=True)
    logger.debug(f"whoami: {stat.stdout}")
    username = str(stat.stdout).strip()

    outdir = os.path.abspath(outdir)

    #now = datetime.datetime.now()
    #timestamp = now.strftime("%Y%m%d-%H%M%S")

    repopath = os.path.join(tmpdir, "tmprepo")
    repopath = os.path.abspath(repopath)
    logger.debug(f"Repo path: {repopath}")

    profilepath = os.path.join(repopath, username, name)
    profilepath = os.path.abspath(profilepath)
    logger.debug(f"Profile path: {profilepath}")
    Path(profilepath).mkdir(parents=True, exist_ok=True)

    cmd = ["cp", "-r"] + glob.glob(outdir+"/*") + [profilepath]
    logger.debug(f"CMD: {' '.join(cmd)}")
    stat = subprocess.run(cmd, cwd=tmpdir)

    cmd = ["git", "add"] + glob.glob(profilepath+"/*")
    logger.debug(f"CMD: {' '.join(cmd)}")
    stat = subprocess.run(cmd, cwd=repopath)

    cmd = ["git", "commit", "-a", "-m", f"'Commit profile {username}/{name}'"]
    logger.debug(f"CMD: {' '.join(cmd)}")
    stat = subprocess.run(cmd, cwd=repopath)

    cmd = ["git", "push", "origin"]
    logger.debug(f"CMD: {' '.join(cmd)}")
    stat = subprocess.run(cmd, cwd=repopath)


def main():

    args = handle_args()

    if not args["name"].isalnum():
        print(f"name argument must contain only letters and numbers: {args['name']}")
        return

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

    # write general site JSON
    site = {"name" : args["name"],
            "timestamp" : str(datetime.datetime.now())}
    write_site_json(site, outdatadir)

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

    if "push" in args:
        push_to_repo(url=args["push"], outdir=outdir, name=args["name"])


if __name__ == "__main__":
   main()
