FROM ubuntu:20.04

MAINTAINER "Ryan Long <ryan.long@noaa.gov>"

# links remote /home with local current directory

ENV DEBIAN_FRONTEND noninteractive

# Update package repo
RUN apt-get update 

# Install dependencies
RUN apt-get install -y -q git build-essential libssl-dev libffi-dev python3 python3-pip python3-dev bison python3.8-venv flex libglib2.0-dev

# Clone profiler
# TODO: Specifiying a branch here, should be main once we get into prod
WORKDIR /home
RUN git clone -b development https://github.com/esmf-org/esmf-profiler.git
WORKDIR /home/esmf-profiler

# install OS dependencies
RUN ./install_dependencies.sh

# Set Environtment paths for Python and LD_Library
ENV PYTHONPATH="/home/esmf-profiler/dependencies/INSTALL/babeltrace2-2.0.4/lib/python3.8/site-packages:$PYTHONPATH"
ENV LD_LIBRARY_PATH="/home/esmf-profiler/dependencies/INSTALL/babeltrace2-2.0.4/lib:$LB_LIBRARY_PATH"

# TODO -e (local install) is required to pick up the module... https://github.com/esmf-org/esmf-profiler/issues/35
RUN ["python3", "-m", "pip", "install", "-e", "."]

# RUN ["/bin/bash", "-c ", ".", "./venv/bin/activate",  "&& esmf-profiler", "-t ", "./tests/fixtures/test-traces", "-n", "test1",  "-o",  "/home/blitzcrank"]"
# CMD [".", "./venv/bin/activate",   && esmf-profiler -t ./tests/fixtures/test-traces -n 'test1' -o /home/blitzcrank
