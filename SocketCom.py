import socket
import subprocess


class serverSocket():
    # initalize the socket
    def __init__(self, sock = None):
        if sock is None:
            # try and exception handling
            try:
                # creating a server socket with AF_INET (IPv4) and SOCK_STREAM (TCP oriented protocol)
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error as err:
                print(f"Fail to create socket, {err}")
        else:
            self.socket = sock
    def bindSocket(self, name, port):
        self.socket.bind((name, port))
        print(f"Server is bind to port {port}")
    def listen(self):
        self.socket.listen()
        print(f"Server is listening on port {port}")
    def accept(self):
        return self.socket.accept()

port = 256
server = serverSocket()
server.bindSocket('127.0.0.1', port)

# listen for any client
server.listen()

while True:
    # accept connection from client
    c, addr = server.accept()
    print("Connection accepted")

    # similar to try catch with keyword
    with c:
        # send client this message
        c.sendall("Welcome to the server!\n" +
            "Pick your option: " + "1. Ping local host\n" +
            "2. Ping to a website\n" +
            "3. Exit")
        # send data if true or else break
        # while True:
        #     data = c.recv(1024)
        #     if not data:
        #         break
        #     c.sendall(data)


