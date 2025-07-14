import socket
import subprocess
import json

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
    def sendMenu(self):
        # using JSON, the options can be split similar to a dict/hashmap with key and values
        userMenu = [
        {"Option": "1", "name": "1. Ping local host" },
        {"Option": "2", "name": "2. Ping to a website"},
        {"Option": "3", "name": "3. Sending over file"},   
        {"Option": "4", "name": "4. Exit"}
        ]
        # turn the userMenu into JSON object and sending it to the client
        welcomeMenu = {"message": "Welcome to the server! Pick the following option",
                       "menu": userMenu}
        userMenuJSON = json.dumps(welcomeMenu)
        return c.sendall((userMenuJSON).encode())

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
    try:
        # receive the data if true or else break
        while True:
            server.sendMenu()
            # taking a size of 4096 bytes as a data
            data = c.recv(4096)
            if not data:
                print("Server: Closed connection")
                break
            else:
                server.accept()
                # decode the data into str and convert it to int
                decodeData = data.decode().strip()
                userChoice = int(decodeData)
                if userChoice == 1:
                    try:
                        # send 3 packets with 3000 ms delay to local host
                        sendPack = subprocess.check_output("ping -n 3 -w 3000 127.0.0.1", shell = True)
                        c.sendall(sendPack)
                    except subprocess.CalledProcessError as e:
                        # sending error message if ping doesn't work
                        errorMessage = f"Ping failed with an error code {e.returncode}".encode()
                        c.sendall(errorMessage)
                elif userChoice == 2:
                    c.sendall("Server: What website would you like to ping".encode())
                    userWebsite = c.recv(1024)
                    if not userWebsite:
                        break
                    # taking the data in byte into str and use it to ping similar to option 1
                    website = userWebsite.decode().strip()
                    try:
                        # send 3 packets with 3000 ms delay to local host
                        sendPack = subprocess.check_output(f"ping -n 3 -w 3000 {website}", shell = True)
                        c.sendall(sendPack)
                    except subprocess.CalledProcessError as e:
                        # sending error message if ping doesn't work
                        errorMessage = f"Ping failed with an error code {e.returncode}".encode()
                        c.sendall(errorMessage)
                elif userChoice == 3:
                    c.sendall("Haven't add this feature yet :(".encode())
                elif userChoice == 4:
                    c.sendall("Goodbye!".encode())
                    break
                else:
                    c.sendall("Invalid choice".encode())
    except ConnectionError:
        print("Server: Connection closed by the server")
    finally:
        # close the socket when done
        c.close()
        print("Connection closed")
            


