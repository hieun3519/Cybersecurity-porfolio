import socket
import subprocess

# def getUserInput(input):
#     # switch case just to be fancy
#     numInput = int(input)
#     match numInput:
#         case 1:
#             print(socket.gethostname())
#
#             return
#         case 2:
#             return
#         case 3:
#
#         case _:
#             return "Invalid Input!"
serverSocket = socket.socket()
# try and exception handling
try:
    # creating a server socket with AF_INET (IPv4) and SOCK_STREAM (TCP oriented protocol)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print(f"Fail to create socket, {err}")

port = 256
serverSocket.bind(('', port))
print(f"Server is bind to port {port}")
# listen for any client
serverSocket.listen()

# can put this in a def
while True:
    # accept connection from client
    c, addr = serverSocket.accept()
    print("Connection accepted")

print("Welcome to the server!\n" +
      "Pick your option: " + "1. Ping local host\n" +
      "2. Ping to a website\n" +
      "3. Exit")
#userInput = input("Enter a valid number: \n")
# while userInput != 3:
#getUserInput(userInput)



