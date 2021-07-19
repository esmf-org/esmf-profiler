import bt2
import pprint
import unittest
import regiontree

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
@bt2.plugin_component_class
class SinglePETSink(bt2._UserSinkComponent):

    def __init__(self, config, params, obj: regiontree.RegionSummary):
        self._port = self._add_input_port("in")
        self._region_map = {}
        self._my_stream = str(params["stream"])
        self._timing_summary = obj
        self._pet = int(self._my_stream[-4:])  # assumes last 4 is PET number
        self._root_region = regiontree.RegionNode()
        self._root_region.name = "ROOT"
        self._root_region.local_id = 0
        self._region_summary = obj
        print("SinglePETSink for stream: {}".format(params["stream"]))

    def _user_graph_is_configured(self):
        self._it = self._create_message_iterator(self._port)

    def _user_consume(self):
        msg = next(self._it)

        if type(msg) is bt2._EventMessageConst:

            if msg.event.name == 'define_region':
                regid = msg.event.payload_field["id"]
                regname = msg.event.payload_field["name"]
                self._region_map[regid] = regname

            if msg.event.name == 'region_profile':
                rn = regiontree.RegionNode()
                rn.pet = self._pet
                regid = msg.event.payload_field["id"]
                regpid = msg.event.payload_field["parentid"]
                rn.local_id = regid
                rn.name = self._region_map.get(regid, "ROOT")
                rn.total = msg.event.payload_field["total"]
                rn.min = msg.event.payload_field["min"]
                rn.max = msg.event.payload_field["max"]
                rn.mean = msg.event.payload_field["mean"]
                rn.count = msg.event.payload_field["count"]

                added = self._root_region.add_to_tree(rn, regpid)
                if not added:
                    raise Exception("region not added to tree: " + str(regpid))

        elif type(msg) is bt2._StreamEndMessageConst:
            self._finish()

    def _finish(self):

        print("FINISHED STREAM: " + str(self._pet))
        
        self._region_summary.merge(self._root_region)
        

#
# Open and read a trace in CTF format output
# from ESMF.
#
# tracepath -- path to directory containing the trace
#
def process_trace(tracepath: str):

    ctf_plugin = bt2.find_plugin("ctf")

    g = bt2.Graph()
    source = g.add_component(ctf_plugin.source_component_classes["fs"],
                         "source",
                         params={"inputs":[tracepath]})

    regionsummary = regiontree.RegionSummary()
    
    sinks = {}
    for idx, op in enumerate(source.output_ports):
        sink = g.add_component(SinglePETSink, "sink" + str(idx), params={"stream": str(op)}, obj=regionsummary)
        g.connect_ports(source.output_ports[op], sink.input_ports["in"])
        sinks[idx] = sink

    g.run()

    pprint.pprint(regionsummary)
    return regionsummary
    
    

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

