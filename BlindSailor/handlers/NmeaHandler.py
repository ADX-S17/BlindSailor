#!/usr/bin/python
#coding: utf-8

pynmea2 = None

from sihd.handlers.AHandler import AHandler

class NmeaHandler(AHandler):

    def __init__(self, name="NmeaHandler", app=None):
        global pynmea2
        if pynmea2 is None:
            import pynmea2
        super().__init__(app=app, name=name)
        self.add_channel_input("input")
        self.add_channel("message")

    def handle(self, channel):
        if channel == self.input:
            data = channel.read()
            if data is not None:
                self.decode_nmea(data)

    def decode_nmea(self, data):
        if isinstance(data, bytes):
            data = data.decode('ascii', errors='replace').strip()
        elif not isinstance(data, str):
            self.log_error("Did not receive bytes or string to decode")
        try:
            msg = pynmea2.parse(data)
        except Exception as e:
            self.log_error(e)
            return False
        self.message.write(msg)
        return True
