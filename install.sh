# change from $HOME
# gcc min 9 and must be loaded

#!/bin/bash
SWIG='swig-4.0.2'
PCRE='pcre-8.37'
BT2='babeltrace2-2.0.4'

cd ./dependencies

echo "Installing ${SWIG}"
if [ ! -e ${SWIG}.tar.gz ]; then
  exit 1;
fi
tar -xovzf ${SWIG}.tar.gz || exit 1
cd $SWIG
./configure --prefix=$PWD/$SWIG
make
make install
cd ..
export PATH=$PWD/$SWIG/$SWIG/bin:$PATH

echo "Installing ${BT2}"
if [ ! -e ${BT2}.tar.bz2 ]; then
  exit 1;
fi
tar -xojvf ${BT2}.tar.bz2 || exit 1
cd $BT2

#  Must have GCC
./configure --prefix=$PWD/$BT2/$BT2 --enable-shared --enable-python-bindings --enable-python-plugins --disable-man-pages --disable-debug-info
make
make install
cd ..

# pip install python-config
echo $PWD
echo "Creating virtual environment"
cd ..
python3 -m virtualenv ./venv || exit 1

echo "Adding BT2/lib to PYTHONPATH"
echo "export PYTHONPATH=$PWD/dependencies/$BT2/$BT2/lib/python3.7/site-packages:$PYTHONPATH" >> ./venv/bin/activate

echo "Adding BT2/lib to LD_LIBRARY_PATH"
echo "export LD_LIBRARY_PATH=$PWD/dependencies/$BT2/$BT2/lib:$LD_LIBRARY_PATH" >> ./venv/bin/activate

source ./venv/bin/activate || exit 1

pip install -e .


# Have 3.6 default




