""" Main point of execution

    Notes:

    * Remove any 'print_execution_time' calls before going to prod
"""


import datetime
import json
import logging
import os
import shutil
import tempfile

from profiler.analyses import LoadBalance
from profiler.git import (
    _command_safe,
    git_add,
    git_commit,
    git_pull,
    git_push,
    git_clone,
)
from profiler.trace import Trace
from profiler.view import handle_args as _handle_args

logger = logging.getLogger(__name__)


def _copy_path(src, dst, symlinks=False, ignore=None):
    """Safe copytree replacement"""
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        try:
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)
        except FileExistsError as _:  # We don't get this flag until Python 3.8
            continue


def _write_json_to_file(data, _path):
    """Dumps json to file"""
    with open(_path, "w", encoding="utf-8") as _file:
        json.dump(data, _file)


def _whoami():
    """Returns the "whoami" command stdout"""
    return _command_safe(["whoami"]).stdout.strip()


def _commit_profile(username, name, repopath=os.getcwd()):
    """git_commit

    Args:
        username (str):
        name (str): name of report to commit
        repopath (str, optional): local repository path if not cwd. Defaults to os.getcwd().

    Returns:
        CompletedProcess:
    """
    return git_commit(f"'Commit profile {username}/{name}'", repopath)


def push_profile_to_repo(input_path, name, url):
    """push_profile_to_repo pushes the generated profile to a remote repository

    A temp directory is created.  The remote repo is cloned into temp.

    The generated report files are copied into the clone repository, added,
    committed with a canned message, and push to the remote repository.

    Args:
        input_path (str): location of the generated profile
        name (str): name of the profile
        url (str): repository url
    """
    with tempfile.TemporaryDirectory() as _temp:
        # TODO: https://github.com/esmf-org/esmf-profiler/issues/42
        username = _whoami()
        git_clone(url, _temp)

        profilepath = _create_directory([_temp, username, name])

        # TODO:  https://github.com/esmf-org/esmf-profiler/issues/39
        git_pull(_temp)

        # copy json data
        _copy_path(input_path, profilepath)

        git_add(profilepath, _temp)
        _commit_profile(username, name, _temp)
        git_push(_temp)


def handle_logging(verbosity=0):
    """handle_logging sets up logging based on a verbosity level

    Args:
        verbosity (int, optional): Defaults to 0 (INFO).
    """
    if verbosity > 0:
        _format = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=_format)
    else:
        _format = "%(name)s : %(message)s"
        logging.basicConfig(level=logging.INFO, format=_format)


def safe_create_directory(paths):
    """safe_create_directory creates a nested directory top-down in order
    of array.

    Args:
        paths (str, [str]): directory to create, with paths[0] being root and so on.

    Returns:
        str: path to the created directory
    """
    _path = os.path.join(*paths)
    os.makedirs(_path, exist_ok=True)
    return _path


def copy_gui_template(output_path, input_path="./web/app/build", _ignore="/data"):
    """copy_gui_template copies the Web GUI template files

    Ignores any existing /data file in input_path

    Args:
        output_path (str):
        input_path (str, optional): Defaults to "./web/app/build".
        _ignore (str || [str] , optional): Patterns to ignore. Defaults to "/data".

    Raises:
        FileNotFoundError: if input_path not found
    """


def create_site_file(name, output_path, site_file_name="site.json"):
    """create_site_file creates a json file containing site information

    Args:
        name (str): name to give to the site
        output_path (str): path
        site_file_name (str, optional): The file name. Defaults to "site.json".
    """
    _write_json_to_file(
        {"name": name, "timestamp": str(datetime.datetime.now())},
        os.path.join(output_path, site_file_name),
    )


def run_analsysis(output_path, tracedir, data_file_name):
    """run_analsysis runs an analysis on a directory containing binary traces files and outputs
    the results to data_file_name

    Args:
        output_path (str): path
        tracedir (str): path containing the binary traces
        data_file_name (str): name to give the output file
    """
    # the only requested analysis is a load balance at the root level
    analyses = [LoadBalance(None, output_path)]

    logger.info("Processing trace: %s", tracedir)
    Trace.from_path(tracedir, analyses)
    logger.debug("Processing trace complete")

    # indicate to the analyses that all events have been processed
    logger.info("Generating %s profiles", len(analyses))
    for analysis in analyses:
        data = analysis.finish()
        _write_json_to_file(data, os.path.join(output_path, data_file_name))
    logger.debug("Finishing analyses complete")


def main():
    """main execution"""

    SITE_FILE_NAME = "site.json"
    DATA_FILE_NAME = "load_balance.json"

    # collect user args
    args = _handle_args()

    # setup logging based on args.verbose
    handle_logging(args.verbose)

    output_path = safe_create_directory([args.outdir])
    output_data_path = safe_create_directory([output_path, "data"])

    # write site.json
    create_site_file(args.name, output_data_path, SITE_FILE_NAME)

    # the only requested analysis is a load balance at the root level
    run_analsysis(output_data_path, args.tracedir, DATA_FILE_NAME)

    # inject web gui files
    copy_gui_template(output_path)

    if args.push is not None:
        push_profile_to_repo(input_path=output_path, name=args.name, url=args.push)


if __name__ == "__main__":
    main()
