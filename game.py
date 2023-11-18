#  This file will handle all game logic such as starting the game, getting the next question, 
#  checking if the answer is correct, and getting the scoreboard. 
#
#

from questions import questions

#TODO
def initGame(numberOfRounds, questionsPerRound):
    print("Initializing game")
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


def sendToClientByUserName(userName, message):
    #TODO
    print("Sending to " + userName + ": " + message)

def sendToAllClients(message):
    #TODO
    print("Sending to all clients: " + message)

def receiveFromUser():
    #TODO: synchronize code with Amine
    randomNumber= random.randint(0,5)
    userName = "user" + str(randomNumber)

def display(message): #Displays in the server console
    #TODO
    print(message)

def initializeScoreBoard(players): 
    for player in players:
        scoreBoard[player["username"]] = 0

def playQuestion(): 
    question = random.choice(questions)
    sendTime = time.time()
    sendToAllClients(question['question'])
    sendToAllClients("A: " + question['A']) 
    sendToAllClients("B: " + question['B'])
    sendToAllClients("C: " + question['C'])
    sendToAllClients("D: " + question['D'])

    #Collect answers:
    while(time.time() - sendTime < 15):
        answer = receiveFromUser()
        #TODO: Double check with Amine the implementation of receiveFromUser()
        if (answer ):
            if(answer['answer'] == question['correctKey']):
                currentPoints = round(15 - (time.time() - sendTime))
                scoreBoard[answer['userName']] += currentPoints
                sendToClientByUserName(answer['userName'], "Correct!")
            else:
                sendToClientByUserName(answer['userName'], "Wrong! The correct answer is " + question['correctKey'] + ": " + question[question['correctKey']])
    questions.remove(question)


def StartRound(questionsPerRound): 
    #TODO: Synchronize code between Ahmed and Amine
    initializeScoreBoard()
    for i in range(questionsPerRound):
        playQuestion()
    display("Round finished!")
    getScoreBoard()
