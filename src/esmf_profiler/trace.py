import math
from typing import List
import logging
import bt2
from esmf_profiler.analyses import Analysis

#from guppy import hpy

logger = logging.getLogger(__name__)

@bt2.plugin_component_class
class MessageSink(bt2._UserSinkComponent):

    def __init__(self, config, params, msg_callback):
        assert callable(msg_callback)
        self._port = self._add_input_port("in")
        self._msg_callback = msg_callback

    def _user_graph_is_configured(self):
        self._it = self._create_message_iterator(self._port)

    def _user_consume(self):
        msg = next(self._it)
        self._msg_callback(msg)


class Trace:

    DEFAULT_CHUNK_SIZE = 250  # default size (number of PETs) to read per chunk

    CTF_PLUGIN = bt2.find_plugin("ctf")
    UTILS_PLUGIN = bt2.find_plugin("utils")

    @staticmethod
    def from_path(_path: str, analyses, chunksize: int):

        logger.debug(f"Loading trace from path: {_path}")

        # hard code for now - eventually query each Analysis
        # for what events need to be included
        includes = ["define_region", "region_profile"]

        # used for memory profiling
        # h = hpy()

        _msg_count = 0

        def _process_chunk(chunk, analyses: List[Analysis]):

            def _process_msg(msg):
                nonlocal _msg_count
                _msg_count = _msg_count + 1
                if _msg_count % 50000 == 0:
                    logger.info(f"Processed {_msg_count} events")

                    for analysis in analyses:
                        analysis.debug_log_queues()
                        #logger.debug(f"  ==> Q size = {analysis.queue_size()}")

                if type(msg) is bt2._EventMessageConst:
                    event_name = msg.event.name
                    if event_name in includes:
                        for analysis in analyses:
                            analysis.process_event(msg)


            g = bt2.Graph()
            source = g.add_component(Trace.CTF_PLUGIN.source_component_classes["fs"],
                                     "source",
                                     params={"inputs": [_path]})

            start_port = chunk * chunksize
            end_port = start_port + chunksize - 1
            oports = [x[1] for x in filter(lambda x: x[0] >= start_port and x[0] <= end_port,
                                           enumerate(source.output_ports))]
            assert len(oports) > 0

            muxer = g.add_component(Trace.UTILS_PLUGIN.filter_component_classes["muxer"], "muxer")

            for idx, oport in enumerate(oports):
                g.connect_ports(source.output_ports[oport], muxer.input_ports["in" + str(idx)])
                # logger.debug(f"connected ports: {oport} -> in{idx}")

            sink = g.add_component(MessageSink, "sink", obj=_process_msg)
            g.connect_ports(muxer.output_ports["out"], sink.input_ports["in"])

            logger.info(f"Processing PETs {start_port} to {end_port}")
            g.run()


        g = bt2.Graph()
        source = g.add_component(Trace.CTF_PLUGIN.source_component_classes["fs"],
                                 "source",
                                 params={"inputs": [_path]})
        total_ports = len(source.output_ports)
        g = None

        # NOTE:  Multi-threading of the trace reading at this
        #        level did not show a performance advantage - in
        #        fact it made it worse in most cases.
        #with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        #    for chunk in range(math.ceil(total_ports/chunksize)):
        #        logger.debug(f"Start thread for chunk {chunk}")
        #        executor.submit(_process_chunk, chunk, [a.new_instance() for a in analyses])

        for chunk in range(math.ceil(total_ports/chunksize)):
            _process_chunk(chunk, analyses)

        logger.debug(f"Total messages: {_msg_count}")
