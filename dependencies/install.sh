#!/bin/bash


SWIG='swig-4.0.2'
PCRE='pcre-8.37'
BT2='babeltrace2-2.0.4'

echo "Installing ${SWIG}"
if [ ! -e ${SWIG}.tar.gz ]; then
  wget -T 10 -t 3 \
    http://prdownloads.sourceforge.net/swig/${SWIG}.tar.gz || exit 1;
fi
tar -xovzf ${SWIG}.tar.gz || exit 1
cd $SWIG
# We first have to install PCRE.
echo "Installing SWIG dependency ${PCRE}"
# if [ ! -e ${PCRE}.tar.gz ]; then
#   wget -T 10 -t 3 \
#     https://sourceforge.net/projects/pcre/files/pcre/8.37/${PCRE}.tar.gz || exit 1;
    
# fi
# Tools/pcre-build.sh
./configure --prefix=/glade/u/home/rlong/opt/swig
make
make install
cd ..

export PATH=/glade/u/home/rlong/opt/swig/bin:$PATH
export PYTHONPATH=/glade/u/home/rlong/opt/bt2/lib/python3.7/site-packages:$PYTHONPATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/glade/u/home/rlong/opt/bt2/lib

echo "Installing ${BT2}"
if [ ! -e ${BT2}.tar.bz2 ]; then
  wget -T 10 -t 3 \
    https://www.efficios.com/files/babeltrace/${BT2}.tar.bz2 || exit 1;
fi
tar -xojvf ${BT2}.tar.bz2 || exit 1
cd ${BT2}
pip install python-config
./configure --prefix=/glade/u/home/rlong/opt/bt2 --enable-shared --enable-python-bindings --enable-python-plugins --disable-man-pages --disable-debug-info
make
make install
cd ..



