#!/usr/bin/python
#coding: utf-8

from sihd.handlers.AHandler import AHandler

class SupportedNmeaHandler(AHandler):

    def __init__(self, name="SupportedNmeaHandler", app=None):
        self._gsv_init = False
        super().__init__(app=app, name=name)
        self.__last_msg = None
        self.__parsing_fun = {
            "GLL": self.__handle_gll_msg,
            "RMC": self.__handle_rmc_msg,
            "VTG": self.__handle_vtg_msg,
        }
        self._pos_dic = {}
        self._cap_dic = {}
        self._speed_over_ground_dic = {}
        self._vtg = 0
        self._rmc = 0
        self._gll = 0
        self.add_channel("pos")
        self.add_channel("speed_over_ground")
        self.add_channel("cap")
        self.add_channel_input("message")

    #
    # Supported Nmea
    #

    def __handle_vtg_msg(self, msg):
        pos = self._pos_dic
        #pos["timestamp"] = None
        self._speed_over_ground_dic.update({
            "knots": msg.spd_over_grnd_kts,
            "knots_sym": msg.spd_over_grnd_kts_sym,
            "kmph": msg.spd_over_grnd_kmph,
            "kmph_sym": msg.spd_over_grnd_kmph_sym,
        })
        self.speed_over_ground.write(self._speed_over_ground_dic)
        self._cap_dic.update({
            "real": msg.true_track,
            "real_sym": msg.true_track_sym,
            "mag": msg.mag_track,
            "mag_sym": msg.mag_track_sym,
        })
        self.cap.write(self._cap_dic)
        self._vtg += 1

    def __handle_rmc_msg(self, msg):
        valid = msg.status
        if valid != "A":
            self.log_error("Not valid RMC: {}".format(valid))
            return
        pos = self._pos_dic
        pos["timestamp"] = msg.timestamp
        pos["latitude"] = msg.lat
        pos["lat_dir"] = msg.lat_dir
        pos["longitude"] = msg.lon
        pos["lon_dir"] = msg.lon_dir
        self.pos.write(pos)
        self._speed_over_ground_dic.update({
            "knots": msg.spd_over_grnd,
            "knots_sym": "N", #TODO
        })
        self.speed_over_ground.write(self._speed_over_ground_dic)
        self._cap_dic["true"] = msg.true_course
        self.cap.write(self._cap_dic)
        self._rmc += 1

    def __handle_gll_msg(self, msg):
        valid = msg.status
        if valid != "A":
            self.log_error("Not valid GLL: {}".format(valid))
            return
        pos = self._pos_dic
        pos["timestamp"] = msg.timestamp
        pos["latitude"] = msg.lat
        pos["lat_dir"] = msg.lat_dir
        pos["longitude"] = msg.lon
        pos["lon_dir"] = msg.lon_dir
        self.pos.write(pos)
        self._gll += 1

    def parse_message(self, msg):
        fun = self.__parsing_fun.get(msg.sentence_type, None)
        if fun is not None:
            fun(msg)
            self.__last_msg = msg
        return fun is not None

    def handle(self, channel):
        if channel == self.message:
            msg = channel.read()
            if msg is not None:
                self.parse_message(msg)
