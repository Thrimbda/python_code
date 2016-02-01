import serial

class Communicata_ARM:
	def __init__(self):
		self.ser = serial.Serial("/dev/ttyUSB0", baudrate = 115200)
		self.fobj = open('/home/michael/Documents/python_code/RPi_and_BigMonster/Computer/PointRoute.txt', 'w')
		print('everything is fine')

	def writefile(self):
		x = self.ser.readline().decode()
		self.fobj.write(x)

cmt1 = Communicata_ARM()
while True:
	cmt1.writefile()