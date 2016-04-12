import numpy as np
import mec_acc

filename = '/home/michael/Documents/python_code/RPi_and_BigMonster/Computer/encoder4.12_19:11(speed1.2).txt'

data = []
xData = []
yData = []
rData = []
colSpeed = []
verSpeed = []
rotSpeed = []
with open(filename, 'r') as fileobj:
    data = fileobj.readlines()

for x in np.arange(len(data)):
    data[x] = eval(data[x])
    print(data[x])
    xData.append(data[x][0])
    yData.append(data[x][1])
    rData.append(data[x][2])

mec_acc.speedCalculator(xData, yData, rData, colSpeed, verSpeed, rotSpeed)
print(len(xData), len(yData), len(rData), len(colSpeed), len(verSpeed), len(rotSpeed))
for i in np.arange(len(colSpeed)):
    print(mec_acc.set_speed(colSpeed[i], verSpeed[i], rotSpeed[i]), (i+1)*0.1)
