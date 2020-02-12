#!/usr/bin/python
#coding: utf-8

""" System """
import os
import sys
import time

import sihd
from sihd.srcs.GUI.Curses.ICursesGui import ICursesGui

pyttsx3 = None

class BlindCurses(ICursesGui):

    def __init__(self, app=None, name="BlindCurses"):
        super(BlindCurses, self).__init__(app=app, name=name)
        global pyttsx3
        if pyttsx3 is None:
            import pyttsx3
        self._set_default_conf({})
        engine = pyttsx3.init()
        engine.setProperty('voice', 'french')
        engine.setProperty('rate', 100)
        self.__tts_engine = engine
        self.__modules = {}
        self.bme_data = {}
        self.gps_data = {}
        self.sat_data = {}
        self.__bme280 = None
        self.__nmea = None
        self.__gsv = None

    def _setup_impl(self):
        ret = super()._setup_impl()
        return True

    def tts(self, text):
        engine = self.__tts_engine
        engine.say(text)
        engine.runAndWait()

    def setup_windows(self):
        super().setup_windows()
        self.main = self.get_window("main")
        self.main.box()
        self.log_info("Curses rolling")
        self.refresh_windows()
        self.update_panels(True)

    def activate_gps(self, nmea, gsv):
        #self.add_to_consume(nmea)
        #self.add_to_consume(gsv)
        nmea.add_observer(self)
        gsv.add_observer(self)
        self.__nmea = nmea
        self.__gsv = gsv
        self.__modules["GPS"] = True

    def activate_bme(self, bme280):
        #self.add_to_consume(bme280)
        bme280.add_observer(self)
        self.__bme280 = bme280
        self.__modules["BME"] = True

    def set_main(self, data):
        win = self.main
        win.clear()
        win.box()
        i = 2
        for k, v in data.items():
            win.addstr(i, 3, "{} = {}".format(k, v))
            i += 1

    def update_bme(self, data):
        self.bme_data = data
        self.set_main(data)

    def update_gps(self, data):
        self.gps_data = data
        self.set_main(data)

    def update_satellite(self, data):
        self.sat_data = data

    def say_from_data(self, data):
        val = self.bme_data.get(data, None)
        if val is None:
            val = self.gps_data.get(data, None)
        if val is None:
            self.log_error("No data for key: {}".format(data))
            return False
        self.tts("{} est {}".format(data, val))
        return True

    def input(self, key, curses):
        char = curses.keyname(key).decode()
        self.log_debug("Pressed: {}".format(char))
        if char == 'q':
            return False
        elif char == 'l':
            self.log_info("Logging !")
        elif char == '1':
            self.say_from_data("latitude")
        elif char == '2':
            self.say_from_data("longitude")
        self.refresh_windows()
        self.update_panels(True)
        return True

    def resize(self):
        super().resize()
        self.clear_windows()
        self.refresh_windows(True)
        self.update_panels(True)

    def update(self, service, data):
        if service == self.__bme280:
            self.update_bme(data)
        elif service == self.__nmea:
            self.update_gps(data)
        elif service == self.__gsv:
            self.update_satellite(data)
        self.log_info("{}: {}".format(service, data))
