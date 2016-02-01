import socket
import math

class Recive_PMT:
	def __init__(self):
		self.UDP_IP = '192.168.10.90'
		self.UDP_PORT = 5005		#Pi to PC

		socket.setdefaulttimeout(3)
		self.s = socket.socket(socket.AF_INET,		#internet
                  socket.SOCK_DGRAM)	#UDP
		self.s.bind((self.UDP_IP, self.UDP_PORT))				#binding socket
		# self.X, self.Y ,self.A, self.Speed_X, self.speed_Y, self.Speed, self.AP, self.AI, self.AD, self.DP, self.DI, self.DD,self.End_X, self.End_Y, self.SpdMx, self.AimA = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

	def Recive_Data(self):
	    self.data, self.addr = self.s.recvfrom(128)
	    # if data.decode() == 'TransfromingFinished':
	        # break
	    self.info = self.data.decode()
	    return self.info

if __name__ == '__main__':
	fobj = open('/home/macsnow/Documents/python_code/database.txt','w')
	obj = Recive_PMT()
	try:
		while True:
			line = obj.Recive_Data()
			print(line)
			fobj.write(line)
	except timeout:
		exit()
	finally:
		fobj.close()