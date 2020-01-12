#!/usr/bin/python
#coding: utf-8

""" System """

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
        path = os.path.join(os.path.dirname(__file__), "resources", "gps_output")
        self.app.set_args("--gps={}".format(path))
        if self.app.setup_app() is False:
            sys.exit(1)
        test_handler = TestHandler()
        self.app.nmea_handler.add_observer(test_handler)
        self.app.start()
        test_handler.start()
        self.app.loop(timeout=2)
        test_handler.stop()

    def test_gps_reader(self):
        if self.app.setup_app() is False:
            sys.exit(1)
        test_handler = TestHandler()
        self.app.nmea_handler.add_observer(test_handler)
        self.app.start()
        test_handler.start()
        self.app.loop(timeout=5)
        test_handler.stop()

if __name__ == '__main__':
    unittest.main(verbosity=2)
