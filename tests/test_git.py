from unittest import mock
import subprocess

from esmf_profiler import git
import pytest


@mock.patch("subprocess.run")
def testCommandSafe_whenRaisesExceptionWithNoStdErr_noExceptionRaised(subprocess_mock):
    exception = subprocess.CalledProcessError(returncode=1, cmd="")
    subprocess_mock.side_effect = exception

    git._command_safe("fake command")
    assert subprocess_mock.called


@mock.patch("subprocess.run")
def testCommandSafe_whenRaisesExceptionWithStdErr_RaisesException(subprocess_mock):
    exception = subprocess.CalledProcessError(returncode=1, cmd="", stderr="error")
    subprocess_mock.side_effect = exception

    with pytest.raises(subprocess.CalledProcessError):
        git._command_safe("fake command")

        assert subprocess_mock.called
