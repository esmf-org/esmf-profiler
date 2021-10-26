""" Main point of execution

    Notes:

    * Remove any 'print_execution_time' calls before going to prod
"""


import datetime
import errno
import glob
import json
import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from profiler.analyses import LoadBalance
from profiler.trace import Trace
from profiler.view import handle_args

logger = logging.getLogger(__name__)


def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else:
            raise


# output some general JSON data
# to be used on the site
def write_site_json(data, dir):
    outfile = os.path.join(dir, "site.json")
    logger.debug(f"Writing site JSON to file: {outfile}")
    with open(outfile, "w") as outfile:
        json.dump(data, outfile)
    logger.debug(f"Finished writing site JSON file")


def command_safe(cmd, cwd):
    logger.debug(f"CMD: {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=cwd, check=True)


def git_add(profilepath, repopath):
    cmd = ["git", "add"] + glob.glob(profilepath + "/*")
    logger.debug(f"CMD: {' '.join(cmd)}")
    return command_safe(cmd, repopath)


def git_commit(username, name, repopath):
    cmd = ["git", "commit", "-a", "-m", f"'Commit profile {username}/{name}'"]
    logger.debug(f"CMD: {' '.join(cmd)}")
    return command_safe(cmd, repopath)


def git_push(repopath):
    cmd = ["git", "push", "origin"]
    logger.debug(f"CMD: {' '.join(cmd)}")
    return command_safe(cmd, repopath)


def git_clone(url, tmpdir):
    cmd = ["git", "clone", url, "tmprepo"]
    return command_safe(cmd, tmpdir)


def profile_path(repopath, username, name):
    profilepath = os.path.join(repopath, username, name)
    profilepath = os.path.abspath(profilepath)
    logger.debug(f"Profile path: {profilepath}")
    Path(profilepath).mkdir(parents=True, exist_ok=True)
    return profilepath


def repo_path(_root):
    repopath = os.path.join(_root, "tmprepo")
    repopath = os.path.abspath(repopath)
    logger.debug(f"Repo path: {repopath}")
    return repopath


def _whoami(tmpdir):
    cmd = ["whoami"]
    command_safe(cmd, tmpdir)
    stat = subprocess.run(cmd, cwd=tmpdir, stdout=subprocess.PIPE, encoding="utf-8")
    return str(stat.stdout).strip()


def push_to_repo(url, outdir, name):
    logger.info(f"Pushing to repository: {url}")

    with tempfile.TemporaryDirectory() as tmpdir:

        # TODO: https://github.com/esmf-org/esmf-profiler/issues/42
        shutil.rmtree("tmprepo")

        git_clone(url, tmpdir)
        username = _whoami(tmpdir)
        outdir = os.path.abspath(outdir)

        repopath = repo_path(tmpdir)
        profilepath = profile_path(repopath, username, name)
        cwd = os.getcwd()  # assumes we are running from esmf-profiler directory

        # copy static site
        # TODO:  need a more robust way to get a handle on the esmf-profiler root path
        # either that or we need to bundle the static site files into the Python install
        copyanything(os.path.join(cwd, "/web/app/build/*"), profilepath)

        # copy json data
        copyanything(os.path.join(outdir, "/data"), profilepath)

        git_add(profilepath, repopath)
        git_commit(username, name, repopath)
        git_push(repopath)


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
