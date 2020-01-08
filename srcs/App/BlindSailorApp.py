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
        self.nmea_handler = BlindSailor.Handlers.NmeaHandler(self)
        return True

    def define_args(self, parser):
        """ Create arguments """
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
