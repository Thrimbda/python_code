import serial

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=0)

while True:
    x = ser.read()
    print(x)
