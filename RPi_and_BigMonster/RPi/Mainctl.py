import serial
import time
import struct
import socket

class TransUDP:			#send data to PC
	def __init__(self):
		self.TUDP_IP = '192.168.10.90'
		self.TUDP_PORT = 5005

		self.T_msg = socket.socket(socket.AF_INET,         #internet
    		              		   socket.SOCK_DGRAM)      #UDP
		
	def TransData(self, Message):
		self.T_msg.sendto(Message.encode(), (self.TUDP_IP, self.TUDP_PORT))

class Communicata_ARM:			#receive data from ARM and send command to ARM
	def __init__(self):
		self.ser = serial.Serial('/dev/ttyAMA0', baudrate = 115200, timeout = 1.0)

	def Readline(self):
		self.string = self.ser.readline().decode()
		return self.string

	# unfinished!!

class ReceiveUDP:		#receive command from PC
	def __init__(self):
		self.UDP_IP = '192.168.10.253'
		self.UDP_PORT = 5006		#PC to Pi

		self.s = socket.socket(socket.AF_INET,		#internet
                 			   socket.SOCK_DGRAM)	#UDP
		self.s.bind((UDP_IP, UDP_PORT))				#binding socket

	def Receive_Data(self):
	    self.data, self.addr = s.recvfrom(64)
	    # if data.decode() == 'TransfromingFinished':
	        # break
	    self.data = self.data.decode()
	    return self.data
	def judge_Type(self):
		# self.tdict = {'posture':self.Recive_Posture, 
					  # 'state':self.Recive_State}
		# if data.decode() in tdict:
			# self.verify = Transmisson()
			# self.verify.TransData('confirm')
			# self.tdict.get(data.decode)()
		self.type = ('posture', 'state')
		self.verify = Transmisson()			#just like TCP to confirm
		if self.data in self.type:
			self.verify.TransData('TypeConfirm')
			if self.data == 'posture':
				self.Recive_Posture()
			else:
				self.Recive_State
		else:
			self.verify.TransData('TypeLost')

	def Receive_Posture(self):
		self.X, self.Y ,self.A, self.Speed_X, self.speed_Y, self.Speed = tuple(eval(self.data)

	def Receive_State(self):
		self.AP, self.AI, self.AD, self.DP, self.DI, self.DD,self.End_X, self.End_Y, self.SpdMx, self.AimAg = tuple(eval(self.data)

cnt = Receive_fARM()
sdctl = Transmission()

while True:
	MESSAGE = cnt.Readline()
	sdctl.TransData(MESSAGE)