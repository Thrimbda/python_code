import os
import numpy as np

with open('/home/michael/Documents/python_code/RPi_and_BigMonster/Computer/encoder4.txt', 'r') as rfileobj:
    with open(os.path.split(os.path.realpath(__file__))[0] + '/Fmt_encoder4.txt', 'w') as wfileobj:
        data = rfileobj.readlines()[274:]
        for line in data:
            line = line.replace('(', '').replace(')', '').replace(',', '') + '\n'
            wfileobj.write(line)
