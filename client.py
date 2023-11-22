#  This file will handle all client connections to the server and sending and receiving data.
#
#
#
import socket
from _thread import *
from style import *


def connectToServer(address, port):
    print_server_info("Client-Status", "Connecting to server...", "red")
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((address, port))
    print_server_info("Client-Status", "Connected to server !  ", "green")
    return clientSocket


if __name__ == "__main__":
    # welcome message
    print_welcome()
    # connect to server
    address = input(get_client_info(
        "Enter server address (if left blank, will use localhost) : ", "blue"))
    if address == "":
        address = "localhost"
    port = input(get_client_info(
        "Enter server port: (if left blank, will use 1234) : ", "blue"))
    if port == "":
        port = 1234
    else:
        port = int(port)
    clientSocket = connectToServer(address, 1234)
    # receive username request
    username = clientSocket.recv(1024).decode("utf-8")
    # send username
    username = input(username)
    while(username == ""):
        print("Username can't be empty. Try again : ", username)
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

    def sendThread(clientSocket):
        while True:
            message = input()
            clientSocket.send(bytes(message, "utf-8"))

    def receiveThread(clientSocket):
        while True:
            data = clientSocket.recv(1024).decode("utf-8")
            if not data:
                break
            print_recv_data(data)

    # start send thread
    start_new_thread(sendThread, tuple([clientSocket]))
    # start receive thread
    start_new_thread(receiveThread, tuple([clientSocket]))

    while True:
        pass
    # # Keep the connection open:
    # while True:
    #     # receive data
    #     data = clientSocket.recv(1024).decode("utf-8")
    #     # check if data is empty
    #     if not data:
    #         break
    #     # print received data
    #     print(data )

    #     if ("Enter answer: " in data) :
    #         answer = input()
    #         clientSocket.send(bytes(answer, "utf-8"))
    #     else:
    #         print("\n")
