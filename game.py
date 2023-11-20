#  This file will handle all game logic such as starting the game, getting the next question, 
#  checking if the answer is correct, and getting the scoreboard. 
#
#

from questions import questions
from server import *
import random
import time

scoreboard = {}

#TODO
def initGame(numberOfRounds, questionsPerRound, players):
    print("Initializing game")
    initializeScoreBoard(players)
    for i in range(numberOfRounds):
        StartRound(questionsPerRound)
    
#TODO
def getNextQuestion():
    print("Getting next question")

#TODO
def checkIfAnswerCorrect(): 
    print("Checking if answer is correct")

#TODO
def getScoreboard(): #Displays in the server console
    print("Getting scoreboard")

def display(message): #Displays in the server console
    #TODO
    print(message)

def initializeScoreBoard(players): 
    for player in players:
        scoreboard[player["username"]] = 0

def playQuestion(): 
    question = random.choice(questions)
    print(question)
    sendToAllPlayers(question['question'])
    sendToAllPlayers("A: " + question['A']) 
    sendToAllPlayers("B: " + question['B'])
    sendToAllPlayers("C: " + question['C'])
    sendToAllPlayers("D: " + question['D'])

    #Collect answers:
    answers = receiveAnswersFromPlayers(players)

    for answer in answers:
        if(answer['answer'] == question['correctKey']):
            currentPoints = round(15 - answer['time'])
            scoreboard[answer['username']] += currentPoints
            sendToPlayer(answer['username'], "Correct!")
        else:
            sendToPlayer(answer['username'], "Wrong! The correct answer is " + question['correctKey'] + ": " + question[question['correctKey']])
    questions.remove(question)


def StartRound(questionsPerRound): 
    for i in range(questionsPerRound):
        playQuestion()
    display("Round finished!")
    getScoreboard()
