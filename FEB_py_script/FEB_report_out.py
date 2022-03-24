from FEB_report_fun import report_ENC, report_pedestal, report_temperature, report_thrdisp
import re
import math
from matplotlib import lines
import os


# acquisizione directory
def print_report(num_report):

    if num_report < 10:
        intermediate_path = "MODULE_00" + str(num_report)
    elif num_report < 100:
        intermediate_path = "MODULE_0" + str(num_report)
    else:
        intermediate_path = "MODULE_" + str(num_report)

    intermediate_path = intermediate_path + "/1/"

    # temperature file
    dir_temp = os.path.dirname(__file__)
    file_temp = os.path.join(dir_temp, '../script_files/' + intermediate_path + 'data/HK_Temperature.dat')

    # noise ENC
    dir_ENC = os.path.dirname(__file__)
    file_ENC = os.path.join(dir_ENC, '../script_files/' + intermediate_path + 'analysis_matlab/ENC/normal/ENC_normal.dat')

    # threshold dispersion
    dir_thr = os.path.dirname(__file__)
    file_thr = os.path.join(dir_thr, '../script_files/'+ intermediate_path + 'analysis_matlab/ThresholdScan/Threshold_dispersion.dat')

    # media pedestal
    dir_ped = os.path.dirname(__file__)
    file_ped = os.path.join(dir_ped, '../script_files/' + intermediate_path + 'data/Pedestals.dat')

    report_temperature(file_temp)
    report_ENC(file_ENC)
    report_thrdisp(file_thr)
    report_pedestal(file_ped)


# main call
start = int(input("Range START: "))
stop = int(input(" Range STOP: "))

for i in range(start, stop+1):
    print_report(i)
    print("\n")

