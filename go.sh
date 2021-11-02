#!/bin/bash

DEFAULT_OUTPUT_NAME="default"
OUTPUT_NAME="${1:-$DEFAULT_OUTPUT_NAME}"

docker build -t esmf-profiler-image .

docker run -it -v $(pwd)/traces:/home/traces esmf-profiler-image esmf-profiler -t /home/traces -n $OUTPUT_NAME -o /home/traces/output