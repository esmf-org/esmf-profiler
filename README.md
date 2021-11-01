# esmf-profiler

## Description
The ESMF-Profiler project is designed to take trace binary output and display it in a web based GUI.

## Quickstart

### Local Install:

1. Clone the [latest stable branch](https://github.com/esmf-org/esmf-profiler.git) from the [esmf-profiler repository](https://github.com/esmf-org/esmf-profiler).

2. cd into the appliction path
```bash
cd esmf-profiler
```

3.  Ensure that the ```install_dependencies.sh``` and ```install.sh``` have executable permissions
```bash
chmod +x ./install_dependencies.sh 
chmod +x ./install.sh
```

4.  Execute both scripts as shown below.  A ```venv``` folder will be created on success.
```bash
./install_dependencies.sh && ./install.sh
```

5.  Activate the [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).
```bash
source ./venv/bin/activate
```

6.  For pre-release, install the *esmf-profiler* using *pip* in developer mode.
```bash
pip install -e .[test]
```

7.  Confirm the installation was successful.  If so, you should now be able to type ```esmf-profiler``` into your terminal and see the help output.
```bash
python -m pytest
esmf-profiler
```





5.  



## Dependencies
### Install Babeltrace2

#### Use a Package Manager
There are some package managers that install Babeltrace2.  
https://babeltrace.org/#bt2-get
However, you need to make sure the Python bindings are included.

#### Build Babeltrace2 from source

Prereqs:
- glibc-2.0  (Ubuntu: `sudo apt-get install libglib2.0`)
- swig (Ubuntu: `sudo apt-get install swig`)

Download:
https://www.efficios.com/files/babeltrace/babeltrace2-2.0.4.tar.bz2

**Note: Babeltrace2 appears to require the GNU compiler >9.0 - there are failures with Intel.**

#### Linux gcc 9.3

```bash
cd /path/to/babeltrace2-2.0.4
./configure --prefix=/path/to/babeltrace2/INSTALL/2.0.4 --enable-python-bindings --enable-python-plugins --disable-debug-info --enable-compile-warnings=no
make -j4
make install

# set up PYTHONPATH so that the bt2 module is available
export PYTHONPATH=/path/to/babeltrace2/INSTALL/2.0.4/lib/python3.5/site-packages

# if installed in non-standard place, you need to set LD_LIBRARY_PATH:
export LD_LIBRARY_PATH=/path/to/babeltrace2/INSTALL/2.0.4/lib

```

#### Cheyenne

```
module load gnu/9.1.0 python/3.7.9
```

SWIG is needed for the build process and is not in the default Cheyenne PATH.
Download: http://prdownloads.sourceforge.net/swig/swig-4.0.2.tar.gz
```bash
./configure --prefix=/glade/u/home/dunlap/bt/INSTALL/swig-4.0.2
make
make install

export PATH=/glade/u/home/dunlap/bt/INSTALL/swig-4.0.2/bin:$PATH
```

Install babeltrace2
```bash
cd /path/to/babeltrace2-2.0.4
./configure --prefix=/glade/u/home/dunlap/bt/INSTALL/babeltrace2-2.0.4 --enable-python-bindings --enable-python-plugins --disable-debug-info
make -j6
make install

# set LD_LIBRARY_PATH so Python3 can find the dynamic library
export LD_LIBRARY_PATH=/glade/u/home/dunlap/bt/INSTALL/babeltrace2-2.0.4/lib:$LD_LIBRARY_PATH
```

#### install_dependencies.sh

esmf-profiler includes a script to build and install dependencies, setup a virtual environment, and add the necessary dependencies to the newly created virtual environment so that, when activate, all dependencies will available.

From the root of the project, execute the install_dependencies.sh script:

```bash
source ./install_dependencies.sh
```




(venv) should now be pre-pended to your prompt.

At this point, you can run the profiler by typing 'profiler' at the command prompt.


### Run Unit Tests
```
python3 -m unittest process_trace
```

### Linting
Pylint

All settings are in the well documented .pylintrc file.
