#!/bin/bash
export PY_VER=`python3 -c "import sys; print('{0[0]}.{0[1]}'.format(sys.version_info))"`
export PY_LOCAL_LIB="$HOME/.local/lib/python$PY_VER/site-packages"
export INSTALL_FOLDER="`pwd`/dependencies"
pip3 install pynmea2 --user
pip3 install serial --user
mkdir -p $INSTALL_FOLDER
git clone https://github.com/mdufaud/sihd.git $INSTALL_FOLDER/sihd
ln -s $INSTALL_FOLDER/sihd $PY_LOCAL_LIB/sihd
ln -s `pwd` $PY_LOCAL_LIB/BlindSailor
