#!/usr/bin/python
#coding: utf-8

""" System """
pynmea2 = None

from sihd.Handlers.IHandler import IHandler

class NmeaHandler(IHandler):

    def __init__(self, app=None, name="NmeaHandler"):
        global pynmea2
        if pynmea2 is None:
            import pynmea2
        super(NmeaHandler, self).__init__(app=app, name=name)
        self.set_step_method(self.consume)
        self.set_service_threading()
        self._set_default_conf({})

    """ IConfigurable """

    def _setup_impl(self):
        return super()._setup_impl()

    """ IObservable """

    def on_error(self, observable, err):
        self.log_error(err)

    def handle(self, service, line):
        if line is None:
            return False
        if isinstance(line, bytes):
            line = line.decode('ascii', errors='replace')
        line = line.strip()
        if line == "":
            return True
        try:
            msg = pynmea2.parse(line)
        except:
            return False
        self.deliver(msg)
        return True
