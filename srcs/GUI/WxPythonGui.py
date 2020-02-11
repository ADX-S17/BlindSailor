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
            "BME": False,
        }

    # Config

    def _setup_impl(self):
        if not super()._setup_impl():
            return False
        self._wx_app = wx.App(False)
        self.frame = MainWindow(None, title="Demo")
        if self.__modules["GPS"] is True:
            self.frame.AddGps()
        if self.__modules["BME"] is True:
            self.frame.AddBme()
        return True

    def gui_loop(self, *args, **kwargs):
        self.frame.Show()
        self._wx_app.MainLoop()

    def activate_gps(self, nmea, gsv):
        #self.add_to_consume(nmea)
        #self.add_to_consume(gsv)
        nmea.add_observer(self)
        gsv.add_observer(self)
        self.__modules["GPS"] = True

    def activate_bme(self, bme280):
        #self.add_to_consume(bme280)
        bme280.add_observer(self)
        self.__modules["BME"] = True

    # Data

    def consumed(self, service, data):
        if isinstance(service, GsvHandler):
            """
            self.frame.logframe.log(str(data))
            for k, v in data.items():
                print(k, v)
            """
            pass
        self.log_info(service, data)
        return True

    def update(self, service, *data):
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
