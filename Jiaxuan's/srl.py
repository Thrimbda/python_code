import serial
import struct
import time
#comm = serial.Serial(1)
avi = []
for i in range(10):
    try:
        s = serial.Serial(i)
        avi.append(i)
        s.close()
    except Exception:
        pass
print avi
# while 1:
#     time.sleep(0.3)
#     m = comm.read(10)
#     print m