"""PlotGPS.py: Récupère et affiche les informations sur les sat GPS en visibilité."""

__author__   = "Federico CISLAGHI"
__email__    = "cislaghi47@gmail.com"

import serial
import pynmea2
import os
#import matplotlib.pyplot as plt

## Script configuration
port = "/dev/ttyAMA0"

## Data initialisation
GSV_Data_Complete = False
NbMsg = 0
SV_PRN_num = [0] * 20
SV_azimuth = [0] * 20
SV_elevation = [0] * 20
SV_SNR = [0] * 20

serialPort = serial.Serial(port, baudrate = 9600, timeout = 1.5)
log = os.open("trame_gps", os.O_WRONLY | os.O_CREAT)
while not(GSV_Data_Complete):
    line = serialPort.readline()
    os.write(log, line)
    str = line.decode('ascii', errors='replace').strip()

    try:
        msg = pynmea2.parse(str)
    except:
        continue
    
    print(type(msg))
    print(msg.__dict__)
    if msg.sentence_type == 'GSV':
        print(str)
        Nb_SV_In_View = int(msg.num_sv_in_view)
        Num_CurMsg = int(msg.msg_num)

        offset = (Num_CurMsg - 1) * 4
        # Enregistrement des données dans les tableaux
        SV_PRN_num[offset + 0] = int(msg.sv_prn_num_1)
        SV_azimuth[offset + 0] = int(msg.azimuth_1)
        SV_elevation[offset + 0] = int(msg.elevation_deg_1)
        SV_SNR[offset + 0] = int(msg.snr_1)
        if offset + 2 <= Nb_SV_In_View:
            SV_PRN_num[offset + 1] = int(msg.sv_prn_num_2)
            SV_azimuth[offset + 1] = int(msg.azimuth_2)
            SV_elevation[offset + 1] = int(msg.elevation_deg_2)
            SV_SNR[offset + 1] = int(msg.snr_2)
        if offset + 3 <= Nb_SV_In_View:
            SV_PRN_num[offset + 2] = int(msg.sv_prn_num_3)
            SV_azimuth[offset + 2] = int(msg.azimuth_3)
            SV_elevation[offset + 2] = int(msg.elevation_deg_3)
            SV_SNR[offset + 2] = int(msg.snr_3)
        if offset + 4 <= Nb_SV_In_View:
            SV_PRN_num[offset + 3] = int(msg.sv_prn_num_4)
            SV_azimuth[offset + 3] = int(msg.azimuth_4)
            SV_elevation[offset + 3] = int(msg.elevation_deg_4)
            SV_SNR[offset + 3] = int(msg.snr_4)

        # On attend le message 1/N pour configurer le nb de messages à recevoir
        if Num_CurMsg == 1:
            NbMsg = int(msg.num_messages)
            MsgReceived = [False] * NbMsg
            
        if NbMsg > 0:
            MsgReceived[Num_CurMsg - 1] = True
            
            if all(MsgReceived):
                GSV_Data_Complete = True
        
os.close(log)
SV_PRN_num = SV_PRN_num[0:Nb_SV_In_View]
SV_azimuth_deg = SV_azimuth[0:Nb_SV_In_View]
SV_elevation = SV_elevation[0:Nb_SV_In_View]
SV_SNR = SV_SNR[0:Nb_SV_In_View]

SV_azimuth_rad = [x/180.0*3.141593 for x in SV_azimuth_deg]

## Tracé de la figure
"""
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_rlim(0, 90)
c = ax.scatter(SV_azimuth_rad, SV_elevation, c=SV_SNR, s=350,
               cmap='rainbow', alpha=0.75, vmin=0)

for i, txt in enumerate(SV_PRN_num):
    ax.annotate(txt, (SV_azimuth_rad[i], SV_elevation[i]))

cbar = fig.colorbar(c)
ax.set_title("%d GPS satellites in view" % Nb_SV_In_View, fontsize=18)
plt.show()
"""

print('Done!')
