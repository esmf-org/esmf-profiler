# type: ignore
"""
Tests
"""

import os
import glob
import tempfile
import pytest

from esmf_profiler.main import (
    create_site_file,
    run_analsysis,
    safe_create_directory,
    copy_gui_template,
)


def test_createSiteFile_createsSiteFileCorrectly():
    with tempfile.TemporaryDirectory() as _temp:
        create_site_file("test", _temp, "site.json")

        file_path = os.path.join(_temp, "site.json")
        assert os.path.exists(file_path)

        with open(file_path, "r") as _file:
            contents = _file.read()
            assert "name" in contents
            assert "test" in contents
            assert "timestamp" in contents


def test_runAnalysis_givesTheCorrectOutput():
    with tempfile.TemporaryDirectory() as _temp:
        run_analsysis(_temp, "tests/fixtures/test-traces", "load_balance.json")

        file_path = os.path.join(_temp, "load_balance.json")
        assert os.path.exists(file_path)

        with open(file_path, "r") as _file:
            with open("tests/fixtures/test-traces/expected.json") as _expected:
                contents = _file.read()
                expected = _expected.read()

                assert contents == expected


def test_safeCreateDirectory_givenValidInputs_createsDirectory():
    with tempfile.TemporaryDirectory() as _temp:
        safe_create_directory([_temp, "test"])
        assert os.path.exists(os.path.join(_temp, "test"))


def test_safeCreateDirectory_givenMultipleValidInputs_createsDirectory():
    with tempfile.TemporaryDirectory() as _temp:
        safe_create_directory([_temp, "testA", "testB", "testC"])
        assert os.path.exists(os.path.join(_temp, "testA", "testB", "testC"))


def test_copyGuiTemplate_withValidInputs_copiesCorrectFiles():
    with tempfile.TemporaryDirectory() as _temp:
        copy_gui_template(_temp, "tests/fixtures/test_build")
        actual = len(glob.glob(os.path.join(_temp, "*")))
        expected = 9  # 9 files and dirs total returned
        assert actual == expected


def test_copyGuiTemplate_whenGivenInvalidInput_RaisesException():
    with pytest.raises(FileNotFoundError):
        with tempfile.TemporaryDirectory() as _temp:
            copy_gui_template(_temp, "bad_path_doesnt_exist_xajahsywe")


if __name__ == "__main__":
    pass
