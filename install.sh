#!/bin/bash

# This script is for local installs only using a virtual environment

BT2='babeltrace2-2.0.4'

# pip install python-config
echo $PWD
echo "Creating virtual environment"
python3 -m venv ./venv || exit 1

BT2PYTHON=$(find $PWD/dependencies/INSTALL/$BT2 -type d -name "site-packages")
if [ ! -d "$BT2PYTHON" ] 
then
    echo "Failed to find Python Babeltrace2 module: $BT2PYTHON"
    exit 1
else
    echo "Found Python Babeltrace2 module: $BT2PYTHON"
fi

echo "Adding BT2/lib to PYTHONPATH"
echo "export PYTHONPATH=$BT2PYTHON:$PYTHONPATH" >> ./venv/bin/activate
echo "set PYTHONPATH=$PYTHONPATH$BT2PYTHON" >> ./venv/bin/activate.csh

echo "Adding BT2/lib to LD_LIBRARY_PATH" 

echo "export LD_LIBRARY_PATH=$PWD/dependencies/INSTALL/$BT2/lib:$LD_LIBRARY_PATH" >> ./venv/bin/activate
echo "set LD_LIBRARY_PATH=$LD_LIBRARY_PATH$PWD/dependencies/INSTALL/$BT2/lib" >> ./venv/bin/activate.csh
