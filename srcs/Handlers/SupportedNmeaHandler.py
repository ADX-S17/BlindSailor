#!/usr/bin/python
#coding: utf-8

""" System """
from sihd.srcs.Handlers.IHandler import IHandler
from sihd.srcs.Core.IProducer import IProducer

class SupportedNmeaHandler(IHandler):

    def __init__(self, app=None, name="SupportedNmeaHandler"):
        self._gsv_init = False
        super(SupportedNmeaHandler, self).__init__(app=app, name=name)
        self._set_default_conf({})
        self.__last_msg = None
        self.__parsing_fun = {
            "GLL": self.__handle_gll_msg,
            "RMC": self.__handle_rmc_msg,
            "VTG": self.__handle_vtg_msg,
        }
        self._datas = {
            "cap": {},
            "speed_over_ground": {},
        }
        self._vtg = 0
        self._rmc = 0
        self._gll = 0

    """ IConfigurable """

    def _setup_impl(self):
        return True

    """ Supported Nmea """

    def __handle_vtg_msg(self, msg):
        datas = self._datas
        datas["timestamp"] = None
        datas["speed_over_ground"].update({
            "knots": msg.spd_over_grnd_kts,
            "knots_sym": msg.spd_over_grnd_kts_sym,
            "kmph": msg.spd_over_grnd_kmph,
            "kmph_sym": msg.spd_over_grnd_kmph_sym,
        })
        datas["cap"].update({
            "real": msg.true_track,
            "real_sym": msg.true_track_sym,
            "mag": msg.mag_track,
            "mag_sym": msg.mag_track_sym,
        })
        self.deliver("VTG", datas)
        self._vtg += 1

    def __handle_rmc_msg(self, msg):
        valid = msg.status
        if valid != "A":
            self.log_error("Not valid RMC: {}".format(valid))
            return
        datas = self._datas
        datas["timestamp"] = msg.timestamp
        datas["latitude"] = msg.lat
        datas["lat_dir"] = msg.lat_dir
        datas["longitude"] = msg.lon
        datas["lon_dir"] = msg.lon_dir
        datas["speed_over_ground"].update({
            "knots": msg.spd_over_grnd,
            "knots_sym": "K", #TODO
        })
        datas["cap"].update({"true": msg.true_course})
        self.deliver(datas)
        self._rmc += 1

    def __handle_gll_msg(self, msg):
        valid = msg.status
        if valid != "A":
            self.log_error("Not valid GLL: {}".format(valid))
            return
        datas = self._datas
        datas["timestamp"] = msg.timestamp
        datas["latitude"] = msg.lat
        datas["lat_dir"] = msg.lat_dir
        datas["longitude"] = msg.lon
        datas["lon_dir"] = msg.lon_dir
        self.deliver("GLL", datas)
        self._gll += 1

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
