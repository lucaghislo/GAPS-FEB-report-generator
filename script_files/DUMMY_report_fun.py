import re
import math
from unittest import case
from matplotlib import lines
import os
import textwrap
from fpdf import FPDF
import csv
import re
from datetime import date

# configuration import
def read_config_file():
    counter = 0
    lines = []

    nation_letter = ""
    doc_version = ""
    data = ""
    author = ""
    nation_word = ""

    with open("../configuration/config.conf") as f:
        lines = f.readlines()

        nation_letter = re.search(
            "nation_letter = '(.*?)'         # nationality letter identifier",
            lines[0],
        ).group(1)

        doc_version = re.search(
            "doc_version = '(.*?)'         # document version",
            lines[1],
        ).group(1)

        data = re.search(
            "date = '(.*?)'         # if empty date is set to current date",
            lines[2],
        ).group(1)

        if data == "":
            today = date.today()
            today = today.strftime("%d.%m.%Y")
            data = today

        author = re.search(
            "author = '(.*?)'     # report author",
            lines[3],
        ).group(1)

        nation_word = re.search(
            "nation_word = '(.*?)'     # nationality identifier word",
            lines[4],
        ).group(1)

        counter = counter + 1

    return [nation_letter, doc_version, data, author, nation_word]


# bias readings
def get_bias_data(module_number):
    module_data = []
    flag = False

    with open("../CSV_tables/DUMMY_testing - Multimeter.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0

        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if row[0] == str(module_number):
                    for i in range(1, 5):
                        row[i] = row[i].replace(",", ".")

                    module_data.append(row[0])
                    module_data.append(format(float(row[1]), ".3f"))
                    module_data.append(format(float(row[2]), ".1f"))
                    module_data.append(format(float(row[3]), ".1f"))
                    module_data.append(row[4])

                    flag = True

                line_count += 1

    return [module_data, flag]
