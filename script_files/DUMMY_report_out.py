from __future__ import print_function
from mailmerge import MailMerge
from docx2pdf import convert

from DUMMY_report_fun import (
    get_bias_data,
    read_config_file,
)

import re
import math
from matplotlib import lines
import os
from pathlib import Path


# main call
start = int(input("Range START: "))
stop = int(input(" Range STOP: "))

for i in range(start, stop + 1):
    bias_data = get_bias_data(i)
    config_data = read_config_file()
    document = MailMerge("../report_template/test_report_DUMMY.docx")

    if i < 10:
        ID_number = "0" + str(i)
    elif i < 100:
        ID_number = str(i)

    print("\nDUMMY D" + str(i) + "-" + str(ID_number))

    document.merge(
        dummy_D1=str(i),
        dummy_ID1=ID_number,
        dummy_D2=str(i),
        dummy_ID2=ID_number,
        doc_version=config_data[1],
        date=config_data[2],
        author=config_data[3],
        temp=bias_data[3],
        AVDD=bias_data[1],
        IVDD=bias_data[2],
        notes=bias_data[4],
    )

    document.write("../report_word/D" + str(i) + "-" + str(ID_number) + ".docx")
    convert(
        "../report_word/D" + str(i) + "-" + str(ID_number) + ".docx",
        "../report_PDF/D" + str(i) + "-" + str(ID_number) + ".pdf",
    )
