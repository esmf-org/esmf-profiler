""" CLI View Layer

author: Ryan Long <ryan.long@noaa.gov>

```python
args = handle_args()
args.name // access args as named properties
```

"""
import argparse
import os
import re


def _allowed_chars(value):
    search_regex = re.compile(r"^[\w\-. ]+$")
    if not bool(search_regex.search(value)):
        raise ValueError(f"{value} contains invalid characters.")
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
        type=_allowed_chars,
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

    return parser.parse_args()
