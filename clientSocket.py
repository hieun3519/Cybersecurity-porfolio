import socket
import os

# creating client socket
clientSocket = socket.socket()

# picking port for the client to connect (same as server)
port = 80
hostname = socket.gethostname()
try:
    # connect to server
    clientSocket.connect((hostname, port))
    # if fail to connect
except ConnectionRefusedError:
    print("Fail to connect")
    clientSocket.close()

userInput = input("Enter a valid number: \n")
while clientSocket.connect():
    print("Connected")
    # send userInput
    clientSocket.send(userInput.encode())
    getData = clientSocket.recv(1024)
    # exit out if there is no data
    if not getData:
        break
    clientSocket.close()
    exit()
