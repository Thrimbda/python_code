import socket
import time
import numpy as np
import struct
HOST='127.0.0.1'
PORT=50007
datatype = np.dtype([('x','<f'),('y','<f')])
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#s.connect((HOST,PORT))
x = 0
y = 0
import random
import serial
comm = serial.Serial(0,baudrate=115200)
a = np.array([(2,3)],dtype = datatype)
while 1:
    time.sleep(0.3)
    x = x + random.random() * 10
    y = y + random.random() * 10
    a = np.array([(x,y)],dtype = datatype)
    comm.write(struct.pack('2B',0xff,0xff) + a.tostring())