#!/usr/bin/python
#coding: utf-8

""" System """
import os
import sys
import logging

from sihd.srcs import Core

try:
    import wx
    Panel = wx.Panel
except ImportError:
    wx = None
    Panel = object

class CursesHandler(logging.Handler):

    def __init__(self, panel):
        logging.Handler.__init__(self)
        self.panel = panel

    def emit(self, record):
        msg = self.format(record)
        panel = self.panel
        panel.log(msg)

class LogFrame(Panel):

    def __init__(self, *args, **kwargs):
        super(LogFrame, self).__init__(*args, **kwargs)
        self.create_controls()
        self.bind_events()
        self.do_layout()
        self.add_logger()

    def add_logger(self):
        log_handler = CursesHandler(self)
        log_handler.setFormatter(Core.ILoggable.get_formatter())
        Core.ILoggable.logger.addHandler(log_handler)
        self._log_handler = log_handler

    def remove_logger(self):
        Core.ILoggable.logger.removeHandler(self._log_handler)

    def create_controls(self):
        self.logger = wx.TextCtrl(self,
                size=(800, 400),
                #style=wx.TE_MULTILINE | wx.TE_READONLY)
                style=wx.TE_MULTILINE)

    def bind_events(self):
        self.logger.Bind(wx.EVT_TEXT, self.on_text_entered)

    def on_text_entered(self, event):
        text = event.GetString()

    def do_layout(self):
        boxSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        boxSizer.Add(self.logger)
        self.SetSizerAndFit(boxSizer)

    # Callback methods:

    def log(self, message):
        self.__log('Message: {}'.format(message))

    # Helper method(s):

    def __log(self, message):
        self.logger.AppendText('%s\n'%message)
