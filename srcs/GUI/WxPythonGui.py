#!/usr/bin/python
#coding: utf-8

""" System """
import os
import os.path
import sys
import logging

wx = None

from sihd.srcs.GUI.IGui import IGui
from sihd.srcs.Core.IConsumer import IConsumer
from sihd.srcs.Core.IThreadedService import IThreadedService

from .MainWindow import MainWindow
from BlindSailor.srcs.Handlers import GsvHandler

class WxPythonGui(IGui, IConsumer, IThreadedService):

    def __init__(self, app=None, name="WxPythonGui"):
        global wx
        if wx is None:
            import wx
        super(WxPythonGui, self).__init__(app=app, name=name)
        #self.set_run_method(self.consume)
        self.__modules = {
            "GPS": False,
            "SAT": False,
            "BME": False,
        }
        self.bme280 = None
        self.gsv = None
        self.nmea = None

    # Config

    def _setup_impl(self):
        if not super()._setup_impl():
            return False
        self._wx_app = wx.App(False)
        self.frame = MainWindow(None, title="Demo")
        if self.__modules["GPS"] is True:
            self.frame.add_gps()
        if self.__modules["BME"] is True:
            self.frame.add_bme()
        if self.__modules["SAT"] is True:
            self.frame.add_sat()
        return True

    def gui_loop(self, *args, **kwargs):
        self.frame.Show()
        self._wx_app.MainLoop()

    def activate_gps(self, nmea, gsv):
        #self.add_to_consume(nmea)
        #self.add_to_consume(gsv)
        nmea.add_observer(self)
        gsv.add_observer(self)
        self.nmea = nmea
        self.gsv = gsv
        self.__modules["GPS"] = True
        self.__modules["SAT"] = True

    def activate_bme(self, bme280):
        #self.add_to_consume(bme280)
        self.bme280 = bme280
        bme280.add_observer(self)
        self.__modules["BME"] = True

    def update_sat(self, data):
        self.frame.satellite_update(data)
        return

    def update_bme(self, data):
        #self.log_info("{}: {}".format(service, data))
        self.frame.bme_update(data)
        return

    def update_gps(self, data):
        #self.log_info("{}: {}".format(service, data))
        return

    # Data

    def update(self, service, *data):
        if service == self.gsv:
            self.update_sat(data[0])
        elif service == self.bme280:
            self.update_bme(data[0])
        elif service == self.nmea:
            self.update_gps(data[0])
        else:
            self.log_info("{}: {}".format(service, data))
        return True

    def on_info(self, reader, info):
        info = info.strip()
        if info != "":
            self.frame.logframe.log(info)

    def on_error(self, reader, err):
        err = err.strip()
        if err != "":
            self.frame.logframe.log(err)
        self.stop(True)

    # Services

    def _stop_impl(self):
        ret = super()._stop_impl()
        if ret:
            if self.frame:
                self.frame.Close()
        return ret

    def _start_impl(self):
        return super()._start_impl()
