import json
import textwrap
from abc import ABC, abstractproperty
from collections import namedtuple
from statistics import mean
from typing import Any, Generator, Iterator, List
import logging

import bt2

from esmf_profiler.utils import print_execution_time
from esmf_profiler.analyses import Analysis
from esmf_profiler.event import TraceEvent, RegionProfile, DefineRegion

import time

logger = logging.getLogger(__name__)
# _format = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
# logging.basicConfig(level=logging.DEBUG, format=_format)

ctf_plugin = bt2.find_plugin("ctf")
utils_plugin = bt2.find_plugin("utils")

MAX_CHUNKS = 1000000       # maximum number of file chunks during trace read
DEFAULT_CHUNK_SIZE = 250   # default size (number of PETs) to read per chunk

@bt2.plugin_component_class
class MessageSink(bt2._UserSinkComponent):

    def __init__(self, config, params, msg_callback):
        assert callable(msg_callback)
        self._port = self._add_input_port("in")
        self._msg_callback = msg_callback

    def _user_graph_is_configured(self):
        self._it = self._create_message_iterator(self._port)
        #logger.debug(f"Message sink: _user_graph_is_configured done")

    def _user_consume(self):
        msg = next(self._it)
        self._msg_callback(msg)


class Trace:
    def __init__(self, msgs: Generator[TraceEvent, None, None]):
        self._msgs = msgs

    def __iter__(self):
        yield from self._msgs

    def filter(self, fx):
        yield from filter(fx, self._msgs)

    @staticmethod
    def from_path(_path: str, analyses):
        logger.debug(f"fetching traces from path: {_path}")

        # hard code for now - eventually query each Analysis
        # for what events need to be included
        includes = ["define_region", "region_profile"]
        tmp_count = 0

        for msg in bt2.TraceCollectionMessageIterator(_path):
            if type(msg) is bt2._EventMessageConst:

                tmp_count += 1
                if tmp_count % 10000 == 0:
                    logger.debug(f"Processed {tmp_count} events")

                eventName = msg.event.name
                if eventName in includes:
                    event = TraceEvent.Of(msg)
                    # allow each analysis to process the event
                    # however it needs to
                    for analysis in analyses:
                        analysis.process_event(event)

        logger.debug(f"exiting from_path")


    @staticmethod
    def from_path_chunk(_path: str, analyses, chunksize: int):

        logger.debug(f"Loading trace from path: {_path}")

        _msg_count = 0

        # hard code for now - eventually query each Analysis
        # for what events need to be included
        includes = ["define_region", "region_profile"]

        def _process_msg(msg):
            nonlocal _msg_count
            _msg_count = _msg_count + 1
            if _msg_count % 10000 == 0:
                logger.debug(f"Processed {_msg_count} events")

            if type(msg) is bt2._EventMessageConst:
                eventName = msg.event.name
                if eventName in includes:
                    event = TraceEvent.Of(msg)
                    # allow each analysis to process the event
                    # however it needs to
                    for analysis in analyses:
                        analysis.process_event(event)


        for chunk in range(MAX_CHUNKS):
            g = bt2.Graph()
            source = g.add_component(ctf_plugin.source_component_classes["fs"],
                                     "source",
                                     params={"inputs": [_path]})

            muxer = g.add_component(utils_plugin.filter_component_classes["muxer"], "muxer")

            start_port = chunk*chunksize
            end_port = start_port + chunksize - 1
            oports = [x[1] for x in filter(lambda x: x[0] >= start_port and x[0] <= end_port,
                                           enumerate(source.output_ports))]
            if len(oports) == 0:
                break

            logger.debug(f"Processing streams {start_port} to {end_port}")
            for idx, oport in enumerate(oports):
                g.connect_ports(source.output_ports[oport], muxer.input_ports["in" + str(idx)])
                #logger.debug(f"connected ports: {oport} -> in{idx}")

            sink = g.add_component(MessageSink, "sink", obj=_process_msg)
            g.connect_ports(muxer.output_ports["out"], sink.input_ports["in"])

            g.run()

        logger.debug(f"Finished processing trace")
