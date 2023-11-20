#  This file will handle all client connections to the server and sending and receiving data.
# 
#
#
import socket

def connectToServer(address, port):
    print("Connecting to server")
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((address, port))
    print("Connected to server")
    return clientSocket

if __name__ == "__main__":
    # connect to server
    address = input("Enter server address: (if left blank, will use localhost) ")
    if address == "":
        address = socket.gethostname()
    port = input("Enter server port: (if left blank, will use 1234) ")
    if port == "":
        port = 1234
    else:
        port = int(port)
    clientSocket = connectToServer(address, 1234)
    # receive username request
    username = clientSocket.recv(1024).decode("utf-8")
    # send username
    username = input(username)
    while(username==""):
        print("Username can't be empty. Try again : ",username)
        username = input(username)
    clientSocket.send(bytes(username, "utf-8"))
    # receive confirmation
    confirmation = clientSocket.recv(1024).decode("utf-8")
    print(confirmation)
    # check if username was accepted
    while "Username accepted." not in confirmation:
        user = input("Username taken. Enter new username: ")
        clientSocket.send(bytes(user, "utf-8"))
        confirmation = clientSocket.recv(1024).decode("utf-8")
        print(confirmation)
    # receive player list
    print("out of loop")
    players = clientSocket.recv(1024).decode("utf-8")
    print(players)
    # start game
    # Keep the connection open:
    while True:
        # receive data
        data = clientSocket.recv(1024).decode("utf-8")
        # check if data is empty
        if not data:
            break
        # print received data
        print("Received:", data)
        
        # send data
        message = input("Enter message to send: ")
        clientSocket.send(bytes(message, "utf-8"))
