import os.path
import bt2
import pprint
import unittest
import timing_tree
import jinja2
from datetime import datetime

@bt2.plugin_component_class
class MultiPETTimingSummary(bt2._UserSinkComponent):

    def __init__(self, config, params, obj):
        self._port = self._add_input_port("in")
        self._single_pet_maps = {}   # per-PET maps of region id to region name
        self._single_pet_roots = {}  # per-PET region timing trees
        self._multi_pet_summary = timing_tree.MultiPETTimingNode()
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

        #print("MultiPETTimingSummary init")

    def _user_graph_is_configured(self):
        self._it = self._create_message_iterator(self._port)
        print("DONE _user_graph_is_configured")

    def _user_consume(self):
        msg = next(self._it)

        self._tmp_count += 1
        if self._tmp_count % 10000 == 0:
            print("Processed {} records".format(self._tmp_count))

        if type(msg) is bt2._EventMessageConst:

            if msg.event.name == 'define_region':
                pet = msg.event.packet.context_field["pet"]
                regid = msg.event.payload_field["id"]
                regname = msg.event.payload_field["name"]
                self._single_pet_maps.setdefault(pet, {})[regid] = regname


            # a region_profile is a single node in a single PET timing tree
            # the tree is reconstructed by adding nodes to the appropriate
            # place in the tree based on the parentid
            elif msg.event.name == 'region_profile':
                pet = msg.event.packet.context_field["pet"]
                root = self._single_pet_roots.setdefault(pet, timing_tree.SinglePETTimingNode(0))
                root.pet = pet

                e = msg.event
                node = timing_tree.SinglePETTimingNode(e.payload_field["id"])
                node.pet = pet
                node.count = e.payload_field["count"]
                node.total = e.payload_field["total"]
                node.max = e.payload_field["max"]
                node.min = e.payload_field["min"]
                node.mean = e.payload_field["mean"]
                node.name = self._single_pet_maps[pet].get(node.local_id, "Unknown")

                # add the node to the right place in the tree based on the parentid
                if not root.add_to_tree(node, e.payload_field["parentid"]):
                    raise Exception("Error adding timed region tree: " + str(node.local_id))

            #else:
            #    print("Msg event name = {}".format(msg.event.name))

        elif type(msg) is bt2._StreamBeginningMessageConst:
            self._stream_count = self._stream_count + 1
        elif type(msg) is bt2._StreamEndMessageConst:
            self._stream_count = self._stream_count - 1
            if self._stream_count == 0:
                self._finish()

    def _finish(self):

        print("ENTER _finish")
        for pet, root in self._single_pet_roots.items():
            self._multi_pet_summary.merge(root)

        print("Region Summary")
        pprint.pprint(self._multi_pet_summary)

        self._generate_html()


    def _generate_html(self):

        print("ENTER _generate_html")

        jenv = jinja2.Environment(
            loader=jinja2.FileSystemLoader('templates'),
            trim_blocks=True,
            lstrip_blocks=True
        )

        template = jenv.get_template("index.html.jinja")
        html = template.render(name=self._name,
                               now=datetime.now(),
                               region_summary=self._multi_pet_summary)

        with open("{}/{}".format(self._output_path, "index.html"), "w") as fh:
            fh.write(html)
        print("Generated file: {}/index.html".format(self._output_path))


        template = jenv.get_template("loadbalance.html.jinja")
        html = template.render(name=self._name,
                               now=datetime.now(),
                               region_summary=self._multi_pet_summary)

        with open("{}/{}".format(self._output_path, "loadbalance.html"), "w") as fh:
            fh.write(html)
        print("Generated file: {}/loadbalance.html".format(self._output_path))



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


class ProcessTraceUnitTest(unittest.TestCase):

    def test_read_trace(self):
        process_trace("./test-traces/atm-ocn")
        #process_trace("./test-traces/cpld_bmark_wave_v16")
