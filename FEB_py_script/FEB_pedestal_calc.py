import re
import math
from matplotlib import lines
import os

# media pedestal
dir_ped = os.path.dirname(__file__)
file_ped = os.path.join(dir_ped, '../script_files/Pedestals.dat')

with open(file_ped) as f:
    lines_tm = f.readlines()

for i in lines_tm[45:]:
    str_tm = i.split("\t")
    print(str_tm)