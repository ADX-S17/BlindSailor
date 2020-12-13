#!/usr/bin/python
#coding: utf-8

""" System """
import os
import sys
from sihd.gui.wxpython.utils.LogFrame import LogFrame
from .GpsFrame import GpsFrame
from .BmeFrame import BmeFrame
from .SatelliteFrame import SatelliteFrame

import wx
import wx.lib.agw.aui as aui

class MainWindow(wx.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_interior_window_components()
        self.create_exterior_window_components()

    def add_bme(self):
        notebook = self.notebook
        bmeframe = BmeFrame(notebook)
        notebook.AddPage(bmeframe, 'BME')
        self.SetClientSize(notebook.GetBestSize())
        self.bmeframe = bmeframe

    def add_gps(self):
        notebook = self.notebook
        gpsframe = GpsFrame(notebook)
        notebook.AddPage(gpsframe, 'GPS')
        self.SetClientSize(notebook.GetBestSize())
        self.gpsframe = gpsframe

    def add_sat(self):
        notebook = self.notebook
        satframe = SatelliteFrame(notebook)
        notebook.AddPage(satframe, 'SAT')
        self.SetClientSize(notebook.GetBestSize())
        self.satframe = satframe

    def create_interior_window_components(self):
        notebook = wx.Notebook(self)
        #notebook = aui.AuiNotebook(self)
        sizer = wx.BoxSizer()
        sizer.Add(notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)
        logframe = LogFrame(notebook)
        logframe.add_handler()
        notebook.AddPage(logframe, 'Logger')
        self.SetClientSize(notebook.GetBestSize())
        self.notebook = notebook
        self.logframe = logframe

    def satellite_update(self, data):
        wx.CallAfter(self.satframe.update, data)

    def bme_update(self, temperature, pressure, humidity):
        wx.CallAfter(self.bmeframe.change_temperature, temperature)
        wx.CallAfter(self.bmeframe.change_pressure, pressure)
        wx.CallAfter(self.bmeframe.change_humidity, humidity)

    # Exterior

    def create_exterior_window_components(self):
        ''' Create "exterior" window components, such as menu and status
            bar. '''
        self.create_menu()
        self.CreateStatusBar()
        self.SetTitle("BlindSailor")

    def create_menu(self):
        fileMenu = wx.Menu()
        for id, label, helpText, handler in \
            [
                (wx.ID_ABOUT, '&About', 'Information about this program', self.OnAbout),
                (wx.ID_EXIT, 'E&xit', 'Terminate the program', self.OnExit)
            ]:
            if id == None:
                fileMenu.AppendSeparator()
            else:
                item = fileMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File') # Add the fileMenu to the MenuBar
        self.SetMenuBar(menuBar)  # Add the menuBar to the Frame

    # Event handlers:

    def OnAbout(self, event):
        dialog = wx.MessageDialog(self, 'A WxPython Gui', 'About Sample', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def OnExit(self, event):
        self.logframe.remove_handler()
        self.Close()
