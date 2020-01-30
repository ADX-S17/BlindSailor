#!/bin/bash
export INSTALL_FOLDER="`pwd`/dependencies"
export SIHD_FOLDER="$INSTALL_FOLDER/sihd"

mkdir -p $INSTALL_FOLDER
if [ ! -d "$SIHD_FOLDER" ]
then
    echo "Downloading SIHD lib"
    git clone https://github.com/mdufaud/sihd.git $INSTALL_FOLDER/sihd
else
    git pull $INSTALL_FOLDER/sihd
fi
