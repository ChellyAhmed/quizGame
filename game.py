import random
import time

questions = []
#TODO: Move questions to a file and read from it instead of hardcoding (Lowest priority)
questions.append({'question': "What is the capital of Tunisia",
                  'A': "Sfax",
                  'B': "Tunis",
                  'C': "Sousse",
                  'D': "Gabes",
                  'correctKey': "B"})
questions.append({'question': "What is the capital of France",
                    'A': "Paris",
                    'B': "Marseille",
                    'C': "Lyon",
                    'D': "Toulouse",
                    'correctKey': "A"})
questions.append({'question': "What is the capital of Germany",
                    'A': "Cologne",
                    'B': "Hamburg",
                    'C': "Munich",
                    'D': "Berlin",
                    'correctKey': "D"})
questions.append({'question': "What is the capital of Italy",
                    'A': "Rome",
                    'B': "Milan",
                    'C': "Naples",
                    'D': "Turin",
                    'correctKey': "A"})
questions.append({'question': "What is the capital of Spain",
                    'A': "Valencia",
                    'B': "Barcelona",
                    'C': "Madrid",
                    'D': "Seville",
                    'correctKey': "C"})
questions.append({'question': "What is the capital of Portugal",
                    'A': "Porto",
                    'B': "Lisbon",
                    'C': "Coimbra",
                    'D': "Braga",
                    'correctKey': "B"})
questions.append({'question': "What is the square of -11",
                  'A': "144",
                  'B': "121",
                  'C': "169",
                  'D': "100",
                  'correctKey': "B"})
questions.append({'question': "What is the square of 12",
                  'A': "144",
                  'B': "121",
                  'C': "169",
                  'D': "100",
                  'correctKey': "A"})
questions.append({'question': "What is the square of 9",
                  'A': "89",
                  'B': "121",
                  'C': "72",
                  'D': "81",
                  'correctKey': "D"})
questions.append({'question': "What is the square root of 64",
                    'A': "8",
                    'B': "6",
                    'C': "7",
                    'D': "9",
                    'correctKey': "A"})
questions.append({'question': "What is the square root of 100",
                    'A': "8",
                    'B': "6",
                    'C': "7",
                    'D': "10",
                    'correctKey': "D"})
questions.append({'question': "What is the square root of 49",
                    'A': "8",
                    'B': "6",
                    'C': "7",
                    'D': "9",
                    'correctKey': "C"})

scoreBoard = dict()

clientsNames = ["user1" , "user2" , "user3" , "user4" , "user5" ]

#TODO: Configure connections

def sendToClientByUserName(userName, message):
    #TODO: get code from Sahar
    print("Sending to " + userName + ": " + message)

def sendToAllClients(message):
    #TODO: get code from Sahar
    print("Sending to all clients: " + message)

def receiveFromUser():
    #TODO: synchronize code with Amine
    randomNumber= random.randint(0,5)
    userName = "user" + str(randomNumber)

def displayScoreBoard(): 
    #TODO: get code from Khalil
    print("ScoreBoard: ")
    print(scoreBoard)

def display(message): #Displays in the server console
    #TODO: get code from Khalil
    print(message)

def StartGame(questionsPerRound, numberOfRounds):
    #TODO: get code from Amine
    print("Startinng game")

def initializeScoreBoard(): #Ahmed
    for user in clientsNames:
        scoreBoard[user] = 0

def playQuestion(): #Ahmed
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
    displayScoreBoard()
