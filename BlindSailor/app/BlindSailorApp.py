#!/usr/bin/python
#coding: utf-8

""" System """

import sys
import os
import time
import argparse

""" Our Stuff """
import sihd
from sihd.app.SihdApp import SihdApp
from sihd.readers.utils.FakeReader import FakeReader
from sihd.readers.file.LineReader import LineReader
from sihd.readers.serial.SerialReader import SerialReader

import BlindSailor
from BlindSailor.readers.Bme280Reader import Bme280Reader
from BlindSailor.handlers.NmeaHandler import NmeaHandler
from BlindSailor.handlers.GsvHandler import GsvHandler
from BlindSailor.handlers.SupportedNmeaHandler import SupportedNmeaHandler
from BlindSailor.gui.WxPythonGui import WxPythonGui
from BlindSailor.gui.curses.BlindCurses import BlindCurses

class BlindSailorApp(SihdApp):

    def __init__(self, *args, **kwargs):
        super().__init__("BlindSailorApp", *args, **kwargs)
        self.configuration.load({
            'channels_input': 'observe',
        })
        self._default_log_level = "info"
        self.set_app_path(sihd.resources.get_dir('tests', 'output'))
        sihd.log.set_color(True)

    def build_services(self):
        self.parse_args()
        self.__make_gui()
        self.__make_readers()
        self.__make_handlers()
        return True

    def __make_gui(self):
        if self.get_arg("curses"):
            gui = BlindCurses('gui', self)
        else:
            gui = WxPythonGui('gui', self)
        gui.configuration.load({
            "runnable_frequency": 1,
            'channels_input': 'observe',
            'links': {
                'gsv_pos': '..supported-nmea-handler.pos',
                'gsv_cap': '..supported-nmea-handler.cap',
                'gsv_speed_over_ground': '..supported-nmea-handler.speed_over_ground',
                'sat_data': '..gsv-handler.output',
                'bme_temperature': '..bme-reader.temperature',
                'bme_pressure': '..bme-reader.pressure',
                'bme_humidity': '..bme-reader.humidity',
                'bme_timestamp': '..bme-reader.timestamp',
            }
        })

        self.gui = gui

    def __make_handlers(self):
        self.__make_gps_handlers()

    def __make_readers(self):
        self.__configure_serial_gps()
        self.__configure_bme()

    def on_init(self):
        self.add_state_observer(self.gui)
        super().on_init()

    #
    # Handlers
    #

    def __make_gps_handlers(self):
        nmea = NmeaHandler("nmea-handler", self)
        nmea.configuration.load({
            "runnable_frequency": 1,
            'channels_input': 'observe',
            'links': {
                'input': '..gps-reader.output',
            }
        })
        gsv = GsvHandler("gsv-handler", self)
        gsv.configuration.load({
            "runnable_frequency": 1,
            'channels_input': 'observe',
            'links': {
                'message': '..nmea-handler.message',
            }
        })
        supp_nmea = SupportedNmeaHandler("supported-nmea-handler", self)
        supp_nmea.configuration.load({
            "runnable_frequency": 1,
            'channels_input': 'observe',
            'links': {
                'message': '..nmea-handler.message',
            }
        })
        self.nmea_handler = nmea
        self.gsv_handler = gsv
        self.supported_nmea_handler = supp_nmea

    """ Readers """

    def __configure_bme(self):
        do_fake = self.get_arg("bme")
        if do_fake:
            service = FakeReader('bme-reader', self)
            service.configuration.load({
                'random': True,
                "runnable_frequency": 10,
                'channels': {
                    'temperature': None,
                    'humidity': None,
                    'pressure': None,
                    'timestamp': None,
                }
            })
        else:
            service = Bme280Reader("bme-reader", self)
            service.configuration.load({
                "port": "/dev/i2c-1",
                "addr": 0x76,
                "runnable_frequency": 1,
                'links': {
                    'output': '..gui.bme_data',
                },
            })
        self.bme280 = service

    def __configure_serial_gps(self):
        path = self.get_arg("gps")
        if path:
            reader = LineReader("gps-reader", self)
            reader.configuration.load({
                "path": path,
                "runnable_frequency": 10,
                "links": {
                }
            })
        else:
            reader = SerialReader("gps-reader", self)
            reader.configuration.load({
                "port": "/dev/ttyS0",
                "baudrate": 9600,
                "timeout": 1,
                "runnable_frequency": 1,
                "links": {
                }
            })
        self.gps_reader = reader

    #
    # Args
    #

    def build_args(self, parser):
        """ Create arguments """
        parser.add_argument("-G", "--gps",
                type=str,
                default=None,
                help="Read gps file")
        parser.add_argument("-B", "--bme",
                action='store_true',
                default=False,
                help="Fake BME")
        parser.add_argument("-C", "--curses",
                action='store_true',
                default=False,
                help="Curses gui")
        parser.add_argument("-t", "--time",
                type=int,
                default=None,
                help="Timer until stop")

    def service_state_changed(self, service, stopped, paused):
        if service == self.gui and stopped:
            self.stop()
