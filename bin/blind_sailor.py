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
    if app.setup_app() is False:
        sys.exit(1)
    app.start()
    app.loop()
