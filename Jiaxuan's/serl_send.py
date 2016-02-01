import serial
import time
import struct
comm = serial.Serial(1,baudrate=115200)
x = struct.pack('=2B3i',0xc8,0xc8,3,201,3)
print len(x)
while 1:
    time.sleep(0.5)
    comm.write(x)
    pass