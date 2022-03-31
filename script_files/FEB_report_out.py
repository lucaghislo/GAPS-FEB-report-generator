from __future__ import print_function
from audioop import bias
from pickle import FALSE, TRUE
from mailmerge import MailMerge
from docx2pdf import convert

from FEB_report_fun import (
    report_ENC,
    report_pedestal,
    report_temperature,
    report_thrdisp,
    text_to_pdf,
    get_bias_data,
    read_config_file,
    defect_notes,
)

from FEB_report_fun import ftxt_a, ftxt_w, ftxt_r
import re
import math
from matplotlib import lines
import os
from pathlib import Path


# acquisizione directory
def print_report(num_report):
    flag = False
    temp_data = []
    ENC_data = []
    thrdisp_data = []
    pedestal_data = ""

    if num_report < 10:
        intermediate_path = "MODULE_00" + str(num_report)
        show = "F00" + str(i) + "I"
    elif num_report < 100:
        intermediate_path = "MODULE_0" + str(num_report)
        show = "F0" + str(i) + "I"
    else:
        intermediate_path = "MODULE_" + str(num_report)
        show = "F" + str(i) + "I"

    intermediate_path = intermediate_path + "/1/"

    # temperature file
    dir_temp = os.path.dirname(__file__)
    file_temp = os.path.join(
        dir_temp, "../modules/" + intermediate_path + "data/HK_Temperature.dat"
    )

    # noise ENC
    dir_ENC = os.path.dirname(__file__)
    file_ENC = os.path.join(
        dir_ENC,
        "../modules/" + intermediate_path + "analysis_matlab/ENC/normal/ENC_normal.dat",
    )

    # threshold dispersion
    dir_thr = os.path.dirname(__file__)
    file_thr = os.path.join(
        dir_thr,
        "../modules/"
        + intermediate_path
        + "analysis_matlab/ThresholdScan/Threshold_dispersion.dat",
    )

    # media pedestal
    dir_ped = os.path.dirname(__file__)
    file_ped = os.path.join(
        dir_ped, "../modules/" + intermediate_path + "data/Pedestals.dat"
    )

    if Path(file_temp).is_file():
        ftxt_a.write("***** MODULE " + show + " ******\n")
        temp_data = report_temperature(file_temp)
        flag = True

    if Path(file_ENC).is_file():
        ENC_data = report_ENC(file_ENC)

    if Path(file_thr).is_file():
        thrdisp_data = report_thrdisp(file_thr)

    if Path(file_ped).is_file():
        pedestal_data = report_pedestal(file_ped)
        ftxt_a.write(" \n")
        ftxt_a.write("----------------------------------------------\n")
        ftxt_a.write(" \n")

    return [flag, temp_data, ENC_data, thrdisp_data, pedestal_data]


# main call
start = int(input("Range START: "))
stop = int(input(" Range STOP: "))

for i in range(start, stop + 1):
    report_data = print_report(i)
    bias_data = get_bias_data(i)
    config_data = read_config_file()
    report_notes = defect_notes(i)
    document = MailMerge("../report_template/test_report_FEB.docx")

    if report_data[0]:
        if i < 10:
            ID_number = "00" + str(i)
        elif i < 100:
            ID_number = "0" + str(i)
        else:
            ID_number = str(i)

        print("\nMODULE F" + str(ID_number) + config_data[0])

        document.merge(
            board_ID_title=ID_number,
            nation_letter=config_data[0],
            board_ID="F" + str(ID_number) + str(config_data[0]),
            doc_version=config_data[1],
            date=config_data[2],
            author=config_data[3],
            asic_ID=ID_number,
            nation_word=config_data[4],
            AVDD=bias_data[1],
            IVDD=bias_data[2],
            DVDD=bias_data[3],
            IDVDD=bias_data[4],
            treVtre=bias_data[5],
            ItreVtre=bias_data[6],
            Ibias=bias_data[7],
            VCMSH=bias_data[8],
            VCM=bias_data[9],
            RVCM=bias_data[10],
            temp_ADC=report_data[1][0],
            temp_T=report_data[1][1],
            no_resp_ch="0",
            ENC_0=report_data[2][0],
            ENC_7=report_data[2][1],
            ENC_15=report_data[2][2],
            ENC_16=report_data[2][3],
            ENC_23=report_data[2][4],
            ENC_31=report_data[2][5],
            thr_disp_bef=report_data[3][0],
            thr_disp_aft=report_data[3][1],
            ped_disp=report_data[4],
            notes=report_notes,
        )

        document.write("../report_word/F" + str(ID_number) + "I" + ".docx")
        convert(
            "../report_word/F" + str(ID_number) + "I" + ".docx",
            "../report_PDF/F" + str(ID_number) + "I" + ".pdf",
        )

ftxt_w.close()
ftxt_a.close()

text = ftxt_r.read()
ftxt_r.close()
text_to_pdf(text, "../report_output.pdf")
