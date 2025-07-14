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

    while True:
        # error handling if user pick anything other than a number
        try:
            # send userInput
            userInput = input("Enter a valid number: \n")
            if not userInput.isdigit():
                raise ValueError("Invalid input")
            elif not (1 <= int(userInput) <= 5):
                raise IndexError("Invalid number")
            else:
                clientSocket.send(userInput.encode())
                getData = clientSocket.recv(1024)
                # exit out if there is no data
                if not getData:
                    break
                clientSocket.close()
                exit()
        except ValueError as v:
            print(v)
        except IndexError as i:
            print(i)
        print(clientSocket.recv(1024).decode())
connectServer()