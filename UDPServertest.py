import socket
serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print('The server is ready to recive.')
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print(message)
    modifyedMessage = message.upper()
    serverSocket.sendto(modifyedMessage, clientAddress)
