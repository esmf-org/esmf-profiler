#!/bin/bash
docker build -t esmf-profiler-image ..

docker run -it -v $(pwd)/traces:/home/traces esmf-profiler-image esmf-profiler -t /home/traces -n 'automatedtest' -o /home/traces/output