import numpy as np
import mec_acc

filename = '/home/michael/Documents/temp/data.txt'

data = []
with open(filename, 'r') as fileobj:
    data = fileobj.readlines()

for x in np.arange(len(data)):
    data[x] = eval(data[x])

x_speed = data[0:131]
y_spped = data[131:263]
r_speed = data[263:]

print(x_speed, y_spped, r_speed)
for i in np.arange(131):
    print(mec_acc.set_speed(x_speed[i], y_spped[i], r_speed[i]), (i+1)*0.1)
