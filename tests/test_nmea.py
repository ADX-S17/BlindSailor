#!/usr/bin/python
#coding: utf-8

""" System """
from __future__ import print_function
import os
import sys

import unittest

import sihd
import BlindSailor

class TestHandler(sihd.Handlers.IHandler):

    def __init__(self, app=None, name="NmeaHandler"):
        super(TestHandler, self).__init__(app=app, name=name)

    def handle(self, reader, data):
        print(data)

class TestNmea(unittest.TestCase):

    def setUp(self):
        self.app = BlindSailor.App.BlindSailorApp()

    def tearDown(self):
        self.app.stop()

    def test_good_file(self):
        if self.app.setup_app() is False:
            sys.exit(1)
        path = os.path.join(os.path.dirname(__file__), "resources", "gps_output")
        reader = sihd.Readers.sys.LineReader(path)
        test_handler = TestHandler()
        reader.add_observer(self.app.nmea_handler)
        self.app.nmea_handler.add_observer(test_handler)
        self.app.start()
        test_handler.start()
        reader.start()
        self.app.loop(timeout=5)
        reader.stop()
        test_handler.stop()

if __name__ == '__main__':
    unittest.main(verbosity=2)
