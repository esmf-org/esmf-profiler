FROM ubuntu:20.04

MAINTAINER "Ryan Long <ryan.long@noaa.gov>"

# links remote /home with local current directory
ADD . /home

ENV HOME /home
ENV DEBIAN_FRONTEND noninteractive

# Update package repo
RUN apt-get update 

# Install Git
RUN apt-get install -y git

# Python & C essentials
RUN apt-get install -y -q build-essential libssl-dev libffi-dev python3 python3-pip python3-dev bison python3.8-venv flex libglib2.0-dev

#TODO: Check GCC version at some point, need >9 but comes with 9.3?

# Clone profiler
WORKDIR /home

# TODO: Specifiying a branch here, should be main once we get into prod
RUN git clone -b 32_bug_version_compare_install_script https://github.com/esmf-org/esmf-profiler.git
WORKDIR /home/esmf-profiler

# install OS dependencies
RUN ./install_dependencies.sh
RUN ./install.sh 

RUN source ./venv/bin/activate && python3 -m pip install -e .

# execute the profiler
RUN esmf-profiler -t ./tests/fixtures/test-traces -n 'test1' -o /home