#!/usr/bin/python
#coding: utf-8

""" System """
import os
import os.path
import sys
import logging

wx = None

from sihd.srcs.GUI.IGui import IGui
from .MainWindow import MainWindow
from BlindSailor.srcs.Handlers import NmeaHandler

class WxPythonGui(IGui):

    def __init__(self, app=None, name="WxPythonGui"):
        global wx
        if wx is None:
            import wx
        super(WxPythonGui, self).__init__(app=app, name=name)
        if app:
            self.get_app().set_loop(self.start_gui)

    def start_gui(self, *args, **kwargs):
        app = wx.App(False)
        self._app = app
        self.frame = MainWindow(None, title="Demo")
        self.frame.Show()
        app.MainLoop()

    def handle(self, handler, dic):
        if isinstance(handler, NmeaHandler):
            print(dic)
        #comm
        """
        if self.frame and self.frame.logframe:
            message = message.strip()
            if message != "":
                self.frame.logframe.log(message)
            if message == "stop":
                self.stop(True)
        """
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

    def _stop_impl(self):
        if self.frame:
            self.frame.Close()
        return True

    # Services

    def _pause_impl(self):
        return True

    def _resume_impl(self):
        return True

    def _start_impl(self):
        if self.get_app() is None:
            self.start_gui()
        return True

    def _stop_impl(self):
        return True
