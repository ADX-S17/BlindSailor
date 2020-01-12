#!/bin/bash
export PY_VER=`python3 -c "import sys; print('{0[0]}.{0[1]}'.format(sys.version_info))"`
export PY_LOCAL_LIB="$HOME/.local/lib/python$PY_VER/site-packages"
export INSTALL_FOLDER="`pwd`/dependencies"
export SIHD_FOLDER="$INSTALL_FOLDER/sihd"

echo "Removing links"
rm $PY_LOCAL_LIB/BlindSailor
rm $PY_LOCAL_LIB/sihd

echo "Removing SIHD"
rm -rf $INSTALL_FOLDER
