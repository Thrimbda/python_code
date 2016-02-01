import socket

class Transmission:
	def __init__(self):
		self.UDP_IP = '192.168.10.151'
		self.UDP_PORT = 5006

		self.s = socket.socket(socket.AF_INET,         #internet
    		          	       socket.SOCK_DGRAM)      #UDP
		
	def TransData(self, Message):
		msg = Message
		self.s.sendto(msg.encode(), (self.UDP_IP, self.UDP_PORT))