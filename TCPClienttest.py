#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-07-07 20:02:56
# @Last Modified by:   Macpotty
# @Last Modified time: 2016-07-07 20:44:14
import socket
import time

serverName = '192.168.0.136'
serverPort = 12001
clienSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clienSocket.connect((serverName, serverPort))
sentence = input('Input your lowercase sentence:')
clienSocket.send(sentence.encode())
timeStamp = time.time()
modifiedSentence = clienSocket.recv(1024).decode()
timeStamp  = time.time() - timeStamp
print('From server:%s\n' % modifiedSentence, 'Transport using:%.4f' % timeStamp)
clienSocket.close()

