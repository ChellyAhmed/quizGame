#  This file will handle all client connections to the server, sending and receiving data and coordinating
#  game logic with clients.
#
#
import socket
from _thread import *

players = []

def startServer():
    # start server with socket TCP and listen for connections
    print("Starting server")
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((socket.gethostname(), 1234))
    serverSocket.listen()
    while True:
        # accept connections
        clientSocket, address = serverSocket.accept()
        print(f"Connection from {address} has been established!")
        # start thread to handle client connection
        start_new_thread(playerConnectionThread, tuple([clientSocket]))


def playerConnectionThread(clientSocket):
    # send username request
    clientSocket.send(bytes("Enter username: ", "utf-8"))
    # receive username
    username = clientSocket.recv(1024).decode("utf-8")
    # check if username is unique
    while username in [player["username"] for player in players]:
        # send username request
        clientSocket.send(bytes("Username already taken, enter a different username: ", "utf-8"))
        # receive username
        username = clientSocket.recv(1024).decode("utf-8")
    # add player to players list
    players.append({"username": username, "connection": clientSocket})
    # send confirmation
    clientSocket.send(bytes("Username accepted. Waiting for game to start ...\n", "utf-8"))
    # send player list to all players
    for player in players:
        player["connection"].send(bytes(str(players), "utf-8"))


def sendToAllPlayers(message):
    for player in players:
        try:
            player["connection"].send(bytes(message, "utf-8"))
        except:
            player["connection"].close()
            print("Player disconnected", player["username"])
            players.remove(player)

def sendToPlayer(player, message):
    try:
        player["connection"].send(bytes(message, "utf-8"))
    except:
        player["connection"].close()
        print("Player disconnected", player["username"])
        players.remove(player)

def receiveAnswerFromPlayerThread(player,answers):
    answer = player["connection"].recv(1024).decode("utf-8")
    answers.append({"username": player["username"], "answer": answer})
    

def receiveAnswersFromPlayers():
    answers = []
    for player in players:
        start_new_thread(receiveAnswerFromPlayerThread, (player,answers))
    while len(answers) < len(players):
        pass
    return answers

if __name__ == "__main__":
    startServer()
    