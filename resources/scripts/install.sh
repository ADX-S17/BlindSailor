#!/bin/bash
export INSTALL_FOLDER="`pwd`/dependencies"
export SIHD_FOLDER="$INSTALL_FOLDER/sihd"

echo "Installing python3 pynmea2"
pip3 install pynmea2 --user
echo "Installing python3 pySerial"
pip3 install pySerial --user

mkdir -p $INSTALL_FOLDER
if [ ! -d "$SIHD_FOLDER" ]
then
    echo "Downloading SIHD lib"
    git clone https://github.com/mdufaud/sihd.git $INSTALL_FOLDER/sihd
fi
