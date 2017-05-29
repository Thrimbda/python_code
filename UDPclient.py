import socket
serverName = '120.27.97.44'
serverPort = 12000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = input('input lowercase message:')
clientSocket.sendto(message.encode(), (serverName, serverPort))
ModifiedMessage, remoteAddr = clientSocket.recvfrom(2048)
print(ModifiedMessage, ModifiedMessage.decode())
addr = eval(ModifiedMessage.decode())
print(type(addr), addr)
clientSocket.sendto('hello from another planet'.encode(), addr)
clientSocket.close()
