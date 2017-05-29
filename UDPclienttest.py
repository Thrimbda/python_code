# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-07-07 19:24:48
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-21 23:17:12
import socket

serverName = '120.27.97.44'
serverPort = 12000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = input('input lowercase message:')
clientSocket.sendto(message.encode(), (serverName, serverPort))

ModifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(ModifiedMessage)
ModifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(ModifiedMessage)
clientSocket.close()
