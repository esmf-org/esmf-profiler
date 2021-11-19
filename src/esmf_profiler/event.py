import textwrap
from abc import ABC, abstractproperty
import bt2
import json


class TraceEvent(ABC):
    def __init__(self, msg: bt2._EventMessageConst):
        self._msg = msg
        self._attributes = {}

    def __repr__(self):
        return f"<{self.__class__.__name__} {textwrap.shorten(str(self.payload), width=50)}>"

    def __str__(self):
        return self.toJSON()

    def toJSON(self):
        return json.dumps(self, cls=TraceEventEncoder)

    @abstractproperty
    def type(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} requires a 'type' property"
        )

    @property
    def keys(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} requires a 'keys' property"
        )

    @property
    def name(self):
        if "name" in self._attributes:
            return self._attributes["name"]
        return ""

    def get(self, key):
        return self._msg.event.payload_field[key]
        #try:
        #    if str(key).lower() in self.keys:
        #        return self.payload[str(key).lower()]
        #except KeyError:
        #    if key in dir(self):
        #        return getattr(self, key)
        #raise AttributeError(f"Key '{key}' does not exist on {self.__class__.__name__}")

    #@property
    #def payload(self):
    #    return self._msg.event.payload_field

    @property
    def pet(self):
        return self._msg.event.packet.context_field["pet"]

    @property
    def nodename(self):
        return self._msg.event.packet.context_field["nodename"]

    @staticmethod
    def Of(msg: bt2._EventMessageConst):
        """Of Convnience constructor

        Args:
            msg (bt2._EventMessageConst):

        Returns:
            Obj:
        """
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
    casting = [
        bt2._UnsignedIntegerFieldConst,
        bt2._DoublePrecisionRealFieldConst,
        bt2._StringFieldConst,
        bt2._UnsignedEnumerationFieldConst,
    ]

    def default(self, obj):
        if type(obj) in self.casting:
            return str(obj)
        if isinstance(obj, TraceEvent):
            result = {}
            for key in obj.keys:
                result[key] = obj.get(key)
            return result
        return json.JSONEncoder.default(self, obj)





class Comp(TraceEvent):
    @property
    def type(self):
        return "comp"

    @property
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
    @property
    def type(self):
        return "regionid_enter"

    @property
    def keys(self):
        return ["regionid"]


class RegionIdExit(TraceEvent):
    @property
    def type(self):
        return "regionid_exit"

    @property
    def keys(self):
        return ["regionid"]


class DefineRegion(TraceEvent):
    @property
    def type(self):
        return "define_region"

    @property
    def keys(self):
        return [
            "name",
            "pet",
            "id",
            "type",
            "vmid",
            "baseid",
            "method",
            "phase",
        ]


class RegionProfile(TraceEvent):
    @property
    def type(self):
        return "region_profile"

    @property
    def keys(self):
        return [
            "id",
            "parentid",
            "total",
            "count",
            "max",
            "min",
            "mean",
            "pet",
            "name",
        ]
