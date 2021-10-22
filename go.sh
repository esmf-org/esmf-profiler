#!/bin/bash

DEFAULT_OUTPUT_NAME="default"
OUTPUT_NAME="${1:-$DEFAULT_OUTPUT_NAME}"

docker build -t test9 .

docker run -it -v $(pwd)/traces:/home/traces test9 esmf-profiler -t /home/traces -n $1 -o /home/traces/output