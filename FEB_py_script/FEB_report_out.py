from __future__ import print_function
from pickle import FALSE, TRUE
from mailmerge import MailMerge
from datetime import date
from docx2pdf import convert

from FEB_report_fun import (
    report_ENC,
    report_pedestal,
    report_temperature,
    report_thrdisp,
    text_to_pdf,
)
from FEB_report_fun import ftxt_a, ftxt_w, ftxt_r
import re
import math
from matplotlib import lines
import os
from pathlib import Path
from datetime import date


# acquisizione directory
def print_report(num_report):

    flag = False

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
        dir_temp, "../script_files/" + intermediate_path + "data/HK_Temperature.dat"
    )

    # noise ENC
    dir_ENC = os.path.dirname(__file__)
    file_ENC = os.path.join(
        dir_ENC,
        "../script_files/"
        + intermediate_path
        + "analysis_matlab/ENC/normal/ENC_normal.dat",
    )

    # threshold dispersion
    dir_thr = os.path.dirname(__file__)
    file_thr = os.path.join(
        dir_thr,
        "../script_files/"
        + intermediate_path
        + "analysis_matlab/ThresholdScan/Threshold_dispersion.dat",
    )

    # media pedestal
    dir_ped = os.path.dirname(__file__)
    file_ped = os.path.join(
        dir_ped, "../script_files/" + intermediate_path + "data/Pedestals.dat"
    )

    if Path(file_temp).is_file():
        ftxt_a.write("***** MODULE " + show + " ******\n")
        report_temperature(file_temp)
        flag = True

    if Path(file_ENC).is_file():
        report_ENC(file_ENC)

    if Path(file_thr).is_file():
        report_thrdisp(file_thr)

    if Path(file_ped).is_file():
        report_pedestal(file_ped)
        ftxt_a.write(" \n")
        ftxt_a.write("----------------------------------------------\n")
        ftxt_a.write(" \n")

    return flag


# main call
start = int(input("Range START: "))
stop = int(input(" Range STOP: "))

for i in range(start, stop + 1):
    flag = print_report(i)

    document = MailMerge("test_report_FEB.docx")

    if flag:

        if i < 10:
            ID_number = "00" + str(i)
        elif i < 100:
            ID_number = "00" + str(i)
        else:
            ID_number = str(i)

        today = date.today()
        today = today.strftime("%d.%m.%Y")

        document.merge(
            board_ID_title=ID_number,
            nation_letter="I",
            board_ID="F" + str(ID_number) + "I",
            doc_version="0.1",
            date=today,
            author="L. Ghislotti",
            asic_ID=ID_number,
            nation_word="Italian",
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
