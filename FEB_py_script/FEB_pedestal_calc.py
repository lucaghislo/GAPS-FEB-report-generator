import re
import math
from matplotlib import lines
import os

# media pedestal
dir_ped = os.path.dirname(__file__)
file_ped = os.path.join(dir_ped, '../script_files/Pedestals.dat')

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