import socket
import subprocess
import json
from json import JSONDecodeError
import platform


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
    def sendMenu(self, client):
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
        return client.sendall((userMenuJSON).encode())

    def get_ping_command(self, host):
        if platform.system() == "Windows":
            return ["ping", "-n", "3", "-w", "3000", host]
        else:
            return ["ping", "-c", "3", host]


port = 4557
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
            # send client the menu
            server.sendMenu(c)
            # taking a size of 4096 bytes as a data
            data = c.recv(4096)
            if not data:
                print("Server: Closed connection")
                break
            else:
                # parsing the JSON from the client by deserializing the json
                try:
                    clientMessage = json.loads(data.decode())
                except JSONDecodeError:
                    print("Server sent invalid data\n")
                    break
                # since clientMessage is a dict, we get the number based on option
                # default to 0 if there is no key enter
                userChoice = int(clientMessage.get("option", 0))
                if userChoice == 1:
                    try:
                        ping_cmd = server.get_ping_command("127.0.0.1")
                        sendPack = subprocess.check_output(ping_cmd)
                        output = sendPack.decode()
                        serverResponse = {
                            "message": "Ping result:",
                            "output": output
                        }
                        c.sendall(json.dumps(serverResponse).encode())

                    except subprocess.CalledProcessError as e:
                        errorOutput = f"Ping failed with return code {e.returncode}"
                        serverResponse = {
                            "message": "Ping result:",
                            "output": errorOutput
                        }
                        c.sendall(json.dumps(serverResponse).encode())
                elif userChoice == 2:
                    website = clientMessage.get("website", "")
                    try:
                        # send 3 packets with 3000 ms delay to local host
                        getPing = server.get_ping_command(website)
                        sendPack = subprocess.check_output(getPing)
                        # sending the response in a form of json since the client is expecting to receive
                        # json format
                        serverResponse = {
                            "message": "Ping result: ",
                            "output": sendPack.decode() # decode the serial of the subprocess function
                        }
                        c.sendall(json.dumps(serverResponse).encode())
                    except subprocess.CalledProcessError as e:
                        # sending error message if ping doesn't work
                        errorMessage = f"Ping failed with an error code {e.returncode}".encode()
                        c.sendall(errorMessage)
                elif userChoice == 3:
                    serverResponse = {
                        "message": "Ping result: ",
                        "output": "Haven't add this feature yet :("  # decode the serial of the subprocess function
                    }
                    c.sendall(json.dumps(serverResponse).encode())
                elif userChoice == 4:
                    serverResponse = {
                        "message": "Ping result: ",
                        "output": "Goodbye"  # decode the serial of the subprocess function
                    }
                    c.sendall(json.dumps(serverResponse).encode())
                    break
                else:
                    serverResponse = {
                        "message": "Invalid option",
                        "output": ""
                    }
                    c.sendall(json.dumps(serverResponse).encode())

    except ConnectionError:
        print("Server: Connection closed by the server")
    finally:
        # close the socket when done
        c.close()
        print("Connection closed")
            


