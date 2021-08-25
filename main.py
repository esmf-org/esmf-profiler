from abc import ABC, abstractproperty
from typing import List
import bt2
import textwrap


class TraceEvent(ABC):
    def __init__(self, msg: bt2._EventMessageConst):
        self._msg = msg

    def __repr__(self):
        return f"<{self.__class__.__name__} {textwrap.shorten(str(self.payload()), width=50)}>"

    def __str__(self):
        payload = str(dict(zip(self.payload().keys(), self.payload().values())))
        return f"{self.__class__.__name__}[PET_{self.pet()}]{payload}"

    @abstractproperty
    def keys(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} requires a 'keys' property"
        )

    def get(self, key):
        if str(key).lower() in self.keys():
            return self.payload()[str(key).lower()]
        raise AttributeError(f"{key} does not exist on {self.__class__.__name__}")

    def payload(self):
        return self._msg.event.payload_field

    def pet(self):
        return self._msg.event.packet.context_field["pet"]

    @staticmethod
    def Of(msg: bt2._EventMessageConst):
        event_type = msg.event.name
        __map = {
            "define_region": lambda msg: DefineRegion(msg),
            "regionid_enter": lambda msg: RegionIdEnter(msg),
            "regionid_exit": lambda msg: RegionIdExit(msg),
            "region_profile": lambda msg: RegionProfile(msg),
            "comp": lambda msg: Comp(msg),
        }

        return __map[event_type](msg)


class Comp(TraceEvent):
    def keys(self):
        return [
            "vmid",
            "baseid",
            "name",
            "IPM",
            "RPM",
            "FPM",
        ]


class RegionIdEnter(TraceEvent):
    def keys(self):
        return ["regionid"]


class RegionIdExit(TraceEvent):
    def keys(self):
        return ["regionid"]


class RegionProfile(TraceEvent):
    def keys(self):
        return [
            "id",
            "parentid",
            "total",
            "self",
            "count",
            "max",
            "min",
            "mean",
            "stdev",
        ]


class DefineRegion(TraceEvent):
    def keys(self):
        return [
            "nodename",
            "pet",
            "id",
            "type",
            "vmid",
            "baseid",
            "method",
            "phase",
        ]


class Trace:
    def __init__(self, msgs: List[TraceEvent]):
        self._msgs = msgs

    def __iter__(self):
        yield from self._msgs

    def filter(self, instance_name):
        return filter(lambda x: isinstance(x, instance_name), self._msgs)

    @staticmethod
    def from_directory(dir: str):
        msgs = [
            TraceEvent.Of(msg)
            for msg in bt2.TraceCollectionMessageIterator("./test-traces")
            if type(msg) is bt2._EventMessageConst
        ]
        return Trace(list(msgs))


def main():
    trace = Trace.from_directory("./test-traces")
    trace = trace.filter(RegionProfile)
    for msg in trace:
        print(msg)


if __name__ == "__main__":
    main()
