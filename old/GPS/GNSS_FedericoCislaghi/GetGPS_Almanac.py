"""GetGPS_Almanac.py: Récupère les almanac GPS depuis le récepteur."""

__author__   = "Federico CISLAGHI"
__email__    = "cislaghi47@gmail.com"

import serial
import pynmea2
import math
import pprint

## Script configuration
port = "COM4"

## Définition d'une fonction pour convertir les valeurs ASCII en valeurs numériques,
## puis prendre en compte le bit de signe (si nécessaire)
## et enfin appliquer le facteur d'échelle (multiplication par LSB)
def ConvertParam(ascii_str, scale_factor=0, nb_bits_for_two_complement=0):
    intval = int(ascii_str, 16)

    if nb_bits_for_two_complement > 0:
        intval = -(intval & (1 << nb_bits_for_two_complement)) | (intval & ((1 << nb_bits_for_two_complement) - 1))
        
    return intval * 2**(scale_factor)
    
pp = pprint.PrettyPrinter(indent=4)

## Data initialisation
ALM_Data_Complete = False
SV_Data = {}
NbMsg = 0

serialPort = serial.Serial(port, baudrate = 19200, timeout = 0.5)
serialPort.read_until() # On saute la première ligne incomplète

serialPort.write("$PGRMO,GPALM,1\r\n".encode('ascii'))

while not(ALM_Data_Complete):
    str = serialPort.readline().decode('ascii', errors='replace').strip()

    try:
        msg = pynmea2.parse(str)
    except:
        continue

    if msg.sentence_type == 'ALM':
        print(str)
        Num_CurMsg = int(msg.msg_num)

        ## NOTA: Source pour les facteurs de conversion des données:
        # https://www.gps.gov/technical/icwg/IS-GPS-200H.pdf (p.125/226)
        # Vérification du bon décodage à faire à partir d'ici:
        # https://celestrak.com/GPS/almanac/Yuma/2019/
        CurSV_Data = {'sat_prn_num':    int(msg.sat_prn_num),
                   'week_num':          int(msg.gps_week_num),
                   'sv_health':         int(msg.sv_health),
                   'eccentricity':      ConvertParam(msg.eccentricity, -21),                # [-]
                   'alamanac_ref_time': ConvertParam(msg.alamanac_ref_time, 12),            # [sec]
                   'inc_angle':         (0.3 + ConvertParam(msg.inc_angle, -19, 16)) * math.pi,     # [rad]
                   #'rate_right_asc':    ConvertParam(msg.rate_right_asc, -38, 16) * math.pi,# [rad/sec]
                   'root_semi_major_axis':ConvertParam(msg.root_semi_major_axis, -11),      # [sqrt(m)]
                   'arg_perigee':       ConvertParam(msg.arg_perigee, -23, 24) * math.pi,   # [rad]
                   'lat_asc_node':      ConvertParam(msg.lat_asc_node, -23, 24) * math.pi,  # [rad]
                   'mean_anom':         ConvertParam(msg.mean_anom, -23, 24) * math.pi,     # [rad]
                   'f0_clock_param':    ConvertParam(msg.f0_clock_param, -20, 11),          # [sec]
                   'f1_clock_param':    ConvertParam(msg.f1_clock_param, -38, 11)           # [sec/sec]
                      } 
        pp.pprint(CurSV_Data)

        SV_Data[CurSV_Data['sat_prn_num']] = CurSV_Data

        # On attend le message 1/N pour configurer le nb de messages à recevoir
        if Num_CurMsg == 1:
            NbMsg = int(msg.total_num_msgs)
            MsgReceived = [False] * NbMsg
            
        if NbMsg > 0:
            MsgReceived[Num_CurMsg - 1] = True
            
            if all(MsgReceived):
                ALM_Data_Complete = True

print("close serial port.")
serialPort.close()
print('Done!')
