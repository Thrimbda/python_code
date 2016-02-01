#so this is for receive
import socket
import math
import Trans_UDP

class Recv_UDP:
	def __init__(self, IPaddress, Port, timeout):
		self.UDP_IP = IPaddress
		self.UDP_PORT = Port		#Pi to PC
		socket.setdefaulttimeout(timeout)
		self.s = socket.socket(socket.AF_INET,		#internet
                  socket.SOCK_DGRAM)	#UDP
		self.s.bind((self.UDP_IP, self.UDP_PORT))				#binding socket
		# self.X, self.Y ,self.A, self.Speed_X, self.speed_Y, self.Speed, self.AP, self.AI, self.AD, self.DP, self.DI, self.DD,self.End_X, self.End_Y, self.SpdMx, self.AimA = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

	def Receive_Data(self):
	    self.data, self.addr = self.s.recvfrom(128)
	    # if data.decode() == 'TransfromingFinished':
	        # break
	    self.type,self.info = tuple(eval(self.data.decode()))

	# def Judge_Type(self):
		# mydraw = drawRoute.graph()
		# while True:
			# self.Receive_Data()
			# if self.type in self.typelist:
				# if self.type == 'posture':
					# self.Receive_Posture()
					# #mydraw.
				# else:
					# self.Receive_State()

	def Receive_Posture(self):
		self.Receive_Data()
		self.X, self.Y ,self.A, self.Speed_X, self.speed_Y, self.Speed = self.info

	def Receive_State(self):
		self.AP, self.AI, self.AD, self.DP, self.DI, self.DD,self.End_X, self.End_Y, self.SpdMx, self.AimA = self.info 