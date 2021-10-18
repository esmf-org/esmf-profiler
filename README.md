# esmf-profiler

### [Kanban Board](https://github.com/esmf-org/esmf-profiler/projects/1)

Status of issues

### [Discussion Board](https://github.com/esmf-org/esmf-profiler/discussions)

Features, bugs, and enhancements.

## Install Jinja2 into your Python environment

https://jinja.palletsprojects.com/en/3.0.x/intro/#installation

## Install Babeltrace2

### Use a Package Manager

There are some package managers that install Babeltrace2.  
https://babeltrace.org/#bt2-get
However, you need to make sure the Python bindings are included.

### Build Babeltrace2 from source

Prereqs:

- glibc-2.0 (Ubuntu: `sudo apt-get install libglib2.0`)
- swig (Ubuntu: `sudo apt-get install swig`)

Download:
https://www.efficios.com/files/babeltrace/babeltrace2-2.0.4.tar.bz2

**Note: Babeltrace2 appears to require the GNU compiler - there are failures with Intel.**

### Linux gcc 9.3

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

### Cheyenne

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

## Run Unit Tests

```
python3 -m unittest process_trace
```
