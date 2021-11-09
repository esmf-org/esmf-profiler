#!/bin/bash
vercomp () {
    if [[ $1 == $2 ]]
    then
        return 0
    fi
    local IFS=.
    local i ver1=($1) ver2=($2)
    # fill empty fields in ver1 with zeros
    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++))
    do
        ver1[i]=0
    done
    for ((i=0; i<${#ver1[@]}; i++))
    do
        if [[ -z ${ver2[i]} ]]
        then
            # fill empty fields in ver2 with zeros
            ver2[i]=0
        fi
        if ((10#${ver1[i]} > 10#${ver2[i]}))
        then
            return 1
        fi
        if ((10#${ver1[i]} < 10#${ver2[i]}))
        then
            return 2
        fi
    done
    return 0
}

gccver="$(gcc -dumpversion)"
requiredgcc="9.0.0"

vercomp $gccver $requiredgcc
if [[ $? < 2 ]]; then 
    echo "Found gcc version ${gccver}"
else
    echo "Error:  The Babeltrace2 dependent library require gcc version of at least ${requiredgcc}.  Make sure gcc 9+ is in your path before running this script."
    exit 1
fi

SWIG='swig-4.0.2'
BT2='babeltrace2-2.0.4'

cd ./dependencies

echo "Bootstrapping ${SWIG}"
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

./configure --prefix=$PWD/../INSTALL/$BT2 --enable-static --enable-python-bindings --enable-python-plugins --disable-man-pages --disable-debug-info
make clean
make -j6
make install
cd ..

echo "Removing install directories"
# rm -rf $BT2
rm -rf $SWIG
rm -rf $PWD/INSTALL/$SWIG

echo "SUCCESS"
exit 0;




