# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-07-07 20:02:56
# @Last Modified by:   Macpotty
# @Last Modified time: 2016-07-07 20:44:14
import socket
serverName = '120.27.97.44'
serverPort = 12001
clienSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clienSocket.connect((serverName, serverPort))
sentence = input('Input your lowercase sentence:')
clienSocket.send(sentence.encode())
modifiedSentence = clienSocket.recv(1024).decode()
print('From server:', modifiedSentence)
clienSocket.close()
