from abc import ABC, abstractproperty
from typing import Generator, List
import bt2
import textwrap
from statistics import mean
import json


class TraceEvent(ABC):
    def __init__(self, msg: bt2._EventMessageConst):
        self._msg = msg

    def __repr__(self):
        return f"<{self.__class__.__name__} {textwrap.shorten(str(self.payload()), width=50)}>"

    def __str__(self):
        """__str__ returns JSON rep of object

        Though already a valid string, passing through 'json.dumps' ensures
        it's valid JSON

        Returns:
            str:
        """
        return self.toJson()

    def toJson(self):
        return json.dumps(self, cls=TraceEventEncoder)

    @abstractproperty
    def keys(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} requires a 'keys' property"
        )

    def get(self, key):
        try:
            if str(key).lower() in self.keys():
                return self.payload()[str(key).lower()]
        except KeyError:
            if key in dir(self):
                return getattr(self, key)()

        raise AttributeError(f"Key '{key}' does not exist on {self.__class__.__name__}")

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


class TraceEventEncoder(json.JSONEncoder):
    casting = [bt2._UnsignedIntegerFieldConst, bt2._DoublePrecisionRealFieldConst]

    def default(self, obj):
        if type(obj) in self.casting:
            return str(obj)
        if isinstance(obj, TraceEvent):
            result = {}
            for key in obj.keys():
                result[key] = obj.get(key)
            return result
        return json.JSONEncoder.default(self, obj)


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
    def __init__(self, msg):
        super().__init__(msg)
        self._children = []

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
            "pet",
            "children",
        ]

    def children(self):
        return self._children


class RegionProfiles:
    def __init__(self, profiles: List[RegionProfile]):
        self._profiles = profiles

    def __iter__(self):
        yield from self._profiles

    def _create_tree(self):
        parentIds = set(
            [
                profile.get("parentId")
                for profile in self._profiles
                if profile.get("parentId") != 0
            ]
        )
        results = []
        for parentId in parentIds:
            parent = list(filter(lambda x: x.get("ID") == parentId, self._profiles))[0]
            children = list(
                filter(lambda x: x.get("parentID") == parentId, self._profiles)
            )
            parent._children = children
            results.append(parent)
        return RegionProfiles(results)


class RegionSummary:
    def __init__(self, region_profiles: List["TraceEvent"]):
        self._profiles = region_profiles
        self._children = {}
        self._pet_count = len(region_profiles)

    def _totals(self):
        # TODO Cache this
        return [profile.get("total") for profile in self._profiles]

    def _count(self):
        # TODO Cache this
        return [profile.get("count") for profile in self._profiles]

    def _pet_ids(self):
        # TODO Cache this
        return [profile.get("pet") for profile in self._profiles]

    def pet_count(self):
        return len(self._profiles)

    def count_each(self):
        return max(self._count())

    def min(self):
        return min(self._totals())

    def max(self):
        return max(self._totals())

    def mean(self):
        return mean(self._totals())

    def min_pet_id(self):
        # QUESTION can't there be multiple id's that share the same value?
        return dict(zip(self._totals(), self._pet_ids()))[self.min()]

    def max_pet_id(self):
        return dict(zip(self._totals(), self._pet_ids()))[self.max()]


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
    def __init__(self, msgs: Generator[TraceEvent, None, None]):
        self._msgs = msgs

    def __iter__(self):
        yield from self._msgs

    def filter(self, fx):
        yield from filter(fx, self._msgs)

    @staticmethod
    # TODO handle errors
    def from_directory(dir: str):
        return Trace(
            (
                TraceEvent.Of(msg)
                for msg in bt2.TraceCollectionMessageIterator(dir)
                if type(msg) is bt2._EventMessageConst
            )
        )
