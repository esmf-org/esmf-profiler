import tempfile

from profiler.main import create_site_file
import os


def test_injectReportTemplate_injectsReportTemplate():
    with tempfile.TemporaryDirectory() as _temp:
        create_site_file("test", _temp, "site.json")

        file_path = os.path.join(_temp, "site.json")
        assert os.path.exists(file_path)

        contents = open(file_path, "r").read()
        assert "name" in contents
        assert "test" in contents
        assert "timestamp" in contents


if __name__ == "__main__":
    pass
