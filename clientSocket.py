import socket
import json
from json import JSONDecodeError

# picking port for the client to connect (same as server)
PORT = 4557
HOSTNAME = '127.0.0.1'

def connectServer():
    # creating client socket
    clientSocket = socket.socket()

    # picking port for the client to connect (same as server)
    global PORT
    global HOSTNAME
    try:
        # connect to server
        clientSocket.connect((HOSTNAME, PORT))
        print("Connected\n")
        # if fail to connect then exit the program
    except ConnectionRefusedError:
        print("Fail to connect\n")
        clientSocket.close()
        exit()

    try:
        while True:
            # error handling if user pick anything other than a number
            data = clientSocket.recv(4096)
            # error handling
            if not data:
                break

            # parsing the JSON from the server by deserializing the json
            try:
                serverMessage = json.loads(data.decode())
            except JSONDecodeError:
                print("Server sent invalid data\n")
                break
            # print out message and menu declared in socketCom to the user
            if "message" in serverMessage:
                print("Server: ", serverMessage["message"], "\n")
            if "menu" in serverMessage:
                print("Server: ", serverMessage["menu"], "\n")
            if "output" in serverMessage:
                print("Server: ", serverMessage["output"], "\n")
            try:
                userInput = input("Client: Enter another option: \n")
                if not 1 <= int(userInput) <= 4:
                    print("Please enter the number within the range")
                    continue
                # using json we can formulate a dict to send it back to the server based on user Input
                if int(userInput) == 2:
                    # user need to enter the website
                    enterWebsite = input("Enter website to ping: ").strip()
                    if "www." in enterWebsite:
                        sendMessage = {
                            "option": 2,
                            "website": enterWebsite
                        }
                    else:
                        print("Website field needs a World Wide Web and a dot in the name, try again")
                        break
                else:
                    sendMessage = {
                        "option": int(userInput)
                    }
                # sending a serialize json message to the server
                clientSocket.send(json.dumps(sendMessage).encode())
            except ValueError:
                print("Invalid input")
            except ConnectionError:
                print("Client: Connection error")
    except ConnectionError:
        print("Client: Connection error")
    finally:
        clientSocket.close()

connectServer()