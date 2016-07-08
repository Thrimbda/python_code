import socket
serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to recive.')
while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    reSentence = sentence.upper()
    connectionSocket.send(reSentence)
    connectionSocket.close()
