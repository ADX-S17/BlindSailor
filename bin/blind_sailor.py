#!/usr/bin/python
#coding: utf-8

""" System """

import sys
import os
import time

from BlindSailor.srcs.App import BlindSailorApp
from sihd.srcs import Core

if __name__ == '__main__':
    app = BlindSailorApp()
    app.set_args("--gps tests/resources/gps/trace_gps --bme tests/resources/bme/trace_gps")
    if app.setup_app() is False:
        sys.exit(1)
    try:
        app.start_all()
        app.loop()
    except Exception as e:
        app.stop()
        raise Exception(e)
    app.stop()
