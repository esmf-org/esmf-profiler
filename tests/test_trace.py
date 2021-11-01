"""
Tests
"""

import os
import tempfile

from profiler.main import create_site_file, run_analsysis


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


if __name__ == "__main__":
    pass
