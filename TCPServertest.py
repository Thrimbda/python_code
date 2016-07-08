import socket
serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to recive.')
while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    print(sentence)
    if sentence == '^]':
        connectionSocket.close()
        print('connection closed.')
        break
    reSentence = sentence.upper()
    connectionSocket.send(reSentence.encode())
    connectionSocket.close()
