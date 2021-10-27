import argparse
import os


def alphanumberic(value):
    if not value.isalnum():
        raise ValueError(
            f"name argument must contain only letters and numbers: {value}"
        )
    return value


def directory(value):
    if not os.path.isdir(value):
        raise ValueError(f"{os.path.isdir} is not a valid directory")
    return value


def handle_args():
    parser = argparse.ArgumentParser(description="ESMF Profiler")
    parser.add_argument(
        "-t",
        "--tracedir",
        help="directory containing the ESMF trace",
        type=directory,
        required=True,
    )
    parser.add_argument(
        "-n",
        "--name",
        help="name to use for the generated profile",
        required=True,
        type=alphanumberic,
    )
    parser.add_argument(
        "-o", "--outdir", help="path to output directory", required=True
    )
    parser.add_argument(
        "-p",
        "--push",
        help="git url of remote repository where to push profile",
        required=False,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="enable verbose output",
        action="count",
        default=0,
    )

    return parser.parse_args()
