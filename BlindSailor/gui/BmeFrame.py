#!/usr/bin/python
#coding: utf-8

""" System """
import os
import sys
try:
    import wx
    Panel = wx.Panel
except ImportError:
    wx = None
    Panel = object

class BmeFrame(Panel):
    ''' The BmeFrame class is a wx.Panel that creates a bunch of controls
        and handlers for callbacks. Doing the layout of the controls is
        the responsibility of subclasses (by means of the doLayout()
        method). '''

    def __init__(self, *args, **kwargs):
        super(BmeFrame, self).__init__(*args, **kwargs)
        self.createControls()
        self.doLayout()

    def createControls(self):
        self.temperatureLabel = wx.StaticText(self, label="Temperature (C):")
        self.temperatureCtrl = wx.TextCtrl(self, style=wx.TE_READONLY)

        self.humidityLabel = wx.StaticText(self, label="Humidity (%):")
        self.humidityCtrl = wx.TextCtrl(self, style=wx.TE_READONLY)

        self.pressureLabel = wx.StaticText(self, label="Pression (HPa):")
        self.pressureCtrl = wx.TextCtrl(self, style=wx.TE_READONLY)

    def doLayout(self):
        ''' Layout the controls by means of sizers. '''

        # A horizontal BoxSizer will contain the GridSizer (on the left)
        # and the logger text control (on the right):
        boxSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        # A GridSizer will contain the other controls:
        gridSizer = wx.FlexGridSizer(rows=5, cols=2, vgap=10, hgap=10)

        # Prepare some reusable arguments for calling sizer.Add():
        gridSizer.Add(self.temperatureLabel)
        gridSizer.Add(self.temperatureCtrl, flag=wx.EXPAND)

        gridSizer.Add(self.humidityLabel)
        gridSizer.Add(self.humidityCtrl, flag=wx.EXPAND)

        gridSizer.Add(self.pressureLabel)
        gridSizer.Add(self.pressureCtrl, flag=wx.EXPAND)

        boxSizer.Add(gridSizer, border=5, flag=wx.ALL)

        self.SetSizerAndFit(boxSizer)

    def change_temperature(self, value):
        self.temperatureCtrl.SetValue("{}".format(value))

    def change_humidity(self, value):
        self.humidityCtrl.SetValue("{}".format(value))

    def change_pressure(self, value):
        self.pressureCtrl.SetValue("{}".format(value))

    def update(self, data):
        self.change_temperature(data['temperature'])
        self.change_humidity(data['humidity'])
        self.change_pressure(data['pressure'])
