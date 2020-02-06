#!/bin/bash
export PY_VER=`python3 -c "import sys; print('{0[0]}.{0[1]}'.format(sys.version_info))"`
export PY_LOCAL_LIB="$HOME/.local/lib/python$PY_VER/site-packages"
export INSTALL_FOLDER="`pwd`/dependencies"
export SIHD_FOLDER="$INSTALL_FOLDER/sihd"

if [ -d "$SIHD_FOLDER" ]
then
    echo "Linking $SIHD_FOLDER -> $PY_LOCAL_LIB/sihd"
    rm -f $PY_LOCAL_LIB/sihd
    ln -s $SIHD_FOLDER $PY_LOCAL_LIB/sihd
else
    echo "Error: SIHD lib not downloaded - please run install script and run this script again"
fi
echo "Linking `pwd` -> $PY_LOCAL_LIB/BlindSailor"
rm -f $PY_LOCAL_LIB/BlindSailor
ln -s `pwd` $PY_LOCAL_LIB/BlindSailor
