#!/usr/bin/python
#coding: utf-8

""" System """

import sys
import os
import time
import argparse

""" Our Stuff """
import sihd
import BlindSailor

class BlindSailorApp(sihd.App.IApp):

    def __init__(self):
        super(BlindSailorApp, self).__init__("BlindSailorApp")
        self.set_module_path(BlindSailor)
        sihd.Core.ILoggable.set_color(True)

    def _setup_app_impl(self):
        self.parse_args()
        self.__make_gui()
        self.__make_readers()
        self.__make_handlers()
        self.__make_links()
        return True

    def __make_links(self):
        #self.nmea_handler.add_to_consume(self.gps_reader)
        self.gps_reader.add_observer(self.nmea_handler)
        self.gui.activate_gps(self.supported_nmea_handler, self.gsv_handler)
        self.gui.activate_bme(self.bme280_reader)

    def __make_gui(self):
        if self.get_arg("curses"):
            gui = BlindSailor.GUI.BlindCurses(self)
        else:
            gui = BlindSailor.GUI.WxPythonGui(self)
        self.gui = gui

    def __make_handlers(self):
        self.__make_gps_handlers()

    def __make_readers(self):
        self.__configure_serial_gps()
        self.__configure_bme()

    """ Handlers """

    def __make_gps_handlers(self):
        nmea_handler = BlindSailor.Handlers.NmeaHandler(self)
        gsv_handler = BlindSailor.Handlers.GsvHandler(self)
        supported_nmea_handler = BlindSailor.Handlers.SupportedNmeaHandler(self)
        self.nmea_handler = nmea_handler
        self.gsv_handler = gsv_handler
        self.supported_nmea_handler = supported_nmea_handler
        nmea_handler.add_observer(gsv_handler)
        nmea_handler.add_observer(supported_nmea_handler)

    """ Readers """

    def __configure_bme(self):
        path = self.get_arg("bme")
        if path:
            reader = sihd.Readers.sys.LineReader(app=self, name="BmeReader")
            reader.set_conf({
                "path": path,
                "thread_frequency": 1,
            })
        else:
            reader = BlindSailor.Readers.Bme280Reader(app=self)
            reader.set_conf({
                "port": "/dev/i2c-1",
                "addr": 0x76,
                "thread_frequency": 1,
            })
        self.bme280_reader = reader
        #reader.set_service_multiprocess()

    def __configure_serial_gps(self):
        path = self.get_arg("gps")
        if path:
            reader = sihd.Readers.sys.LineReader(app=self, name="GpsReader")
            reader.set_conf({
                "path": path,
                "thread_frequency": 1,
            })
        else:
            reader = sihd.Readers.SerialReader(app=self)
            reader.set_conf({
                "port": "/dev/ttyAMA0",
                "baudrate": 9600,
                "timeout": 1,
                "thread_frequency": 1,
            })
        self.gps_reader = reader
        #self.gps_reader.set_service_multiprocess()

    """ Arguments """

    def define_args(self, parser):
        """ Create arguments """
        parser.add_argument("-G", "--gps",
                type=str,
                default=None,
                help="Read gps file")
        parser.add_argument("-B", "--bme",
                type=str,
                default=None,
                help="Read gps file")
        parser.add_argument("-C", "--curses",
                action='store_true',
                default=False,
                help="Curses gui")
        parser.add_argument("-t", "--time",
                type=int,
                default=None,
                help="Timer until stop")

    def service_state_changed(self, service, stopped, paused):
        pass
