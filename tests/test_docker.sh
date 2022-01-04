#!/bin/bash
docker build -t esmf-profiler-image ..
cd ..
echo $PWD
echo "$PWD/traces"
docker run -it -v $PWD/traces:/home/traces esmf-profiler-image esmf-profiler -t /home/traces -n 'automatedtest' -o /home/traces/output
