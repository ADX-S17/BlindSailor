#!/usr/bin/python
#coding: utf-8

""" System """

import time
import os

smbus2 = None
bme280 = None

from sihd.srcs.Readers.IReader import IReader

class Bme280Reader(IReader):
    
    def __init__(self, app=None, name="Bme280Reader"):
        global bme280
        if bme280 is None:
            import bme280
        global smbus2
        if smbus2 is None:
            import smbus2
        super(Bme280Reader, self).__init__(app=app, name=name)
        self.__bus = None
        self.__calib = None
        self._set_default_conf({
            "port": 0,
            "addr": 0,
        })
        self.set_run_method(self._sample)

    """ IConfigurable """

    def _setup_impl(self):
        super(Bme280Reader, self)._setup_impl()
        addr = self.get_conf("addr")
        port = self.get_conf("port")
        if port and addr:
            self.set_source(port, addr)
        if not self.__calib:
            return False
        return True

    """ Reader """

    def set_source(self, port, addr):
        self.__data = 0
        bus = smbus2.SMBus(port)
        calib = bme280.load_calibration_params(bus, addr)
        self.__bus = bus
        self.__calib = calib
        self.__port = port
        self.__addr = addr
        s = "Reading on port: {} - addr: {}".format(port, addr)
        self.log_info(s)
        return True

    def _sample(self):
        data = bme280.sample(self.__bus, self.__addr, self.__calib)
        if data is None:
            self.stop()
            return False
        self.produce(data)
        self.__data += 1
        return True

    """ IService """

    def _start_impl(self):
        if self.__calib is None:
            self.log_error("No bme280 reader has been set")
            return False
        return super(Bme280Reader, self)._start_impl()

    def _stop_impl(self):
        if self._serial:
            self._serial.close()
            self._serial = None
        return super(Bme280Reader, self)._stop_impl()
