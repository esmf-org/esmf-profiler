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
    run_analysis,
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


def _files_match(compare, expected):

    with open(compare) as _c:
        _clines = _c.readlines()
        _clines = [l.strip() for l in _clines]

    with open(expected) as _e:
        _elines = _e.readlines()
        _elines = [l.strip() for l in _elines]

    i = 0
    for l1, l2 in zip(_clines, _elines):
        i += 1
        if not l1 == l2:
            print(f"\nFailed to match line: {i}\n")
            print(f"\tFile1 {compare} line: ", l1, end='\n')
            print(f"\tFile2 {expected} line: ", l2, end='\n')
            return False

    return True


def test_runAnalysis_givesTheCorrectOutput():
    with tempfile.TemporaryDirectory() as _temp:
        run_analysis(_temp, "tests/fixtures/test-traces/atm-ocn", "load_balance.json")

        file_path = os.path.join(_temp, "load_balance.json")
        assert os.path.exists(file_path)
        assert _files_match(file_path, "tests/fixtures/expected/atm-ocn/load_balance.json")

def test_runAnalysis_chunksize():
    with tempfile.TemporaryDirectory() as _t1:
        with tempfile.TemporaryDirectory() as _t2:

            run_analysis(_t1, "tests/fixtures/test-traces/atm-ocn-concurrent", "load_balance.json", xopts={"chunksize" : 2})
            _f1 = os.path.join(_t1, "load_balance.json")
            assert os.path.exists(_f1)

            run_analysis(_t2, "tests/fixtures/test-traces/atm-ocn-concurrent", "load_balance.json", xopts={"chunksize" : 5})
            _f2 = os.path.join(_t2, "load_balance.json")
            assert os.path.exists(_f2)

            assert _files_match(_f1, _f2)

def test_runAnalysis_threads():
    with tempfile.TemporaryDirectory() as _t1:
        with tempfile.TemporaryDirectory() as _t2:

            run_analysis(_t1, "tests/fixtures/test-traces/atm-ocn-concurrent", "load_balance.json", xopts={"analysis_threads" : 1})
            _f1 = os.path.join(_t1, "load_balance.json")
            assert os.path.exists(_f1)

            run_analysis(_t2, "tests/fixtures/test-traces/atm-ocn-concurrent", "load_balance.json", xopts={"analysis_threads" : 3})
            _f2 = os.path.join(_t2, "load_balance.json")
            assert os.path.exists(_f2)

            assert _files_match(_f1, _f2)

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
