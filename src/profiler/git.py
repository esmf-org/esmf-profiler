"""
Git commands module
author: Ryan Long <ryan.long@noaa.gov>
"""

import glob
import os
import subprocess


def _command_safe(cmd, cwd=os.getcwd()):
    """_command_safe ensures commands are run safely and raise exceptions
    on error
    """
    try:
        return subprocess.run(
            cmd, cwd=cwd, check=True, stdout=subprocess.PIPE, encoding="utf-8"
        )
    except Exception as e:
        print(f"Subprocess error: {e}")


def git_add(profilepath, repopath=os.getcwd()):
    cmd = ["git", "add"] + glob.glob(profilepath + "/*")
    return _command_safe(cmd, repopath)


def git_commit(username, name, repopath=os.getcwd()):
    cmd = ["git", "commit", "-a", "-m", f"'Commit profile {username}/{name}'"]
    return _command_safe(cmd, repopath)


def git_pull(repopath=os.getcwd(), destination="origin"):
    cmd = ["git", "pull", destination]
    return _command_safe(cmd, repopath)


def git_push(repopath=os.getcwd(), destination="origin"):
    cmd = ["git", "push", destination]
    return _command_safe(cmd, repopath)


def git_clone(url, tmpdir):
    cmd = ["git", "clone", url, tmpdir]
    return _command_safe(cmd, tmpdir)
