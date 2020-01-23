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

class WxLogHandler(logging.Handler):

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
        self._log_handler = None
        self.add_logger()

    def __del__(self):
        self.remove_logger()

    def add_logger(self):
        self.remove_logger()
        log_handler = WxLogHandler(self)
        log_handler.setFormatter(Core.ILoggable.get_formatter())
        Core.ILoggable.logger.addHandler(log_handler)
        self._log_handler = log_handler

    def remove_logger(self):
        logger = self._log_handler
        if logger:
            Core.ILoggable.logger.removeHandler(logger)
            self._log_handler = None

    def create_controls(self):
        self.logger = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY)

    def bind_events(self):
        self.logger.Bind(wx.EVT_TEXT, self.on_text_entered)

    def on_text_entered(self, event):
        text = event.GetString()

    def do_layout(self):
        boxSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        boxSizer.Add(self.logger, border=5, proportion=1, flag=wx.ALL | wx.EXPAND)
        self.SetSizerAndFit(boxSizer)

    # Callback methods:

    def log(self, message):
        self.__log('Message: {}'.format(message))

    # Helper method(s):

    def __log(self, message):
        self.logger.AppendText('%s\n'%message)
