import os
import numpy as np

with open('/home/michael/Documents/SORT/SORT2.txt', 'r') as rfileobj:
    with open(os.path.split(os.path.realpath(__file__))[0] + '/Fmt_SORT2.txt', 'w') as wfileobj:
        data = rfileobj.readlines()
        lines = data[1].split(' ')
        line = '{'
        for i in lines:
            line += i
            line += ','
        wfileobj.write(line)
