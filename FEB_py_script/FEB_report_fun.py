import re
import math
from matplotlib import lines
import os

# temperatura
def report_temperature(file_temp):
    with open(file_temp) as f:
        lines_tm = f.readlines()

    sum = 0
    count = 0

    for i in lines_tm[45:]:
        str_tm = i.split("\t")
        sum = sum + int(str_tm[1][0:4])
        count = count + 1

    print("\n*** TEMPERATURE SENSOR ***")
    print("\nTemperature sensor [ADC]: " + str(int(sum/count)))

    ADC_code = int(sum/count)
    V_T = 0.9*1000 - (ADC_code - 1024)*1.72/(5.14)
    T = 30 + (5.506 - math.sqrt((-5.506)**2 + 4*.00176*(870.6 - V_T)))/(2*(-0.00176))

    print(" Temperature sensor [°C]: " + str(round(T,3)) +"\n")


# noise ENC
def report_ENC(file_ENC):  
    with open(file_ENC) as f:
        lines_enc = f.readlines()

    print("*** NOISE ENC ***\n")

    count = 0

    for i in lines_enc[7:]:
        str_enc = i.split("\t")
        
        time = str_enc[1][1:]
        channel = str_enc[0][1:]

        if(time == "6"):
            count = count + 1

            if((count -1) == 0 or (count -1) == 7 or (count -1) == 15 or (count -1) == 16 or (count -1) == 23 or (count -1) == 31 ):
                if((count-1)<10):
                    print(" Canale " + str(count-1) +": " + str_enc[4])
                else:
                    print("Canale " + str(count-1) +": " + str_enc[4])


# threshold dispersion
def report_thrdisp(file_thr):
    with open(file_thr) as f:
        lines_tr = f.readlines()

    str_tr = lines_tr[13]
    list_tr = str_tr.split("\t")
    print("\n*** THRESHOLD DISPERSION ***")
    print("\nBefore FT [DAC]: " + list_tr[3])
    print(" After FT [DAC]: " + list_tr[8] + "\n")


# media pedestal
def report_pedestal(file_ped):
    with open(file_ped) as f:
        lines_tm = f.readlines()

    sum = 0
    count = 0

    for i in lines_tm[1:]:
        str_tm = i.split("\t")

        if(int(str_tm[1])==6):
            sum = sum + float(str_tm[3])
            count = count + 1

    print("\n*** PEDESTAL DISPERSION ***")
    print("\nPedestal dispersion [ADC]: " + str(round(sum/count, 3)) + "\n")