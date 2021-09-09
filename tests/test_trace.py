from profiler.trace import Trace


def testTrace_whenInstantiatedFromDirectory_IsCorrect():
    trace = Trace.from_path("./tests/fixtures", [], [])
    assert trace.__class__.__name__ == "Trace"

    _trace = trace
    msg = next(iter(_trace))

    assert (
        str(msg)
        == "Comp[PET_1]{'vmid': 0, 'baseid': 0, 'name': 'esm', 'IPM': 'IPDv02p1=2||IPDv02p3=3||IPDv02p5=4||ExternalAdvertise=5||ExternalRealize=6||ExternalDataInitialize=7', 'RPM': 'RunPhase1=1', 'FPM': 'FinalizePhase1=1||ExternalFinalizeReset=2'}"
    )

    print(msg)

    # trace = list(trace.filter(lambda x: isinstance(x, RegionProfile)))
    # summary = RegionSummary(trace)
    # print(summary.pet_count())
    # print(summary.count_each())

    for msg in trace:
        print(str(msg))
        print(msg.get("id"))
        print(msg.get("parentid"))
        print(msg.get("par"))
        exit()
