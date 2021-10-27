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


def copy_path(src, dst):
    """copy_path copy one path to another including contents

    Args:
        src (str):
        dst (str):
    """
    try:
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else:
            raise


# output some general JSON data
# to be used on the site
def write_site_json(data, _dir, file_name="site.json"):
    with open(os.path.join(_dir, file_name), "w", encoding="utf-8") as _file:
        json.dump(data, _file)


def command_safe(cmd, cwd=os.getcwd()):
    return subprocess.run(
        cmd, cwd=cwd, check=True, stdout=subprocess.PIPE, encoding="utf-8"
    )


def git_add(profilepath, repopath):
    cmd = ["git", "add"] + glob.glob(profilepath + "/*")
    return command_safe(cmd, repopath)


def git_commit(username, name, repopath):
    cmd = ["git", "commit", "-a", "-m", f"'Commit profile {username}/{name}'"]
    return command_safe(cmd, repopath)


def git_pull(repopath):
    cmd = ["git", "pull", "origin"]
    return command_safe(cmd, repopath)


def git_push(repopath):
    cmd = ["git", "push", "origin"]
    return command_safe(cmd, repopath)


def git_clone(url, tmpdir):
    cmd = ["git", "clone", url, "tmprepo"]
    return command_safe(cmd, tmpdir)


def create_profile_path(repopath, username, name):
    profilepath = os.path.abspath(os.path.join(repopath, username, name))
    Path(profilepath).mkdir(parents=True, exist_ok=True)
    return profilepath


def create_temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        return tmpdir


def _whoami():
    return command_safe(["whoami"]).stdout.strip()


def push_to_repo(url, outdir, name):
    logger.info(f"Pushing to repository: {url}")

    with tempfile.TemporaryDirectory() as tmpdir:

        # TODO: https://github.com/esmf-org/esmf-profiler/issues/42
        username = _whoami()

        repopath = create_temp_dir()
        profilepath = create_profile_path(repopath, username, name)

        # copy static site
        # TODO:  need a more robust way to get a handle on the esmf-profiler root path
        # either that or we need to bundle the static site files into the Python install
        git_pull(repopath)
        copy_path(os.path.join(os.getcwd(), "/web/app/build/*"), profilepath)

        # copy json data
        copy_path(os.path.join(outdir, "/data"), profilepath)

        git_add(profilepath, repopath)
        git_commit(username, name, repopath)
        git_push(repopath)


def handle_logging(verbosity):
    if verbosity > 0:
        _format = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=_format)
    else:
        _format = "%(name)s : %(message)s"
        logging.basicConfig(level=logging.INFO, format=_format)


def create_directory(paths):
    _path = os.path.join(*paths)
    Path(_path).mkdir(parents=True, exist_ok=True)
    return _path


def main():
    # collect user args
    args = handle_args()

    # setup logging based on args.verbose
    handle_logging(args.verbose)

    outdatadir = create_directory([args.outdir, "data"])

    # write site.json 
    write_site_json(
        {"name": args["name"], "timestamp": str(datetime.datetime.now())}, outdatadir
    )

    # the only requested analysis is a load balance at the root level
    
    analyses = [LoadBalance(None, outdatadir)]

    logger.info(f"Processing trace: {args.tracedir}")
    trace = Trace.from_path(args.tracedir, analyses)
    logger.debug("Processing trace complete")

    # indicate to the analyses that all events have been processed
    logger.info("Generating profile")
    for analysis in analyses:
        analysis.finish()
    logger.debug("Finishing analyses complete")

    if args["push"] is not None:
        push_to_repo(
            url=args["push"], outdir=os.path.abspath(args.outdir), name=args["name"]
        )


if __name__ == "__main__":
    main()
