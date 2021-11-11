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

logger = logging.getLogger(__name__)
# _format = "%(asctime)s : %(levelname)s : %(name)s : %(message)s"
# logging.basicConfig(level=logging.DEBUG, format=_format)


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
