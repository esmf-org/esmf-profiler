""" CLI View Layer

author: Ryan Long <ryan.long@noaa.gov>

```python
args = handle_args()
args.name // access args as named properties
```

"""
import argparse
import os


def _alphanumberic(value):
    if not value.isalnum():
        raise ValueError(
            f"name argument must contain only letters and numbers: {value}"
        )
    return value


def _directory(value):
    if not os.path.isdir(value):
        raise ValueError(f"{os.path.isdir} is not a valid directory")
    return value


def handle_args():
    """handle_args returns an object whose properties correspond to named arguments

    ```python
    args = handle_args()
    args.name // access args as named properties
    ```

    Returns:
        object: property accessor
    """
    parser = argparse.ArgumentParser(description="ESMF Profiler")
    parser.add_argument(
        "-t",
        "--tracedir",
        help="directory containing the ESMF trace",
        type=_directory,
        required=True,
    )
    parser.add_argument(
        "-n",
        "--name",
        help="name to use for the generated profile",
        required=True,
        type=_alphanumberic,
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
    parser.add_argument(
        "-s",
        "--serve",
        help="start a local server to host the profile results",
        action="store_true",
    )
    parser.add_argument(
        "-x",
        "--xopts",
        help="extra options to customize the behavior of the profiler",
        required=False,
    )

    return parser.parse_args()
