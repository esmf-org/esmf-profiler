from abc import ABC, abstractclassmethod, abstractmethod, abstractproperty
import abc
from typing import Any, cast
import bt2
import json

import os.path
import pprint
import unittest


import regiontree
from datetime import datetime
import textwrap


@bt2.plugin_component_class
class MultiPETTimingSummary(bt2._UserSinkComponent):
    def __init__(self, config, params, obj):
        self._port = self._add_input_port("in")
        self._region_maps = {}  # per-PET maps of region id to region name
        self._region_roots = {}  # per-PET region timing trees
        self._region_summary = regiontree.RegionSummary()
        self._stream_count = 0
        self._tmp_count = 0

        if "name" not in params:
            raise Exception("Missing required parameter: name")
        self._name = str(params["name"])

        if "output_path" not in params:
            raise Exception("Missing required parameter: output_path")

        self._output_path = str(params["output_path"])
        if not os.path.isdir(self._output_path):
            os.makedirs(self._output_path)

        # print("MultiPETTimingSummary init")

    def _user_graph_is_configured(self):
        self._it = self._create_message_iterator(self._port)
        print("DONE _user_graph_is_configured")

    def _user_consume(self):
        msg = next(self._it)

        self._tmp_count += 1
        if self._tmp_count % 10000 == 0:
            print("Processed {} records".format(self._tmp_count))

        if type(msg) is bt2._EventMessageConst:

            if msg.event.name == "define_region":
                pet = msg.event.packet.context_field["pet"]
                regid = msg.event.payload_field["id"]
                regname = msg.event.payload_field["name"]
                self._region_maps.setdefault(pet, {})[regid] = regname

            elif msg.event.name == "region_profile":
                pet = msg.event.packet.context_field["pet"]
                root = self._region_roots.setdefault(pet, regiontree.RegionNode(0))
                root.pet = pet

                e = msg.event
                node = regiontree.RegionNode(e.payload_field["id"])
                node.pet = pet
                node.count = e.payload_field["count"]
                node.total = e.payload_field["total"]
                node.max = e.payload_field["max"]
                node.min = e.payload_field["min"]
                node.mean = e.payload_field["mean"]
                node.name = self._region_maps[pet].get(node.local_id, "Unknown")

                if not root.add_to_tree(node, e.payload_field["parentid"]):
                    raise Exception(
                        "Error adding timed region tree: " + str(node.local_id)
                    )

            # else:
            #    print("Msg event name = {}".format(msg.event.name))

        elif type(msg) is bt2._StreamBeginningMessageConst:
            self._stream_count = self._stream_count + 1
        elif type(msg) is bt2._StreamEndMessageConst:
            self._stream_count = self._stream_count - 1
            if self._stream_count == 0:
                self._finish()

    def _finish(self):

        print("ENTER _finish")
        for pet, root in self._region_roots.items():
            self._region_summary.merge(root)

        print("Region Summary")
        pprint.pprint(self._region_summary)

        self._generate_html()

    def _generate_html(self):

        print("ENTER _generate_html")

        jenv = jinja2.Environment(
            loader=jinja2.FileSystemLoader("templates"),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        template = jenv.get_template("index.html.jinja")
        html = template.render(
            name=self._name, now=datetime.now(), region_summary=self._region_summary
        )

        with open("{}/{}".format(self._output_path, "index.html"), "w") as fh:
            fh.write(html)
        print("Generated file: {}/index.html".format(self._output_path))

        template = jenv.get_template("loadbalance.html.jinja")
        html = template.render(
            name=self._name, now=datetime.now(), region_summary=self._region_summary
        )

        with open("{}/{}".format(self._output_path, "loadbalance.html"), "w") as fh:
            fh.write(html)
        print("Generated file: {}/loadbalance.html".format(self._output_path))


def process_trace(tracepath: str):
    ctf_plugin = bt2.find_plugin("ctf")
    utils_plugin = bt2.find_plugin("utils")
    # text_plugin = bt2.find_plugin("text")

    g = bt2.Graph()
    source = g.add_component(
        ctf_plugin.source_component_classes["fs"],
        "source",
        params={"inputs": [tracepath]},
    )

    muxer = g.add_component(utils_plugin.filter_component_classes["muxer"], "muxer")

    for idx, oport in enumerate(source.output_ports):
        g.connect_ports(source.output_ports[oport], muxer.input_ports["in" + str(idx)])

    # sink = g.add_component(text_plugin.sink_component_classes["pretty"], "sink")

    sink = g.add_component(
        MultiPETTimingSummary,
        "sink",
        params={"output_path": "htmlout", "name": "mytrace"},
    )

    g.connect_ports(muxer.output_ports["out"], sink.input_ports["in"])

    g.run()


class ProcessTraceUnitTest(unittest.TestCase):
    def test_read_trace(self):
        process_trace("./test-traces/atm-ocn")
        # process_trace("./test-traces/cpld_bmark_wave_v16")


class TraceEvent(abc.ABC):
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
        print(event_type)
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
    @staticmethod
    def from_directory(dir: str):
        return [
            TraceEvent.Of(msg)
            for msg in bt2.TraceCollectionMessageIterator("./test-traces")
            if type(msg) is bt2._EventMessageConst
        ]


def main():
    trace = Trace.from_directory("./test-traces")
    for msg in trace:
        print(msg)


if __name__ == "__main__":
    main()
