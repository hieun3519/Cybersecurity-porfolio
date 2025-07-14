import socket



# picking port for the client to connect (same as server)
PORT = 256
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
        print("Connected")
        # if fail to connect then exit the program
    except ConnectionRefusedError:
        print("Fail to connect")
        clientSocket.close()
        exit()

    try:
        while True:
            # error handling if user pick anything other than a number
            data = clientSocket.recv(4096)
            # error handling
            if not data:
                break
            serverMessage = data.decode()
            print("Server: ", serverMessage)
            # send userInput
            # need to implement JSON to make this easier
            userInput = input("Client: Enter a valid number: \n")
            clientSocket.send(userInput.encode())

    except ConnectionError:
        print("Client: Connection error")
    finally:
        clientSocket.close()

connectServer()