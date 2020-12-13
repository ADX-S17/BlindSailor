#!/usr/bin/python
#coding: utf-8

""" System """

import os
import sys

import unittest
import time

import sihd
import BlindSailor
from BlindSailor.app.BlindSailorApp import BlindSailorApp

logger = sihd.log.setup('info')

class TestApp(unittest.TestCase):

    def setUp(self):
        sihd.resources.add('tests', 'resources', 'gps')
        pass

    def tearDown(self):
        time.sleep(1)

    def test_app(self):
        app = BlindSailorApp("app-test")
        app.configuration.load({
            'children': {
                'gui': {
                    'modules': {
                        'BME': True,
                        'SAT': True,
                        'GPS': True,
                    }
                },
            },
        })
        app.set_args("--bme --gps " + sihd.resources.get('trace_gps'))
        app.start()
        sihd.tree.dump()
        i = 3
        while app.gui.is_active() and i > 0:
            logger.info("Remaining: %d" % i)
            time.sleep(1)
            i -= 1

if __name__ == '__main__':
    unittest.main(verbosity=2)
