#  This file will handle all client connections to the server, sending and receiving data and coordinating
#  game logic with clients.
#
#
import socket
import time
from threading import Thread
from _thread import *
import game

players = []
gameStarted = False

def startServer():
    # start server with socket TCP and listen for connections
    print("Starting server")
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', 1234))
    print("server started")
    serverSocket.listen()
    # start thread to handle game logic
    start_new_thread(serverGameThread, ())
    while not gameStarted:
        # accept connections
        clientSocket, address = serverSocket.accept()
        print(f"Connection from {address} has been established!")
        # start thread to handle client connection
        start_new_thread(playerConnectionThread, tuple([clientSocket]))


def serverGameThread():
    print("Type 'begin' to start the game")
    ans = input()
    while(ans!="begin"):
        print("Type 'begin' to start the game")
        ans = input()
    sendToAllPlayers("Game has begun")
    sendToAllPlayers("Game has begun")
    sendToAllPlayers("Game has begun")
    sendToAllPlayers("Game has begun")
    sendToAllPlayers("Game has begun")
    global gameStarted
    gameStarted = True
    game.initGame(1,3,players)
    sendToAllPlayers("Ended thread")

    


def playerConnectionThread(clientSocket):
    global players
    # send username request
    clientSocket.send(bytes("Enter username: ", "utf-8"))
    # receive username
    username = clientSocket.recv(1024).decode("utf-8")
    print("username received ",username)
    # check if username is unique
    while username in [player["username"] for player in players] or username=="":
        if(username==""):
            clientSocket.send(bytes("Username can't be empty, enter a different username: ", "utf-8"))
        else:
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

def sendToPlayerByUsername(playerUsername, message):
    for player in players:
        if player["username"] == playerUsername:
            try:
                player["connection"].send(bytes(message, "utf-8"))
            except:
                player["connection"].close()
                print("Player disconnected", player["username"])
                players.remove(player)

def receiveAnswerFromPlayerThread(player,answers):
    print("waiting for answer from player ",player["username"])
    sendTime = time.time()
    while(time.time() - sendTime < 15):
        answer = player["connection"].recv(1024).decode("utf-8")
        answers.append({"username": player["username"], "answer": answer, "time": time.time() - sendTime})
        print(answer)
        print("got answer from ",player["username"])
    answers.append({"username": player["username"], "answer": "No answer", "time": time.time() - sendTime})
    

def receiveAnswersFromPlayers():
    print("waiting for answers")
    answers = []
    threads = []
    print("players ",players)
    for player in players:
        print("Player starting")
        t = Thread(target=receiveAnswerFromPlayerThread, args=(player,answers, ))
        t.start()
        print("thread started")
        threads.append(t)
    for t in threads:
        t.join()
    return answers

if __name__ == "__main__":
    startServer()
    