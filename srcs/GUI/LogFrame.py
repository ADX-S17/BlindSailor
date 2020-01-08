#!/usr/bin/python
#coding: utf-8

""" System """
from __future__ import print_function

import os
import sys
import logging

try:
    import wx
    Panel = wx.Panel
except ImportError:
    wx = None
    Panel = object

class LogFrame(Panel):

    def __init__(self, *args, **kwargs):
        super(LogFrame, self).__init__(*args, **kwargs)
        self.createControls()
        self.bindEvents()
        self.doLayout()

    def createControls(self):
        self.logger = wx.TextCtrl(self,
                size=(800, 400),
                #style=wx.TE_MULTILINE | wx.TE_READONLY)
                style=wx.TE_MULTILINE)

    def bindEvents(self):
        self.logger.Bind(wx.EVT_TEXT, self.onTextEntered)

    def onTextEntered(self, event):
        text = event.GetString()

    def doLayout(self):
        boxSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        boxSizer.Add(self.logger)
        self.SetSizerAndFit(boxSizer)

    # Callback methods:

    def log(self, message):
        self.__log('Message: {}'.format(message))

    # Helper method(s):

    def __log(self, message):
        self.logger.AppendText('%s\n'%message)
