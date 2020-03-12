#!/usr/bin/python
#coding: utf-8

""" System """
from sihd.Handlers.IHandler import IHandler

class GsvHandler(IHandler):

    def __init__(self, app=None, name="GsvHandler"):
        self._gsv_init = False
        super(GsvHandler, self).__init__(app=app, name=name)
        self._set_default_conf({})

    """ IConfigurable """

    def _setup_impl(self):
        return True

    """ Gsv """

    def __init_gsv_data(self):
        self._GsvMsgReceived = None
        self._GsvNbMsg = 0
        self._SV_PRN_num = [0] * 20
        self._SV_azimuth = [0] * 20
        self._SV_elevation = [0] * 20
        self._SV_SNR = [0] * 20
        self._gsv_init = True

    def __get_int(self, num):
        if num:
            return int(num)
        return None

    def __handle_gsv_msg(self, msg):
        if self._gsv_init is False:
            self.__init_gsv_data()

        SV_PRN_num = self._SV_PRN_num
        SV_azimuth = self._SV_azimuth
        SV_elevation = self._SV_elevation
        SV_SNR = self._SV_SNR

        if self._GsvMsgReceived is None:
            NbMsg = self.__get_int(msg.num_messages)
            if NbMsg is None or NbMsg <= 0:
                self.log_error("Number of messages impossible: {}".format(NbMsg))
                return
            self._GsvNbMsg = NbMsg
            self._GsvMsgReceived = [False] * NbMsg

        MsgReceived = self._GsvMsgReceived

        Nb_SV_In_View = self.__get_int(msg.num_sv_in_view)
        Num_CurMsg = self.__get_int(msg.msg_num)

        offset = (Num_CurMsg - 1) * 4
        # Enregistrement des données dans les tableaux
        SV_PRN_num[offset + 0] = self.__get_int(msg.sv_prn_num_1)
        SV_azimuth[offset + 0] = self.__get_int(msg.azimuth_1)
        SV_elevation[offset + 0] = self.__get_int(msg.elevation_deg_1)
        SV_SNR[offset + 0] = self.__get_int(msg.snr_1)
        if offset + 2 <= Nb_SV_In_View:
            SV_PRN_num[offset + 1] = self.__get_int(msg.sv_prn_num_2)
            SV_azimuth[offset + 1] = self.__get_int(msg.azimuth_2)
            SV_elevation[offset + 1] = self.__get_int(msg.elevation_deg_2)
            SV_SNR[offset + 1] = self.__get_int(msg.snr_2)
        if offset + 3 <= Nb_SV_In_View:
            SV_PRN_num[offset + 2] = self.__get_int(msg.sv_prn_num_3)
            SV_azimuth[offset + 2] = self.__get_int(msg.azimuth_3)
            SV_elevation[offset + 2] = self.__get_int(msg.elevation_deg_3)
            SV_SNR[offset + 2] = self.__get_int(msg.snr_3)
        if offset + 4 <= Nb_SV_In_View:
            SV_PRN_num[offset + 3] = self.__get_int(msg.sv_prn_num_4)
            SV_azimuth[offset + 3] = self.__get_int(msg.azimuth_4)
            SV_elevation[offset + 3] = self.__get_int(msg.elevation_deg_4)
            SV_SNR[offset + 3] = self.__get_int(msg.snr_4)
            
        MsgReceived[Num_CurMsg - 1] = True
        if all(MsgReceived):
            self._gsv_init = False
            SV_azimuth_deg = SV_azimuth[0:Nb_SV_In_View]
            data = {
                "SV_PRN_num": SV_PRN_num[0:Nb_SV_In_View],
                "SV_azimuth_deg": SV_azimuth_deg,
                "SV_elevation": SV_elevation[0:Nb_SV_In_View],
                "SV_SNR": SV_SNR[0:Nb_SV_In_View],
                "SV_azimuth_rad": [x / 180.0*3.141593 for x in SV_azimuth_deg if x is not None],
                "Nb_SV_In_View": Nb_SV_In_View,
            }
            self.deliver(data)
        return True

    """ IObservable """

    def on_error(self, observable, err):
        self.log_error(err)

    def handle(self, observable, msg):
        ret = False
        if msg.sentence_type == 'GSV':
            ret = self.__handle_gsv_msg(msg)
        return ret
