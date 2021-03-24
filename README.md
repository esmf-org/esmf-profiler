# esmf-profiler

## Babeltrace2

Download:
https://www.efficios.com/files/babeltrace/babeltrace2-2.0.4.tar.bz2

**Note: Babeltrace2 appears to require the GNU compiler - there are failures with Intel.**

### Linux gcc 9.3

```bash
cd /path/to/babeltrace2-2.0.4
./configure --prefix=/home/rocky/bt2/INSTALL/2.0.4 --enable-python-bindings --enable-python-plugins --disable-debug-info --enable-compile-warnings=no
make -j4
make install

# set up PYTHONPATH so that the bt2 module is available
export PYTHONPATH=/home/rocky/bt2/INSTALL/2.0.4/lib/python3.5/site-packages

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
