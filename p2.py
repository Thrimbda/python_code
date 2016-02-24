import os
import numpy as np

with open(os.path.split(os.path.realpath(__file__))[0]+"/RPi_and_BigMonster/Computer/Route_blue.txt", 'r') as frobj:
    with open(os.path.split(os.path.realpath(__file__))[0]+'/Fmt_route_blue.txt', 'w') as fwobj:
        line = frobj.readline()
        while True:
            line = line.replace(' { {', '').replace('}', '').split(',')
            if line == [' ']:
                break
            line = '("posture",('+line[0]+','+line[1]+','+line[2]+','+str(np.cos(float(line[2]))*line[4])+','+str(np.sin(float(line[2]))*line[4])+','+line[4]+'))\n'
            fwobj.write(line)
            line = frobj.readline()
