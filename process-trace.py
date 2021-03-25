import bt2
import pprint
import unittest
import regiontree

#from concurrent.futures import ThreadPoolExecutor
#import csv
#import json
#import os

class TimingSummary:

    def __init__(self):
        self._csv_data = {}

    def add_summary(self, pet, rows):
        self._csv_data[pet] = rows


@bt2.plugin_component_class
class SinglePETSink(bt2._UserSinkComponent):

    def __init__(self, config, params, obj: TimingSummary):
        self._port = self._add_input_port("in")
        self._region_map = {}
        #self._region_stats = {}
        self._my_stream = str(params["stream"])
        self._timing_summary = obj
        self._pet = int(self._my_stream[-4:])  # assumes last 4 is PET number
        self._root_region = regiontree.RegionNode()
        self._root_region.name = "ROOT"
        self._root_region.local_id = 0
        #self._cur_region = self._root_region
        print("SinglePETSink for stream: {}".format(params["stream"]))
        #params["addme"].append(self)

    def _user_graph_is_configured(self):
        self._it = self._create_message_iterator(self._port)

    def _user_consume(self):
        msg = next(self._it)

        if type(msg) is bt2._EventMessageConst:

            if msg.event.name == 'define_region':
                #pet = msg.event.packet.context_field["pet"]
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

                added = self._root_region.add_to_tree(rn, regpid)
                if not added:
                    raise Exception("region not added to tree: " + str(regpid))

        elif type(msg) is bt2._StreamEndMessageConst:
            #if self._pet == 0:
            self._finish()

            #if self._my_stream.endswith("0000"):
            #    self._debug_print()

    def _finish(self):
        #self._csv.add_summary(self._pet, )
        #with open('data/regions.csv', 'w+') as outfile:
        #    wr = csv.writer(outfile, quoting=csv.QUOTE_ALL)
        #    wr.writerow(["id","name"])
        #    for k in self._region_map:
        #        wr.writerow([k, self._region_map[k]])


        print("\n\nRESULT OF STREAM: " + str(self._pet))
        print("==============================================")
        pprint.pprint(self._region_map)

        #if not os.path.exists("data"):
        #    os.makedirs("data")

        #with open("data/timing_summary.json", "w+") as outfile:
        #    json.dump({"regions": self._region_map, "timing": self._region_stats}, outfile, indent=3)


        #print("wrote data/timing_summary.json")

    #def _debug_print(self):
        #print("\n============\n")
        #pprint.pprint(self._region_map)
        #print("\n============\n")
        #pprint.pprint(self._region_stats)

# set up the processing graph
#text_plugin = bt2.find_plugin("text")
#utils_plugin = bt2.find_plugin("utils")

def process_trace(tracepath: str):

    ctf_plugin = bt2.find_plugin("ctf")

    g = bt2.Graph()
    source = g.add_component(ctf_plugin.source_component_classes["fs"],
                         "source",
                         params={"inputs":[tracepath]})

    for idx, op in enumerate(source.output_ports):
        sink = g.add_component(SinglePETSink, "sink" + str(idx), params={"stream": str(op)})
        g.connect_ports(source.output_ports[op], sink.input_ports["in"])

    #muxer = g.add_component(utils_plugin.filter_component_classes["muxer"],
    #                           "filter")

    #sink = g.add_component(text_plugin.sink_component_classes["pretty"], "sink")

    #sink = g.add_component(MyFirstSink, "sink")

    #counter = g.add_component(utils_plugin.sink_component_classes["counter"], "counter")


    #outports = list(source.output_ports)
    #inports = list(sink.input_ports)

    # connect all source output streams to the muxer
    #for idx, op in enumerate(source.output_ports):
    #    g.connect_ports(source.output_ports[op], muxer.input_ports["in"+str(idx)])



    # connect muxer output to pretty print
    #g.connect_ports(muxer.output_ports["out"], sink.input_ports["in"])

    #g.connect_ports(muxer.output_ports["out"], counter.input_ports["in"])

    #t0 = time.time()
    g.run()
    #t1 = time.time()
    #total = t1-t0

    #print out
    #sinks[0]._debug_print()

    #print("Total time: " + str(total))


def process_stream(pet):
    ctf_plugin = bt2.find_plugin("ctf")
    g = bt2.Graph()
    source = g.add_component(ctf_plugin.source_component_classes["fs"],
                         "source",
                         params={"inputs":["/home/rocky/tmp/fv3/wave/traceout"]})

    ports = list(source.output_ports)
    sink = g.add_component(SinglePETSink, "sink"+str(pet), params={"stream": str(ports[pet])})
    g.connect_ports(source.output_ports[ports[pet]], sink.input_ports["in"])
    print("Connected port: " + str(pet))

    g.run()


#executor = ThreadPoolExecutor(8)
#t0 = time.time()
#futures = []
#for i in range(0,100):
#    future = executor.submit(process_stream, i)
#    futures.append(future)
#for i in range(0,100):
#    futures[i].result()
#t1 = time.time()
#total = t1-t0
#print("Total time: " + str(total))


class ProcessTraceUnitTest(unittest.TestCase):

    def test_read_trace(self):
        process_trace("./test-traces/atm-ocn")

