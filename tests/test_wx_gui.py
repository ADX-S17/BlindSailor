#!/usr/bin/python
#coding: utf-8

""" System """

import os
import sys

import unittest
import time

import sihd
import BlindSailor
from BlindSailor.gui.WxPythonGui import WxPythonGui

logger = sihd.log.setup('info')

class TestGui(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gui(self):
        gui = WxPythonGui()
        gui.configuration.load({
            'modules': {
                'BME': True,
                'SAT': True,
                'GPS': True,
            }
        })
        gui.start()
        sihd.tree.dump()
        time.sleep(20)
        gui.stop()

if __name__ == '__main__':
    unittest.main(verbosity=2)
