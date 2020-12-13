#!/usr/bin/python
#coding: utf-8

""" System """
import os
import os.path
import sys

wx = None

from sihd.gui.wxpython.AWxPythonGui import AWxPythonGui
from .MainWindow import MainWindow

class WxPythonGui(AWxPythonGui):

    def __init__(self, name="BlindSailorGui", app=None):
        global wx
        if wx is None:
            import wx
        super().__init__(app=app, name=name)
        self.configuration.add_defaults({
            'modules': {
                'GPS': False,
                'BME': False,
                'SAT': False,
            },
        })
        self.add_channel_input("gsv_pos")
        self.add_channel_input("gsv_cap")
        self.add_channel_input("gsv_speed_over_ground")
        self.add_channel_input("sat_data")
        self.add_channel_input("bme_timestamp")
        self.add_channel_input("bme_humidity")
        self.add_channel_input("bme_temperature")
        self.add_channel_input("bme_pressure")

    # Config

    def on_setup(self, config):
        return super().on_setup(config)

    def build_wx_frames(self, app):
        config = self.configuration
        self.main_window = MainWindow(None, title="Demo")
        modules = config.get('modules')
        if modules.get("GPS", False):
            self.main_window.add_gps()
        if modules.get("BME", False):
            self.main_window.add_bme()
        if modules.get("SAT", False):
            self.main_window.add_sat()
        self.main_window.Show()

    def update_sat(self, data):
        self.main_window.satellite_update(data)
        return

    def update_bme(self, temperature, pressure, humidity):
        self.main_window.bme_update(temperature, pressure, humidity)

    def update_gsv_pos(self, data):
        return

    def update_gsv_cap(self, data):
        return

    def update_gsv_sog(self, data):
        return

    def handle(self, channel):
        if channel == self.bme_timestamp:
            temperature = self.bme_temperature.read()
            pressure = self.bme_pressure.read()
            humidity = self.bme_humidity.read()
            self.update_bme(temperature, pressure, humidity)
        elif channel == self.sat_data:
            data = channel.read()
            if data is not None:
                self.update_sat(data)
        elif channel == self.gsv_pos:
            data = channel.read()
            if data is not None:
                self.update_gsv_pos(data)
        elif channel == self.gsv_cap:
            data = channel.read()
            if data is not None:
                self.update_gsv_cap(data)
        elif channel == self.gsv_speed_over_ground:
            data = channel.read()
            if data is not None:
                self.update_gsv_sog(data)

    #
    # Service
    #

    def on_stop(self):
        if self.main_window:
            self.main_window.Close()
        return super().on_stop()
