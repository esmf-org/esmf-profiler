""" Main point of execution

"""

import datetime
import json
import logging
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import webbrowser
from subprocess import PIPE

from esmf_profiler import git
from esmf_profiler.analyses import LoadBalance, Analysis
from esmf_profiler.trace import Trace
from esmf_profiler.view import handle_args

import time

# import cProfile, pstats
# from pycallgraph import PyCallGraph
# from pycallgraph.output import GraphvizOutput

logger = logging.getLogger(__name__)


def _copy_path(src, dst, ignore=[]):  # pylint: disable=dangerous-default-value
    """Safe copytree replacement"""
    for src_dir, _, files in os.walk(src):
        dst_dir = src_dir.replace(src, dst, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            if file_ in ignore:
                continue
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                # in case of the src and dst are the same file
                if os.path.samefile(src_file, dst_file):
                    continue
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)


def _write_json_to_file(data, _path):
    """Dumps json to file"""
    with open(_path, "w", encoding="utf-8") as _file:
        json.dump(data, _file)
    if not os.path.exists(_path):
        raise FileNotFoundError(f"failed to write output to {_path}")


def _whoami():
    """Returns the "whoami" command stdout"""
    # TODO _command_safe should be copy/paste to eliminate the dependency
    return git._command_safe(["whoami"]).stdout.strip()


def _start_server(build_path, url="localhost:8000"):
    logger.info("Starting local server port 8000 (CTRL+C to close)")
    subprocess.call(
        ["python", "-m", "http.server", "--directory", build_path],
        stdout=PIPE,
        stderr=PIPE,
    )


def _commit_profile(username, name, repopath=os.getcwd()):
    """git_commit

    Args:
        username (str):
        name (str): name of report to commit
        repopath (str, optional): local repository path if not cwd. Defaults to os.getcwd().

    Returns:
        CompletedProcess:
    """
    return git.commit(f"'Commit profilee {username}/{name}'", repopath)


def push_profile_to_repo(input_path, name, url):
    """push_profile_to_repo pushes the generated profile to a remote repository

    A temp directory is created.  The remote repo is cloned into temp.

    The generated report files are copied into the clone repository, added,
    committed with a canned message, and push to the remote repository.

    We should be running `pull` after `clone` based on this answer for now:
    https://stackoverflow.com/questions/55941908/do-i-have-to-run-git-pull-after-git-clone

    #TODO: https://github.com/esmf-org/esmf-profiler/issues/42

    Args:
        input_path (str): location of the generated profile
        name (str): name of the profile
        url (str): repository url
    """
    with tempfile.TemporaryDirectory() as _temp:
        git.clone(url, _temp)

        username = _whoami()
        profilepath = safe_create_directory([_temp, username, name])
        logger.debug(
            "push_profile_to_repo: input_path: %s  profilepath: %s _temp: %s url: %s",
            input_path,
            profilepath,
            _temp,
            url,
        )

        _copy_path(input_path, profilepath)

        git.add(_temp)
        logger.debug(git.status(_temp).stdout)
        _commit_profile(username, name, _temp)
        git.push(url, _temp)


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


def copy_gui_template(  # pylint: disable=dangerous-default-value
    output_path, input_path="./web/app/build", _ignore=["site.json", "load_balance.json"]
):
    """copy_gui_template copies the Web GUI template files

    Ignores any existing /data file in input_path

    Args:
        output_path (str):
        input_path (str, optional): Defaults to "./web/app/build".
        _ignore (str || [str] , optional): Patterns to ignore.

    Raises:
        FileNotFoundError: if input_path not found
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError()
    _copy_path(input_path, output_path, ignore=_ignore)


def create_site_file(name, output_path, site_file_name="site.json"):
    """create_site_file creates a json file containing site information

    Args:
        name (str): name to give to the site
        output_path (str): path
        site_file_name (str, optional): The file name. Defaults to "site.json".

    Returns:
        str: the path of the created site file
    """
    output_file_path = os.path.join(output_path, site_file_name)
    _write_json_to_file(
        {"name": name, "timestamp": str(datetime.datetime.now())},
        output_file_path,
    )
    return output_file_path


def run_analysis(output_path, tracedir, data_file_name, xopts=None):
    """run_analysis runs an analysis on a directory containing binary traces files and outputs
    the results to data_file_name

    Args:
        output_path (str): path
        tracedir (str): path containing the binary traces
        data_file_name (str): name to give the output file
        xopts (dict): extra options from the user to customize behavior

    Returns:
        str: path off the output file
    """

    chunksize = Trace.DEFAULT_CHUNK_SIZE
    analysis_threads = Analysis.DEFAULT_NUM_THREADS
    if xopts is not None:
        if "chunksize" in xopts:
            try:
                chunksize = int(xopts["chunksize"])
                logger.info(f"Using custom chunksize of {chunksize}")
            except ValueError:
                logger.info(
                    f"Invalid chunksize: {xopts['chunksize']} - using default value of {chunksize}"
                )
        if "analysis_threads" in xopts:
            try:
                analysis_threads = int(xopts["analysis_threads"])
                logger.info(f"Using custom analysis_threads of {analysis_threads}")
            except ValueError:
                logger.info(
                    f"Invalid analysis_threads: {xopts['analysis_threads']} - using default value of {analysis_threads}"
                )

    # for now, the only supported analysis is load balance
    analyses = [LoadBalance(num_threads=analysis_threads)]
    # profiler = cProfile.Profile()

    logger.info("Processing trace: %s", tracedir)

    start = time.time()
    # profiler.enable()
    # with PyCallGraph(output=GraphvizOutput()):

    Trace.from_path(tracedir, analyses=analyses, chunksize=chunksize)

    # indicate to the analyses that all events have been processed
    logger.info("Generating profile")
    output_file_path = os.path.join(output_path, data_file_name)
    for analysis in analyses:
        data = analysis.finish()
        _write_json_to_file(data, output_file_path)
    logger.debug("Finishing analyses complete")

    # profiler.disable()

    end = time.time()
    logger.info(f"Trace processing time: {round(end - start, 2)}s")

    # stats = pstats.Stats(profiler).sort_stats('tottime')
    # stats.print_stats()

    return output_file_path


def main():
    """main execution"""

    def signal_handler(sig, frame):  # pylint: disable=unused-argument
        logger.info("Closing local server")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    SITE_FILE_NAME = "site.json"  # pylint: disable=invalid-name
    DATA_FILE_NAME = "load_balance.json"  # pylint: disable=invalid-name

    # collect user args
    args = handle_args()

    # setup logging based on args.verbose
    handle_logging(args.verbose)

    # TODO: this section should probably be in handle_args()
    xopts = None
    if args.xopts is not None:
        # format:  key1=value1:key2=value2:key3=value3
        try:
            xopts = dict(x.split("=") for x in args.xopts.split(":"))
        except ValueError:
            logger.error("Incorrect format for -x/--xopts command line argument")
            return

    output_path = safe_create_directory([args.outdir])
    output_data_path = safe_create_directory([output_path, "data"])

    # write site.json
    create_site_file(args.name, output_data_path, SITE_FILE_NAME)

    # the only requested analysis is a load balance at the root level
    run_analysis(output_data_path, args.tracedir, DATA_FILE_NAME, xopts)

    # inject web gui files
    copy_gui_template(output_path)

    if args.push is not None:
        logger.info(f"Pushing profile in {output_path} to {args.push}")
        push_profile_to_repo(input_path=output_path, name=args.name, url=args.push)

    if args.serve:
        _start_server(output_path)


if __name__ == "__main__":
    main()
