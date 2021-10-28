
import os
import subprocess
import glob

def _command_safe(cmd, cwd=os.getcwd()):
    return subprocess.run(
        cmd, cwd=cwd, check=True, stdout=subprocess.PIPE, encoding="utf-8"
    )

def git_add(profilepath, repopath):
    cmd = ["git", "add"] + glob.glob(profilepath + "/*")
    return _command_safe(cmd, repopath)


def git_commit(username, name, repopath):
    cmd = ["git", "commit", "-a", "-m", f"'Commit profile {username}/{name}'"]
    return _command_safe(cmd, repopath)


def git_pull(repopath, destination="origin"):
    cmd = ["git", "pull", destination]
    return _command_safe(cmd, repopath)


def git_push(repopath, destination="origin"):
    cmd = ["git", "push", destination]
    return _command_safe(cmd, repopath)


def git_clone(url, tmpdir):
    cmd = ["git", "clone", url, "tmprepo"]
    return _command_safe(cmd, tmpdir)