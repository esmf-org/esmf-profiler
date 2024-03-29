![alt text](https://i.imgur.com/69q9VuJ.png)

# esmf-profiler

[![Python application](https://github.com/esmf-org/esmf-profiler/actions/workflows/python-app.yml/badge.svg?branch=development)](https://github.com/esmf-org/esmf-profiler/actions/workflows/python-app.yml)
### [Kanban Board](https://github.com/esmf-org/esmf-profiler/projects/1)

Status of issues

### [Discussion Board](https://github.com/esmf-org/esmf-profiler/discussions)

Features, bugs, and enhancements.

## Description

The ESMF-Profiler project is designed to take trace binary output and display it in a web based GUI.

## Getting a Binary Trace
To collect a binary trace, set the environment variables to the values below:

```bash
export ESMF_RUNTIME_PROFILE=ON
export ESMF_RUNTIME_PROFILE_OUTPUT="BINARY SUMMARY"
```

## Quickstart

### Local Install:

:warning:
At the time of this release IntelPython is not compatible.

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

6.  For pre-release, install the *esmf-profiler* using [pip editable install](https://pip.pypa.io/en/latest/cli/pip_install/#editable-installs).  Running tests require access to [PyPi Public Repositories](https://pypi.org/).  This step is optional, but encouraged.  Some HPC platforms do not have open internet access, so will not be able to install the tests.
```bash
pip install -e . or pip install -e .[test] // to run tests
```

7.  Confirm the installation was successful.  If so, you should now be able to type ```esmf-profiler``` into your terminal and see the help output.
```bash
python -m pytest // optional, to run tests
esmf-profiler
```

:information_source: 
If using **C-Shell**, deactivate then reactivate the virtual environment to run the applicication.

### Install with Docker

A [Dockerfile](https://docs.docker.com/engine/reference/builder/#:~:text=A%20Dockerfile%20is%20a%20text,command%2Dline%20instructions%20in%20succession.) is included in the repository to allow users using Docker to install the application with ease.

1. Clone the [latest stable branch](https://github.com/esmf-org/esmf-profiler.git) from the [esmf-profiler repository](https://github.com/esmf-org/esmf-profiler).

2. cd into the appliction path
```bash
cd esmf-profiler
```

3. Build the image
```bash
docker build -t esmf-profiler-image .
```

4. Run the application in the image.  For example, assuming your [binary traces](https://github.com/esmf-org/esmf-profiler/tree/main/tests/fixtures/test-traces/atm-ocn) are in ```./traces```
```bash
docker run -it -v $(pwd)/traces:/home/traces esmf-profiler-image esmf-profiler -t /home/traces -n 'profilename' -o /home/traces/output
```

This will spin up an *esmf-profiler-image* and mount ```./traces``` from client to host.  

Here, output is being directed to ```/home/traces/output```.  

:warning: 
Be sure the output path you pass to the ```esmf-profiler``` command has your client folder as it's root (```./traces``` *in the example*).  Otherwise, the output will not persist to your client machine after the application has run.

## Generating and Viewing Profiles
```bash

You can see the help menu displayed below after installation by running ```esmf-profiler``` with no arguments.

usage: esmf-profiler [-h] -t TRACEDIR -n NAME -o OUTDIR [-p PUSH] [-v] [-s]

ESMF Profiler

optional arguments:
  -h, --help            show this help message and exit
  -t TRACEDIR, --tracedir TRACEDIR
                        directory containing the ESMF trace
  -n NAME, --name NAME  name to use for the generated profile
  -o OUTDIR, --outdir OUTDIR
                        path to output directory
  -p PUSH, --push PUSH  git url of remote repository where to push profile
  -v, --verbose         enable verbose output
  -s, --serve           start a local server to host the profile results
```

### Examples

```bash
esmf-profiler -t ./fresh_traces -n "build_abc123" -o "output" -s
```
This is the most common way to use the profiler.  It requires some simple user permissions on the server you're running the application on.  

You're telling the application to:
- **-t ./freshtraces** The traces to run on are contained in **fresh_traces**, a subdirectory of the current working directory
- **-n "build_abc123** Name the output (the profile) "build_abc123".  This will be used for titles, directories, links, etc. in the GUI and file structure.
- **-o "output"** Send the output to **output** a directory that will be created (if no already exists) in the current working directory.  All output will be sent there.
- **-s** On success, start an ultra-light-weight python native web server at 0.0.0.0:8000

```bash
esmf-profiler -t ./fresh_traces -n "build_abc123" -o "output" -p 'git@github.com:user_name/repo_name.git'
```
This example will run the processing work locally as the first example, but then publish the results to the repository at ```git@github.com:user_name/repo_name.git```.

To view the profile on GitHub.io, you need to explicitly turn on "GitHub Pages" within the target repository.  Refer to the [Quickstart for Github Pages](https://docs.github.com/en/pages/quickstart) for details on how to turn on "Pages" within your repository.

```bash
docker build -t esmf-profiler-image .

docker run -it -v $(pwd)/traces:/home/traces esmf-profiler-image esmf-profiler -t /home/traces -n 'my_profile' -o /home/traces/output
```
This example utitilizes the [Dockerfile] for those leveraging Docker.

The image is built first, then ```<current_working_directory>/traces``` is mounted to ```/home/traces``` on the virtual machine.

Commands are the same for local and docker installations.

Here, we're telling the application to:
- **-t ./freshtraces** The traces to run on are contained in /home/traces (locally, $pwd and traces)
- **-n "build_abc123** Name the output (the profile) "my_profile".
- **-o "/home/traces/output** The target for the output of the applications.  **This must be a directory mounted via the ```docker run``` command
as discussed above.  Otherwise, the results will not persists after the docker run command has completed.

## Dependencies

:information_source: 
All dependencies are installed using any of the installation methods in Quick Start section.  This section is primarly for reference and historical purposes.

### Install Babeltrace2

#### Use a Package Manager
There are some package managers that install Babeltrace2.  
https://babeltrace.org/#bt2-get
However, you need to make sure the Python bindings are included.

#### Build Babeltrace2 from source

Prereqs:

- glibc-2.0 (Ubuntu: `sudo apt-get install libglib2.0`)
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
## Resources
https://docs.pytest.org/en/6.2.x/
https://code.visualstudio.com/docs/python/testing
http://www.swig.org/Doc4.0/SWIGDocumentation.html
