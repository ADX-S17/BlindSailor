#!/usr/bin/python
#coding: utf-8

""" System """

import time
import os

smbus2 = None
bme280 = None

from sihd.readers.AReader import AReader

class Bme280Reader(AReader):

    def __init__(self, name="Bme280Reader", app=None):
        global bme280
        if bme280 is None:
            import bme280
        global smbus2
        if smbus2 is None:
            import smbus2
        super().__init__(app=app, name=name)
        self.__bus = None
        self.__calib = None
        self.configuration.add_defaults({
            "port": "/dev/something",
            "addr": 0,
        })
        self.add_channel("temperature", type='double')
        self.add_channel("pressure", type='double')
        self.add_channel("humidity", type='double')
        self.add_channel("timestamp", type='double')

    def on_setup(self, config):
        port = config.get("port", default=False)
        addr = config.get("addr")
        if port and addr:
            ret = self.open(port, int(addr))
        return ret and super().on_setup(config)

    """ Reader """

    def open(self, port, addr):
        self.log_info("Reading on port: {} - addr: {}".format(port, addr))
        bus = smbus2.SMBus(port)
        calib = bme280.load_calibration_params(bus, addr)
        self.__bus = bus
        self.__calib = calib
        self.__port = port
        self.__addr = addr
        self.__data = 0
        return True

    def on_step(self):
        data = bme280.sample(self.__bus, self.__addr, self.__calib)
        if data is None:
            self.stop()
            return False
        self.temperature.write(data.temperature)
        self.pressure.write(data.pressure)
        self.humidity.write(data.humidity)
        self.timestamp.write(data.timestamp)
        self.__data += 1
        return True

    """ IService """

    def _start_impl(self):
        if self.__calib is None:
            self.log_error("No bme280 reader has been set")
            return False
        return super()._start_impl()

    def _stop_impl(self):
        return super()._stop_impl()
