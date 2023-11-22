#  This file will handle everything related to interface of the game to ensure a friendly user experience.
#
#
#
import os
import sys
import rich
from termcolor import colored, cprint
from rich import print
from rich.panel import Panel
from rich.console import Console
from questions import questions

# defining ascii strings that will have their own custom print functions

quizTrivia = """


 ██████╗ ██╗   ██╗██╗███████╗    ████████╗██████╗ ██╗██╗   ██╗██╗ █████╗
██╔═══██╗██║   ██║██║╚══███╔╝    ╚══██╔══╝██╔══██╗██║██║   ██║██║██╔══██╗
██║   ██║██║   ██║██║  ███╔╝        ██║   ██████╔╝██║██║   ██║██║███████║
██║▄▄ ██║██║   ██║██║ ███╔╝         ██║   ██╔══██╗██║╚██╗ ██╔╝██║██╔══██║
╚██████╔╝╚██████╔╝██║███████╗       ██║   ██║  ██║██║ ╚████╔╝ ██║██║  ██║
 ╚══▀▀═╝  ╚═════╝ ╚═╝╚

    """


# the following functions will be used to print the ascii strings defined above
def print_welcome():
    cprint(quizTrivia, 'green')


# panel to print server and client side info
def print_server_info(side, info, color):
    panel = Panel.fit(info,
                      title=side,
                      border_style=color,
                      title_align="left",
                      padding=(1, 2),
                      width=150
                      )
    print(panel)


# style begin instruction to start the game
def print_begin_game(text):
    cprint(text, "black", "on_yellow", attrs=["bold"])


# panel to input client ip address and port number
def get_client_info(info, color):
    panel = Panel.fit(info,
                      border_style=color,
                      title_align="left",
                      padding=(1, 2),
                      )
    print(panel)
    return ""


# print question
def print_question(question):
    cprint(question, "cyan", attrs=["bold"], )


# # print answer options
def print_question_option(option):
    cprint("A. " + option, "cyan", attrs=["bold"], file=sys.stderr)


def print_recv_data(data):
    # if data string starts with Wrong or Correct, print it in red
    if data.startswith("Wrong"):
        cprint("\n"+data+"\n", "red", attrs=["bold"])
    elif data.startswith("⭐"):
        cprint("\n"+data+"\n", "yellow", attrs=["bold"])
    # to test latest print for sccoreboard
    elif data.startswith("Scoreboard"):
        panel = Panel.fit(data,
                          border_style="cyan",
                          title_align="left",
                          padding=(1, 2),
                          )
        print(panel)
    ##############################
    else:
        cprint("\n"+data+"\n", "green", attrs=["bold"])


def print_start_game():
    print("""
   _____ _             _   _                _____
  / ____| |           | | (_)              / ____|
 | (___ | |_ __ _ _ __| |_ _ _ __   __ _  | |  __  __ _ _ __ ___   ___
  \___ \| __/ _` | '__| __| | '_ \ / _` | | | |_ |/ _` | '_ ` _ \ / _ \
  ____) | || (_| | |  | |_| | | | | (_| | | |__| | (_| | | | | | |  __/_ _ _
 |_____/ \__\__,_|_|   \__|_|_| |_|\__, |  \_____|\__,_|_| |_| |_|\___(_|_|_)
                                    __/ |
                                   |___/
    """)
