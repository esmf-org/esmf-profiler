import os.path
import bt2
import pprint
import unittest
import regiontree
import jinja2
from datetime import datetime

#
# Processes a single stream in the trace.  A stream
# corresponds to one ESMF PET.  Currently this only
# considers two types of events:
#
# - 'define_region'  -- maps an id to a timed region name
# - 'region_profile' -- timing statistics for a region 
#
# All other event types are ignored.
#
# @bt2.plugin_component_class
# class SinglePETSink(bt2._UserSinkComponent):
#
#     def __init__(self, config, params, obj: regiontree.RegionSummary):
#         self._port = self._add_input_port("in")
#         self._region_map = {}
#         self._my_stream = str(params["stream"])
#         self._timing_summary = obj
#         self._pet = int(self._my_stream[-4:])  # assumes last 4 is PET number
#         self._root_region = regiontree.RegionNode(0)
#         self._root_region.name = "ROOT"
#         self._region_summary = obj
#         print("SinglePETSink for stream: {}".format(params["stream"]))
#
#     def _user_graph_is_configured(self):
#         self._it = self._create_message_iterator(self._port)
#
#     def _user_consume(self):
#         msg = next(self._it)
#
#         if type(msg) is bt2._EventMessageConst:
#
#             if msg.event.name == 'define_region':
#                 regid = msg.event.payload_field["id"]
#                 regname = msg.event.payload_field["name"]
#                 self._region_map[regid] = regname
#
#             if msg.event.name == 'region_profile':
#                 regid = msg.event.payload_field["id"]
#                 regpid = msg.event.payload_field["parentid"]
#                 rn = regiontree.RegionNode(regid)
#                 rn.pet = self._pet
#                 rn.name = self._region_map.get(regid, "ROOT")
#                 rn.total = msg.event.payload_field["total"]
#                 rn.min = msg.event.payload_field["min"]
#                 rn.max = msg.event.payload_field["max"]
#                 rn.mean = msg.event.payload_field["mean"]
#                 rn.count = msg.event.payload_field["count"]
#
#                 added = self._root_region.add_to_tree(rn, regpid)
#                 if not added:
#                     raise Exception("region not added to tree: " + str(regpid))
#
#         elif type(msg) is bt2._StreamEndMessageConst:
#             self._finish()
#
#     def _finish(self):
#
#         print("FINISHED STREAM: " + str(self._pet))
#
#         self._region_summary.merge(self._root_region)


@bt2.plugin_component_class
class MultiPETTimingSummary(bt2._UserSinkComponent):

    def __init__(self, config, params, obj):
        self._port = self._add_input_port("in")
        self._region_maps = {}   # per-PET maps of region id to region name
        self._region_roots = {}  # per-PET region timing trees
        self._region_summary = regiontree.RegionSummary()
        self._stream_count = 0

        if "name" not in params:
            raise Exception("Missing required parameter: name")
        self._name = str(params["name"])

        if "output_path" not in params:
            raise Exception("Missing required parameter: output_path")

        self._output_path = str(params["output_path"])
        if not os.path.isdir(self._output_path):
            os.makedirs(self._output_path)

        #print("MultiPETTimingSummary init")

    def _user_graph_is_configured(self):
        self._it = self._create_message_iterator(self._port)

    def _user_consume(self):
        msg = next(self._it)

        if type(msg) is bt2._EventMessageConst:

            if msg.event.name == 'define_region':
                pet = msg.event.packet.context_field["pet"]
                regid = msg.event.payload_field["id"]
                regname = msg.event.payload_field["name"]
                self._region_maps.setdefault(pet, {})[regid] = regname

            if msg.event.name == 'region_profile':
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
                    raise Exception("Error adding timed region tree: " + str(node.local_id))

        elif type(msg) is bt2._StreamBeginningMessageConst:
            self._stream_count = self._stream_count + 1
        elif type(msg) is bt2._StreamEndMessageConst:
            self._stream_count = self._stream_count - 1
            if self._stream_count == 0:
                self._finish()

    def _finish(self):

        for pet, root in self._region_roots.items():
            self._region_summary.merge(root)

        print("Region Summary")
        pprint.pprint(self._region_summary)

        self._generate_html()

    def _generate_html(self):

        jenv = jinja2.Environment(
            loader=jinja2.FileSystemLoader('templates'),
            trim_blocks=True,
            lstrip_blocks=True
        )

        template = jenv.get_template("index.html.jinja")
        html = template.render(name=self._name,
                               now=datetime.now(),
                               region_summary=self._region_summary)

        with open("{}/{}".format(self._output_path, "index.html"), "w") as fh:
            fh.write(html)
        print("Generated file: {}/index.html".format(self._output_path))


        template = jenv.get_template("loadbalance.html.jinja")
        html = template.render(name=self._name,
                               now=datetime.now(),
                               region_summary=self._region_summary)

        with open("{}/{}".format(self._output_path, "loadbalance.html"), "w") as fh:
            fh.write(html)
        print("Generated file: {}/loadbalance.html".format(self._output_path))


#
# Open and read a trace in CTF format output
# from ESMF.
#
# tracepath -- path to directory containing the trace
#
# def process_trace(tracepath: str):
#
#     ctf_plugin = bt2.find_plugin("ctf")
#
#     g = bt2.Graph()
#     source = g.add_component(ctf_plugin.source_component_classes["fs"],
#                          "source",
#                          params={"inputs":[tracepath]})
#
#     regionsummary = regiontree.RegionSummary()
#
#     sinks = {}
#     for idx, op in enumerate(source.output_ports):
#         sink = g.add_component(SinglePETSink, "sink" + str(idx), params={"stream": str(op)}, obj=regionsummary)
#         g.connect_ports(source.output_ports[op], sink.input_ports["in"])
#         sinks[idx] = sink
#
#     g.run()
#
#     pprint.pprint(regionsummary)
#     return regionsummary


def process_trace(tracepath: str):
    ctf_plugin = bt2.find_plugin("ctf")
    utils_plugin = bt2.find_plugin("utils")
    #text_plugin = bt2.find_plugin("text")

    g = bt2.Graph()
    source = g.add_component(ctf_plugin.source_component_classes["fs"],
                             "source",
                             params={"inputs": [tracepath]})

    muxer = g.add_component(utils_plugin.filter_component_classes["muxer"], "muxer")

    for idx, oport in enumerate(source.output_ports):
        g.connect_ports(source.output_ports[oport], muxer.input_ports["in"+str(idx)])

    #sink = g.add_component(text_plugin.sink_component_classes["pretty"], "sink")

    sink = g.add_component(MultiPETTimingSummary, "sink",
                           params={"output_path": "htmlout",
                                   "name": "mytrace"})

    g.connect_ports(muxer.output_ports["out"], sink.input_ports["in"])

    g.run()

#def process_stream(pet):
#    ctf_plugin = bt2.find_plugin("ctf")
#    g = bt2.Graph()
#    source = g.add_component(ctf_plugin.source_component_classes["fs"],
#                         "source",
#                         params={"inputs":["/home/rocky/tmp/fv3/wave/traceout"]})
#
#    ports = list(source.output_ports)
#    sink = g.add_component(SinglePETSink, "sink"+str(pet), params={"stream": str(ports[pet])})
#    g.connect_ports(source.output_ports[ports[pet]], sink.input_ports["in"])
#    print("Connected port: " + str(pet))
#
#    g.run()



class ProcessTraceUnitTest(unittest.TestCase):

    def test_read_trace(self):
        process_trace("./test-traces/atm-ocn")
