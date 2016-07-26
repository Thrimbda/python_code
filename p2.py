import serial
import struct

ser = serial.Serial("/dev/ttyUSB1", 115200, timeout=0)

while True:
    x = input()
    # x = eval(x)
    # x = struct.pack("H", x)
    ser.write(x.encode())
