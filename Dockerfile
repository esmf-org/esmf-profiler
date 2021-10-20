FROM ubuntu:20.04

MAINTAINER "Ryan Long <ryan.long@noaa.gov>"

# links remote /home with local current directory
ADD . /home

ENV HOME /home
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

# Create virtual environment to persist paths
RUN python3 -m venv ./venv

# install OS dependencies
RUN ./install_dependencies.sh && ./install.sh

# activate venv and install application
# TODO -e (local install) is required to pick up the module...
RUN ./venv/bin/activate && python3 -m pip install -e .

# activate venv and execute the profiler
CMD ./venv/bin/activate && esmf-profiler -t ./tests/fixtures/test-traces -n 'test1' -o /home