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
        engine = pyttsx3.init()
        engine.setProperty('voice', 'french')
        engine.setProperty('rate', 100)
        self.__tts_engin = engine
        self.__modules = {}

    def tts(self, text):
        engine = self.__tts_engine
        engine.say(text)
        engine.runAndWait()

    def setup_windows(self):
        super().setup_windows()
        self.main = self.get_window("main")
        self.main.box()
        self.log_info("Curses rolling")
        self.set_main_str("Hello")
        self.refresh_windows()
        self.update_panels(True)

    def activate_gps(self, nmea, gsv):
        #self.add_to_consume(nmea)
        #self.add_to_consume(gsv)
        nmea.add_observer(self)
        gsv.add_observer(self)
        self.__modules["GPS"] = True

    def activate_bme(self, bme280):
        #self.add_to_consume(bme280)
        bme280.add_observer(self)
        self.__modules["BME"] = True

    def set_main_str(self, s):
        win = self.main
        win.clear()
        win.box()
        win.addstr(2, 3, "Main window: ")
        win.addstr(3, 3, s)

    def input(self, key, curses):
        char = curses.keyname(key).decode()
        self.set_main_str("Pressed: {}".format(char))
        if char == 'q':
            return False
        elif char == 'l':
            self.log_info("Logging !")
        elif char == '1':
            self.set_main_str("Cap = 90")
        self.refresh_windows()
        self.update_panels(True)
        return True

    def resize(self):
        super().resize()
        self.clear_windows()
        self.refresh_windows(True)
        self.update_panels(True)

    def update(self, service, *data):
        self.log_info("{}: {}".format(service, data))
