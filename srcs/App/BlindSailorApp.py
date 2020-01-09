#!/usr/bin/python
#coding: utf-8

""" System """
from __future__ import print_function
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
        self.load_app_conf()
        sihd.Utilities.ILoggable.set_color(True)

    def _setup_app_impl(self):
        self.parse_args()
        self.nmea_handler = BlindSailor.Handlers.NmeaHandler(self)
        self.__configure_serial_gps()
        return True

    def __configure_serial_gps(self):
        if self.args.gps:
            reader = sihd.Readers.sys.LineReader(self.args.gps, app=self)
            self.gps_reader = reader
        else:
            serial = sihd.Readers.SerialReader(self)
            serial.set_conf({
                "port": "/dev/ttyAMA0",
                "baudrate": 9600,
                "timeout": 1.0,
            })
            self.gps_reader = serial
        self.gps_reader.add_observer(self.nmea_handler)

    def define_args(self, parser):
        """ Create arguments """
        parser.add_argument("-G", "--gps",
                type=str,
                default=None,
                help="Read gps file")
        parser.add_argument("-S", "--stats",
                action='store_true',
                default=False,
                help="Print stats when printing results")
        parser.add_argument("-t", "--time",
                type=int,
                default=None,
                help="Timer until stop")

    def service_state_changed(self, service, stopped, paused):
        pass
