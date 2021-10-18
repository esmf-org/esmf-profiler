""" Main point of execution

    Notes:

    * Remove any 'print_execution_time' calls before going to prod
"""


import datetime
import glob
import json
import logging
import os
import subprocess
from pathlib import Path

from profiler.analyses import LoadBalance
from profiler.trace import Trace
from profiler.view import handle_args

logger = logging.getLogger(__name__)

# output some general JSON data
# to be used on the site
def write_site_json(data, dir):
    outfile = os.path.join(dir, "site.json")
    logger.debug(f"Writing site JSON to file: {outfile}")
    with open(outfile, "w") as outfile:
        json.dump(data, outfile)
    logger.debug(f"Finished writing site JSON file")


def push_to_repo(url, outdir, name):
    logger.info(f"Pushing to repository: {url}")

    tmpdir = "./.pushtmp"
    Path(tmpdir).mkdir(parents=True, exist_ok=True)
    if not os.path.isdir(tmpdir):
        print(
            f"Cannot push to remote repo.  Failed to create temporary directory: {tmpdir}"
        )
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
    stat = subprocess.run(cmd, cwd=tmpdir, stdout=subprocess.PIPE, encoding="utf-8")
    username = str(stat.stdout).strip()
    logger.debug(f"CMD: whoami returned: {username}")

    outdir = os.path.abspath(outdir)

    # now = datetime.datetime.now()
    # timestamp = now.strftime("%Y%m%d-%H%M%S")

    repopath = os.path.join(tmpdir, "tmprepo")
    repopath = os.path.abspath(repopath)
    logger.debug(f"Repo path: {repopath}")

    profilepath = os.path.join(repopath, username, name)
    profilepath = os.path.abspath(profilepath)
    logger.debug(f"Profile path: {profilepath}")
    Path(profilepath).mkdir(parents=True, exist_ok=True)

    # copy static site
    # TODO:  need a more robust way to get a handle on the esmf-profiler root path
    # either that or we need to bundle the static site files into the Python install
    cwd = os.getcwd()  # assumes we are running from esmf-profiler directory
    cmd = ["cp", "-r"] + glob.glob(cwd + "/web/app/build/*") + [profilepath]
    logger.debug(f"CMD: {' '.join(cmd)}")
    stat = subprocess.run(cmd, cwd=tmpdir)

    # copy json data
    cmd = ["cp", "-r", outdir + "/data", profilepath]
    logger.debug(f"CMD: {' '.join(cmd)}")
    stat = subprocess.run(cmd, cwd=tmpdir)

    cmd = ["git", "add"] + glob.glob(profilepath + "/*")
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

    if args["verbose"] > 0:
        _format = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=_format)
    else:
        _format = "%(name)s : %(message)s"
        logging.basicConfig(level=logging.INFO, format=_format)

    tracedir = args["tracedir"]
    outdir = args["outdir"]
    outdatadir = os.path.join(outdir, "data")
    Path(outdatadir).mkdir(parents=True, exist_ok=True)

    if not os.path.isdir(outdatadir):
        print(f"Failed to create output directory: {outdir}")
        return

    # write general site JSON
    site = {"name": args["name"], "timestamp": str(datetime.datetime.now())}
    write_site_json(site, outdatadir)

    # the only requested analysis is a load balance at the root level
    analyses = [LoadBalance(None, outdatadir)]

    logger.info(f"Processing trace: {tracedir}")
    trace = Trace.from_path(tracedir, analyses)
    logger.debug(f"Processing trace complete")

    # indicate to the analyses that all events have been processed
    logger.info(f"Generating profile")
    for analysis in analyses:
        analysis.finish()
    logger.debug(f"Finishing analyses complete")

    if args["push"] is not None:
        push_to_repo(url=args["push"], outdir=outdir, name=args["name"])


if __name__ == "__main__":
    main()
