#  This file will handle all client connections to the server, sending and receiving data and coordinating
#  game logic with clients.
#
#
import socket
import time
import random
from threading import Thread
from _thread import *
import select
from questions import questions
from style import *


players = []
gameStarted = False
scoreboard = {}
isWaiting = False
answers = []
threads = []
expectedKey = ""

# to be displayed to the client in welcome screen
PORT = 1024
SERVER = socket.gethostbyname(socket.gethostname())


def initGame(numberOfRounds, questionsPerRound, players):
    print("Initializing game")
    initializeScoreBoard(players)
    for _ in range(numberOfRounds):
        StartRound(questionsPerRound)


def initializeScoreBoard(players):
    for player in players:
        scoreboard[player["username"]] = 0


def playQuestion():
    global isWaiting
    global threads
    global expectedKey
    question = random.choice(questions)
    expectedKey = question['correctKey']
    print_question(question)
    # print_question_option(question['A'])

    # print(question)
    sendToAllPlayers(question['question'] + "\n")
    sendToAllPlayers("A. " + question['A']+"\n")
    sendToAllPlayers("B. " + question['B']+"\n")
    sendToAllPlayers("C. " + question['C'] + "\n")
    sendToAllPlayers("D. " + question['D'] + "\n")

    # Collect answers:
    receiveAnswersFromPlayers(players)

    # wait for the threads to terminate
    for t in threads:
        t.join()
    print("answers received")

    for answer in answers:
        answer['answer'] = answer['answer'].upper()
        print("answer ", answer)
        if(answer['answer'] == question['correctKey']):
            isWaiting = False
            currentPoints = round(15 - answer['time'])
            scoreboard[answer['username']] += currentPoints
            sendToPlayerByUsername(answer['username'], "⭐ Correct! ⭐")
        else:
            sendToPlayerByUsername(answer['username'], "Wrong! The correct answer is " +
                                   question['correctKey'] + ": " + question[question['correctKey']])
    questions.remove(question)
    # this is the value of scoreboard : Scoreboard: {'sahar': 3, 'jjk':      ││  0}Ended Game. Thanks for playing!
    # i want to only print the values of the dictionary
    print(scoreboard)


def StartRound(questionsPerRound):
    for _ in range(questionsPerRound):
        playQuestion()
    print("Round finished!")


def startServer():
    # welcome message
    print_welcome()
    print_instructions(
        "Instructions", "red", SERVER, PORT)
    print_start_connection("Setting up connection............ ")
    # start server with socket TCP and listen for connections
    print_server_info("Server-Status", "Starting server...", "red")
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', 1234))
    print_server_info("Server-Status", "Server Started !  ", "green")
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
    print_begin_game("Type 'begin' to start the game : ")
    ans = input()
    while(ans != "begin"):
        print_begin_game("Type 'begin' to start the game : ")
        ans = input()
    global gameStarted
    gameStarted = True
    initGame(1, 3, players)
    sendToAllPlayers(str(scoreboard))
    # sendToAllPlayers("\n Ended Game. Thanks for playing!")


def playerConnectionThread(clientSocket):
    global players
    # send username request
    clientSocket.send(bytes("Enter username: ", "utf-8"))
    # receive username
    username = clientSocket.recv(1024).decode("utf-8")
    print_name_recieved(username)
    # check if username is unique
    while username in [player["username"] for player in players] or username == "":
        if(username == ""):
            clientSocket.send(
                bytes("Username can't be empty, enter a different username: ", "utf-8"))
        else:
            clientSocket.send(
                bytes("Username already taken, enter a different username: ", "utf-8"))
        # receive username
        username = clientSocket.recv(1024).decode("utf-8")
    # add player to players list
    players.append({"username": username, "connection": clientSocket})
    # send confirmation
    clientSocket.send(
        bytes("Username accepted. Waiting for game to start ...\n", "utf-8"))
    # send only the players usernames to all players
    for player in players:
        player["connection"].send(
            bytes(str([player["username"] for player in players]), "utf-8"))


def sendToAllPlayers(message):
    for player in players:
        try:
            player["connection"].send(bytes(message, "utf-8"))
        except:
            player["connection"].close()
            print("Player disconnected", player["username"])
            players.remove(player)


def sendToPlayer(player, message):  # Take a player object (dict) and a message
    try:
        player["connection"].send(bytes(message, "utf-8"))
    except:
        player["connection"].close()
        print("Player disconnected", player["username"])
        players.remove(player)


# Take a player username as a string
def sendToPlayerByUsername(playerUsername, message):
    for player in players:
        if player["username"] == playerUsername:
            try:
                player["connection"].send(bytes(message, "utf-8"))
            except:
                player["connection"].close()
                print("Player disconnected", player["username"])
                players.remove(player)


def receiveAnswerFromPlayerThread(player, answers):
    global isWaiting
    global expectedKey
    print("waiting for answer from player ", player["username"])
    sendToPlayer(player, "Enter answer: ")
    startTime = time.time()
    while (isWaiting):
        readable, writable, exceptional = select.select(
            [player["connection"]], [], [], 0.1)
        if readable:  # If there is data to be read
            answer = readable[0].recv(1024).decode("utf-8")
            print("answer received from player ",
                  player["username"], " : ", answer)
            answers.append(
                {"username": player["username"], "answer": answer, "time": time.time() - startTime})
            if (answer.upper() == expectedKey):
                isWaiting = False
            return
        if (time.time() - startTime > 15):
            isWaiting = False
    # Timeout
    print("Player ", player["username"], " didn't answer in time")
    answers.append(
        {"username": player["username"], "answer": "No answer", "time": 0})
    return


def receiveAnswersFromPlayers(players):
    global isWaiting
    isWaiting = True
    print("waiting for answers")
    global answers
    answers = []
    global threads
    threads = []
    print("players ", players)
    for player in players:
        print("Player starting")
        t = Thread(target=receiveAnswerFromPlayerThread,
                   args=(player, answers, ))
        t.start()
        threads.append(t)


if __name__ == "__main__":
    startServer()
