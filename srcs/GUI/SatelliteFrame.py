#!/usr/bin/python
#coding: utf-8

""" System """
import os
import sys
import logging

try:
    import wx
    Panel = wx.Panel
    import wx.lib.agw.aui as aui
    import wx.lib.mixins.inspection as wit
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
    from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
    matplotlib.use('WXAgg')
except ImportError:
    wx = None
    Panel = object

class SatelliteFrame(Panel):
    def __init__(self, parent, id=-1, dpi=None, **kwargs):
        wx.Panel.__init__(self, parent, id=id, **kwargs)
        fig = matplotlib.figure.Figure(dpi=dpi, figsize=(2, 2))
        ax = fig.add_subplot(111, polar=True)
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.set_rlim(0, 90)
        self.figure = fig
        self.ax = ax
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Realize()
        self.annotations = []
        self.color_bar = fig.colorbar(c)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.SetSizer(sizer)

    def get_figure(self):
        return self.figure

    def plot(self, data):
        SV_azimuth_rad = data["SV_azimuth_rad"]
        SV_elevation = data["SV_elevation"]
        SV_SNR = data["SV_SNR"]
        SV_PRN_num = data["SV_PRN_num"]
        Nb_SV_In_View = data["Nb_SV_In_View"]

        fig = self.figure
        ax = self.ax
        ax.clear()
        c = ax.scatter(SV_azimuth_rad, SV_elevation, c=SV_SNR, s=350,
                            cmap='rainbow', alpha=0.75, vmin=0)
        if self.annotations:
            for ann in self.annotations:
                ann.remove()
            self.annotations = []
        for i, txt in enumerate(SV_PRN_num):
            ann = ax.annotate(txt, (SV_azimuth_rad[i], SV_elevation[i]))
            self.annotations.append(ann)
        ax.set_title("%d GPS satellites in view" % Nb_SV_In_View, fontsize=18)
        try:
            self.canvas.draw()
        except RuntimeError:
            pass
