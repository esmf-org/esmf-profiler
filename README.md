# esmf-profiler

## Babeltrace2

Download:
https://www.efficios.com/files/babeltrace/babeltrace2-2.0.4.tar.bz2

### Linux gcc 9.3

```bash
./configure --prefix=/home/rocky/bt2/INSTALL/2.0.4 --enable-python-bindings --enable-python-plugins --disable-debug-info --enable-compile-warnings=no
make -j4
make install
```
