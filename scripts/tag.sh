#!/bin/bash

# tag.sh
# Ryan Long <ryan.long@noaa.gov>

# Used to keep setup.py and Git versions in sync.  

# Reads the version from setup.py and attempts to create
# a git tag based off of it.

echo "Enter a version description."
read VERSION_DESCRIPTION
git tag -a v$(python setup.py --version) -m $VERSION_DESCRIPTION