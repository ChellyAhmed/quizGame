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
    clientSocket = connectToServer(socket.gethostname(), 1234)
    # receive username request
    username = clientSocket.recv(1024).decode("utf-8")
    # send username
    username = input(username)
    clientSocket.send(bytes(input(username), "utf-8"))
    # receive confirmation
    confirmation = clientSocket.recv(1024).decode("utf-8")
    print(confirmation)
    # check if username was accepted
    while confirmation != "Username accepted. Waiting for game to start ...":
        user = input("Username taken. Enter new username: ")
        clientSocket.send(bytes(user, "utf-8"))
        confirmation = clientSocket.recv(1024)
        print(confirmation)
    # receive player list
    players = clientSocket.recv(1024).decode("utf-8")
    print(players)
    # start game
    


