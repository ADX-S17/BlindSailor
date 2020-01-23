#!/usr/bin/python
#coding: utf-8

""" System """
from sihd.srcs.Handlers.IHandler import IHandler
from sihd.srcs.Core.IProducer import IProducer

class SupportedNmeaHandler(IHandler, IProducer):

    def __init__(self, app=None, name="SupportedNmeaHandler"):
        self._gsv_init = False
        super(SupportedNmeaHandler, self).__init__(app=app, name=name)
        self._set_default_conf({
        })
        self.__last_msg = None
        self.__parsing_fun = {
            "GLL": self.__handle_gll_msg,
            "RMC": self.__handle_rmc_msg,
        }

    """ IConfigurable """

    def _setup_impl(self):
        return True

    """ Supported Nmea """

    def __handle_rmc_msg(self, msg):
        latitude = msg.lat
        lat_dir = msg.lat_dir
        longitude = msg.lon
        lon_dir = msg.lon_dir
        acquisition = msg.timestamp
        valid = msg.status
        """
        print("RMC -> Lat: {} - Long: {}".format(latitude, longitude))
        print("RMC -> Latdir: {} - Longdir: {}".format(lat_dir, lon_dir))
        print(acquisition, valid)
        """
        if valid == "A":
            self.notify_observers("RMC", msg)
        else:
            self.log_error("Not valid RMC: {}".format(valid))

    def __handle_gll_msg(self, msg):
        latitude = msg.lat
        lat_dir = msg.lat_dir
        longitude = msg.lon
        lon_dir = msg.lon_dir
        acquisition = msg.timestamp
        valid = msg.status
        """
        print("GLL -> Lat: {} - Long: {}".format(latitude, longitude))
        print("GLL -> Latdir: {} - Longdir: {}".format(lat_dir, lon_dir))
        print(acquisition, valid)
        """
        if valid == "A":
            self.notify_observers("GLL", msg)
        else:
            self.log_error("Not valid GLL: {}".format(valid))

    """ IObservable """

    def on_error(self, observable, err):
        self.log_error(err)

    def handle(self, observable, msg):
        ret = False
        fun = self.__parsing_fun.get(msg.sentence_type, None)
        if fun is not None:
            ret = fun(msg)
        if ret:
            self.__last_msg = msg
        return ret
