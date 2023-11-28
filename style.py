#  This file will handle everything related to interface of the game to ensure a friendly user experience.
#
#
#

import sys
from termcolor import colored, cprint
from rich import print as rprint  # maybe import this as rprint
from rich.panel import Panel
from rich.console import Console
from questions import questions
from strings import *
from rich.style import Style
from rich.table import Table


# table.add_column("Released", justify="right", style="cyan", no_wrap=True)

danger_style = Style(color="green", blink=True, bold=True)
console = Console()

# the following functions will be used to print the ascii strings defined above


def print_welcome():
    # print(quizTrivia, style=danger_style)
    # console.print(quizTrivia, style=danger_style)
    print(f'\033[1;35;40m {border}')
    cprint(quizTrivia, 'green', attrs=['blink'])
    print(f'\033[1;35;40m {border}')
    print('\n')

# panel to print server and client side info


def print_instructions(title, color, server_ip, server_port):
    panel = Panel.fit(f" The players must connect with the following parameters : \n\033[1;36;40m server : \033[1;33;40m {server_ip} \n\033[1;36;40m port : \033[1;33;40m {server_port}",
                      title=title,
                      border_style=color,
                      title_align="left",
                      padding=(1, 2),
                      width=150
                      )
    rprint(panel)


# panel to print server and client side info
def print_server_info(side, info, color):
    panel = Panel.fit(info,
                      title=side,
                      border_style=color,
                      title_align="left",
                      padding=(1, 2),
                      width=150
                      )
    rprint(panel)


# style begin instruction to start the game
def print_begin_game(text):
    cprint(text, "black", "on_yellow", attrs=["bold"])


def print_start_connection(text):
    print("\n")
    cprint(text, "black", "on_green", attrs=["bold"])
    print("\n")


# panel to input client ip address and port number
def get_client_info(info, color):
    panel = Panel.fit(info,
                      border_style=color,
                      title_align="left",
                      padding=(1, 2),
                      )
    rprint(panel)
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
    elif data.startswith("{'"):
        panel = Panel.fit(f'{data} \n \n \033[1;36;40m Round ended, Thanks for playing!',
                          border_style="yellow",
                          title_align="left",
                          title="Scoreboard",
                          padding=(1, 2),
                          )
        rprint(panel)
    elif data.startswith("Ended"):
        cprint("\n"+data+"\n", "cyan", attrs=["bold"])

    ##############################
    else:
        cprint("\n"+data+"\n", "green", attrs=["bold"])

# client side


def print_name_recieved(name):
    cprint(f"Welcome \033[1;33;40m{name}!\n",
           "cyan", attrs=["bold"], file=sys.stderr)


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
