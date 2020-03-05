#!/usr/bin/python
#coding: utf-8

""" System """
from sihd.srcs.Handlers.IHandler import IHandler

class Bme280Handler(IHandler):

    def __init__(self, app=None, name="Bme280Handler"):
        self._gsv_init = False
        super(Bme280Handler, self).__init__(app=app, name=name)
        self._set_default_conf({})

    """ IConfigurable """

    def _setup_impl(self):
        return True

    def handle(self, observable, msg):
        fake = {
            "temperature": 42,
            "pressure": 1000,
            "humidity": 88,
            "timestamp": 4000002,
        }
        self.deliver(fake)
        return True
