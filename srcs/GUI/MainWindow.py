#!/usr/bin/python
#coding: utf-8

""" System """
import os
import sys
import logging

from .LogFrame import LogFrame
from .GpsFrame import GpsFrame
from .BmeFrame import BmeFrame
from .SatelliteFrame import SatelliteFrame

try:
    import wx
    Frame = wx.Frame
    import wx.lib.agw.aui as aui
except ImportError:
    wx = None
    Frame = object

class MainWindow(Frame):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.CreateInteriorWindowComponents()
        self.CreateExteriorWindowComponents()

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

    def CreateInteriorWindowComponents(self):
        notebook = wx.Notebook(self)
        #notebook = aui.AuiNotebook(self)
        sizer = wx.BoxSizer()
        sizer.Add(notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)
        logframe = LogFrame(notebook)
        notebook.AddPage(logframe, 'Logger')
        self.SetClientSize(notebook.GetBestSize())
        self.notebook = notebook
        self.logframe = logframe

    def satellite_update(self, data):
        self.satframe.update(data)

    def bme_update(self, data):
        self.bmeframe.update(data)

    # Exterior

    def CreateExteriorWindowComponents(self):
        ''' Create "exterior" window components, such as menu and status
            bar. '''
        self.CreateMenu()
        self.CreateStatusBar()
        self.SetTitle()

    def CreateMenu(self):
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
        dialog = wx.MessageDialog(self, 'A WxPython Gui',
                                    'About Sample', wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def OnExit(self, event):
        self.Close()  # Close the main window.

    def SetTitle(self):
        # MainWindow.SetTitle overrides wx.Frame.SetTitle, so we have to
        # call it using super:
        super(MainWindow, self).SetTitle('BlindSailor')
