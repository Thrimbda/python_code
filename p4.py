import os
import numpy as np

with open(os.path.split(os.path.realpath(__file__))[0] + '/PointRoute.c', 'r') as rfileobj:
    with open(os.path.split(os.path.realpath(__file__))[0] + '/Fmt_RouteRed.txt', 'w') as wfileobj:
        db = rfileobj.readlines()[4239:8459:10]
        for item in db:
            line = item.replace('{', '').replace('}', '').replace(' ', '').split(',')
            speed_x = str(np.cos(eval(line[2]))*eval(line[4]))
            speed_y = str(np.sin(eval(line[2]))*eval(line[4]))
            line = '('+line[0]+','+line[1]+','+line[2]+','+speed_x+','+speed_y+','+line[4]+')\n'
            wfileobj.write(line)
