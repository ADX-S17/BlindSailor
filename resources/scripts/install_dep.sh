#!/bin/bash
export INSTALL_FOLDER="`pwd`/dependencies"
export SIHD_FOLDER="$INSTALL_FOLDER/sihd"

echo "Installing python3 pynmea2"
pip3 install pynmea2 --user
echo "Installing python3 pySerial"
pip3 install pySerial --user
echo "Installing python3 RPi.bme280"
pip3 install RPi.bme280 --user
