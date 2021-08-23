import re

class DataPoint:

    PATTERN = r'(^\[.*\]).*(\(.*\)).*(\{.*\})$'

    def __init__(self, data: str):
        self._data = data
        self._timestamp = None
        self._elapsed = None
        self._type = None
        self._stats = None

    def timestamp(self):
        if self._timestamp is None:
            self._timestamp = re.search(PATTERN, line)[1][1:-1]
        return self._timestamp

    def elapsed(self):
        if self._elapsed is None:
            self._elapsed = re.search(PATTERN, line)[2]
        return self._elapsed

    def stats(self):
        if self._elapsed is None:
            self._elapsed = re.search(PATTERN, line)[3]
        return self._elapsed

class Stats:
    def __init__(self, data: str):
        self._data = data

    


def main():
    with open('./sample_trace_output.txt') as _file:
        for line in _file:
            point = DataPoint(line)
            print(line)

if __name__ == "__main__":
    main()
