#!/bin/bash

gccver="$(gcc -dumpversion)"
requiredgcc="9.0.0"
if [ "$(printf '%s\n' "$requiredgcc" "$gccver" | sort -V | head -n1)" = "$requiredgcc" ]; then 
    echo "Found gcc version ${gccver}"
else
    echo "Error:  The Babeltrace2 dependent library require gcc version of at least ${requiredgcc}.  Make sure gcc 9+ is in your path before running this script."
    exit 1
fi

SWIG='swig-4.0.2'
BT2='babeltrace2-2.0.4'

cd ./dependencies

echo "Installing ${SWIG}"
if [ ! -e ${SWIG}.tar.gz ]; then
  exit 1;
fi
tar -xovzf ${SWIG}.tar.gz || exit 1
cd $SWIG
./configure --prefix=$PWD/../INSTALL/$SWIG --without-go --without-r --without-lua --without-csharp --without-ocaml --without-ruby --without-mzscheme --without-java --without-javascript --without-octave --without-scilab
make clean
make -j6
make install
cd ..
export PATH=$PWD/INSTALL/$SWIG/bin:$PATH

echo "Installing ${BT2}"
if [ ! -e ${BT2}.tar.bz2 ]; then
  exit 1;
fi
tar -xojvf ${BT2}.tar.bz2 || exit 1
cd $BT2

./configure --prefix=$PWD/../INSTALL/$BT2 --enable-shared --enable-python-bindings --enable-python-plugins --disable-man-pages --disable-debug-info
make clean
make -j6
make install
cd ..



