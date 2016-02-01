import numpy as np
import matplotlib.pyplot as plt
import socket

Pi_IP = '192.168.10.151'
Pi_PORT = 5005

s = socket.socket(socket.AF_INET,		#internet
				  socket.SOCK_DGRAM)	#UDP
s.bind((Pi_IP, Pi_PORT)		#binding ip and port

while True:
	data, addr = recvfrom(64)
	X, Y = tuple(eval(data.decode()))		#split data and assign to X Y
	plt.scatter(X, Y, s = 1, c = green, alpha)		#draw the route