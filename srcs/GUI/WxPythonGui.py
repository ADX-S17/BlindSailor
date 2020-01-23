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
        self.set_run_method(self.consume)
        if app:
            self.get_app().set_loop(self.start_gui)

    def _setup_impl(self):
        if not super()._setup_impl():
            return False
        self._wx_app = wx.App(False)
        self.frame = MainWindow(None, title="Demo")
        return True

    def start_gui(self, *args, **kwargs):
        self.frame.Show()
        self._wx_app.MainLoop()

    def consumed(self, service, data):
        if isinstance(service, GsvHandler):
            """
            self.frame.logframe.log(str(data))
            """
            for k, v in data.items():
                print(k, v)
        return True

    """
    def update(self, handler, dic):
        if isinstance(handler, NmeaHandler):
            self.frame.logframe.log(str(dic))
            print(dic)
        return True
    """

    def on_info(self, reader, info):
        info = info.strip()
        if info != "":
            self.frame.logframe.log(info)

    def on_error(self, reader, err):
        err = err.strip()
        if err != "":
            self.frame.logframe.log(err)
        self.stop(True)

    def _stop_impl(self):
        ret = super()._stop_impl()
        if ret:
            if self.frame:
                self.frame.Close()
        return ret

    # Services

    def _start_impl(self):
        if self.get_app() is None:
            self.start_gui()
        return super()._start_impl()
