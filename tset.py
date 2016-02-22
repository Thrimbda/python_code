import serial

ser = serial.Serial('/dev/ttyUSB0', baudrate=115200)

while True:
    print(ser.readline())
