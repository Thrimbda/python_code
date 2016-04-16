import serial

ser = serial.Serial("/dev/ttyUSB0", 115200)
data = []
i = 0

try:
    while True:
        data.append(ser.readline())
        print(data[i])
except KeyboardInterrupt:
    with open('/home/michael/Documents/temp/data.txt', 'w') as fobj:
        for i in data:
            fobj.write(i)
