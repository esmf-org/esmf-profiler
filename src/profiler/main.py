import os
from profiler.trace import RegionProfile, RegionSummary, Trace


def main():
    print(os.getcwd())
    trace = Trace.from_directory("./tests/fixtures")
    trace = list(trace.filter(lambda x: isinstance(x, RegionProfile)))
    summary = RegionSummary(trace)
    print(summary.pet_count())
    print(summary.count_each())
    exit()
    for msg in trace:
        print(str(msg))
        print(msg.get("id"))
        print(msg.get("parentid"))
        print(msg.get("par"))
        exit()


if __name__ == "__main__":
    main()
