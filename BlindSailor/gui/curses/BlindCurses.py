#!/usr/bin/python
#coding: utf-8

""" System """
import os
import sys
import time

import sihd
from sihd.gui.curses.ACursesGui import ACursesGui

pyttsx3 = None

class BlindCurses(ACursesGui):

    def __init__(self, app=None, name="BlindCurses"):
        super(BlindCurses, self).__init__(app=app, name=name)
        global pyttsx3
        if pyttsx3 is None:
            import pyttsx3
        self._set_default_conf({})
        engine = pyttsx3.init()
        engine.setProperty('voice', 'french')
        engine.setProperty('rate', 170)
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

        self.main.addstr(2, 5, "Cursed Sailor")

        #Height - Width - Y - X
        win1, panel1 = self.create_panel(25, 40, 3, 5)
        win1.addstr(1, 2, "Panel_GPS")
        win1.box()
        self.add_panel(win1, panel1, "Panel_GPS")

        win2, panel2 = self.create_panel(10, 35, 3, 50)
        win2.addstr(1, 2, "Panel_BME")
        win2.box()
        self.add_panel(win2, panel2, "Panel_BME")

        panel1.top()

        self.win_gps = win1
        self.win_bme = win2

        self.log_info("Curses rolling")

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

    def set_win(self, win, data, title=None):
        win.erase()
        win.box()
        if title:
            self.win_add_str(win, 1, 2, title)
            i = 3
        else:
            i = 2
        for k, v in data.items():
            val = v
            if isinstance(v, dict):
                val = "{"
            if isinstance(val, float):
                val = "{0:.3f}".format(val)
            self.win_add_str(win, i, 2, "{} = {}".format(k, val))
            i += 1
            if isinstance(v, dict):
                for child_k, child_v in v.items():
                    if isinstance(child_v, float):
                        child_v = "{0:.3f}".format(child_v)
                    self.win_add_str(win, i, 6, "{} = {}".format(child_k, child_v))
                    i += 1
                self.win_add_str(win, i, 2, "}")
                i += 1
        win.refresh()

    def update_bme(self, data):
        self.bme_data = data
        self.set_win(self.win_bme, data, title="BME")

    def update_gps(self, data):
        self.gps_data = data
        self.set_win(self.win_gps, data, title="GPS")

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
        refresh = True
        if char == 'q':
            return False
        elif char == 'r':
            self.resize()
        elif char == 'l':
            self.log_info("Logging !")
        elif char == '1':
            self.say_from_data("latitude")
        elif char == '2':
            self.say_from_data("longitude")
        else:
            refresh = False
        if refresh:
            self.refresh_windows()
            self.update_panels(True)
        return True

    def resize(self):
        super().resize()
        self.clear_windows()
        self.main.box()
        self.main.addstr(2, 5, "Cursed Sailor")
        self.update_bme(self.bme_data)
        self.update_gps(self.gps_data)
        self.refresh_windows(True)
        self.update_panels(True)

    def update(self, service, data):
        try:
            if service == self.__bme280:
                self.update_bme(data)
            elif service == self.__nmea:
                self.update_gps(data)
            elif service == self.__gsv:
                self.update_satellite(data)
        except Exception as e:
            self.stop()
            self.log_error(e)
        #self.log_info("{}: {}".format(service, data))
