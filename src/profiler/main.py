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
from git import git_add, git_clone, git_commit, git_pull, git_push


from profiler.analyses import LoadBalance
from profiler.trace import Trace
from profiler.view import handle_args as _handle_args

logger = logging.getLogger(__name__)


def _copy_path(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else:
            raise


# output some general JSON data
# to be used on the site
def _write_json_to_file(data, _path):
    with open(_path, "w", encoding="utf-8") as _file:
        json.dump(data, _file)


def _command_safe(cmd, cwd=os.getcwd()):
    return subprocess.run(
        cmd, cwd=cwd, check=True, stdout=subprocess.PIPE, encoding="utf-8"
    )

def _create_temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        return tmpdir


def _whoami():
    return _command_safe(["whoami"]).stdout.strip()


def _push_to_repo(url, outdir, name):
    logger.info("Pushing to repository: %s", url)

    with tempfile.TemporaryDirectory() as tmpdir:

        # TODO: https://github.com/esmf-org/esmf-profiler/issues/42
        username = _whoami()
        profilepath = _create_directory([tmpdir, username, name])

        # TODO:  https://github.com/esmf-org/esmf-profiler/issues/39
        # copy static site
        git_pull(tmpdir)
        _copy_path(os.path.join(os.getcwd(), "/web/app/build/*"), profilepath)

        # copy json data
        _copy_path(os.path.join(outdir, "/data"), profilepath)

        git_add(profilepath, tmpdir)
        git_commit(username, name, tmpdir)
        git_push(tmpdir)


def _handle_logging(verbosity):
    if verbosity > 0:
        _format = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=_format)
    else:
        _format = "%(name)s : %(message)s"
        logging.basicConfig(level=logging.INFO, format=_format)


def _create_directory(paths):
    _path = os.path.join(*paths)
    os.makedirs(_path, exist_ok=True)
    return _path

def main():
    OUTPUT_DATA_PATH = "data"
    SITE_FILE_NAME = "site.json"
    DATA_FILE_NAME = "load_balance.json"

    # collect user args
    args = _handle_args()

    # setup logging based on args.verbose
    _handle_logging(args.verbose)

    output_data_path = _create_directory([args.outdir, OUTPUT_DATA_PATH])

    # write site.json
    _write_json_to_file(
        {"name": args.name, "timestamp": str(datetime.datetime.now())}, os.path.join(output_data_path, SITE_FILE_NAME)
    )

    # the only requested analysis is a load balance at the root level

    analyses = [LoadBalance(None, output_data_path)]

    logger.info("Processing trace: %s", args.tracedir)
    Trace.from_path(args.tracedir, analyses)
    logger.debug("Processing trace complete")

    # indicate to the analyses that all events have been processed
    logger.info("Generating profile")
    for analysis in analyses:
        data = analysis.finish()
        _write_json_to_file(data, os.path.join(output_data_path, DATA_FILE_NAME))
    logger.debug("Finishing analyses complete")

    if args.push is not None:
        _push_to_repo(
            url=args["push"], outdir=os.path.abspath(args.outdir), name=args["name"]
        )


if __name__ == "__main__":
    main()
