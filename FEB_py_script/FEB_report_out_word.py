from FEB_report_fun import report_ENC, report_pedestal, report_temperature, report_thrdisp, text_to_pdf
from FEB_report_fun import ftxt_a, ftxt_w, ftxt_r
import re
import math
from matplotlib import lines
import os
from pathlib import Path
from datetime import date

from io import StringIO 
from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage


# acquisizione directory
def print_report(num_report):
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

    if Path(file_temp).is_file():
        ftxt_a.write("***** MODULE " + show + " ******\n")
        report_temperature(file_temp)

    if Path(file_ENC).is_file():
        report_ENC(file_ENC)

    if Path(file_thr).is_file():
        report_thrdisp(file_thr)

    if Path(file_ped).is_file():
        report_pedestal(file_ped)
        ftxt_a.write(" \n")
        ftxt_a.write("----------------------------------------------\n")
        ftxt_a.write(" \n")


def get_context():
    return {
        'invoice_no': 12345,
        'date': '30 Mar',
        'due_date': '30 Apr',
        'name': 'Jane Doe',
        'address': '123 Quiet Lane',
        'subtotal': 335,
        'tax_amt': 10,
        'total': 345,
        'amt_paid': 100,
        'amt_due': 245,
        'row_contents': [
            {
                'description': 'Eggs',
                'quantity': 30,
                'rate': 5,
                'amount': 150
            }, {
                'description': 'All Purpose Flour',
                'quantity': 10,
                'rate': 15,
                'amount': 150
            }, {
                'description': 'Eggs',
                'quantity': 5,
                'rate': 7,
                'amount': 35
            }
        ]
    }


def from_template(template, signature):
    target_file = StringIO()

    template = DocxTemplate(template)
    context = get_context()  # gets the context used to render the document

    img_size = Cm(7)  # sets the size of the image
    sign = InlineImage(template, signature, img_size)
    context['signature'] = sign  # adds the InlineImage object to the context

    target_file = StringIO()
    template.render(context)
    template.save(target_file)

    return target_file


# main call
start = int(input("Range START: "))
stop = int(input(" Range STOP: "))

for i in range(start, stop+1):
    print_report(i)

ftxt_w.close()
ftxt_a.close()

text = ftxt_r.read()
ftxt_r.close()
text_to_pdf(text, '../report_output.pdf')