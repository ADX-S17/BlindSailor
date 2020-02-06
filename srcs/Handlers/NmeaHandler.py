#!/usr/bin/python
#coding: utf-8

""" System """
pynmea2 = None

from sihd.srcs.Handlers.IHandler import IHandler
from sihd.srcs.Core.IThreadedService import IThreadedService
from sihd.srcs.Core.IConsumer import IConsumer

class NmeaHandler(IHandler, IThreadedService, IConsumer):

    def __init__(self, app=None, name="NmeaHandler"):
        global pynmea2
        if pynmea2 is None:
            import pynmea2
        super(NmeaHandler, self).__init__(app=app, name=name)
        self.set_run_method(self.consume)
        self._set_default_conf({
        })

    """ IConfigurable """

    def _setup_impl(self):
        return super()._setup_impl()

    """ IObservable """

    def on_error(self, observable, err):
        self.log_error(err)

    #def consumed(self, service, line):
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
        self.notify_observers(msg)
        return True

    def _start_impl(self):
        return IThreadedService._start_impl(self)

    def _stop_impl(self):
        return IThreadedService._stop_impl(self)
