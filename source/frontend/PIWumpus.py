import aiohttp
import asyncio
import kbhit
import os
import sys
import time
import WumpusGameEngine

# Constants
ESC = chr(27)
ANSI = ESC + "["
CR = chr(13)

CHAT_START = 8
CHAT_END = 22
INPUT_LINE = 24

REFRESH_INTERVAL = 0.5

HOST = 'localhost'
PORT = '8080'

# Utils
def enable_ansi():
    if sys.platform[0 : 3] == "win":
        os.system('')

def clear_screen():
    print_part(ANSI + "2J")

def move_line(n):
    print_part(ANSI + str(n) + "H")

def erase_line(n):
    move_line(n)
    print_part(ANSI + "K")

def erase_lines(start, end):
    for line in range(start, end + 1):
        erase_line(line)

def print_part(s):
    print(s, end="", flush=True)

def input_async(timeout, echo=True):
    kb = kbhit.KBHit()

    ret = ""
    elapsed = 0
    while True:
        if kb.kbhit():
            c = kb.getch().capitalize()
            ret += c
            if echo==True:
                print_part(c)
            if c == CR:
                break
        else:
            time.sleep(0.1)
            elapsed += 0.1
            if elapsed > timeout:
                break
    return ret

# App Code
def list_users():
    print("TODO: get and print users")

def lobby_screen(login):
    clear_screen()
    print("Hello {}! You are now in the lobby. Other nervous engineers that are avoiding eye contact are:".format(login))
    print()
    list_users()
    print()
    print("Press the ENTER (or RETURN) key to start with the current players")
    while True:
        input = input_async(REFRESH_INTERVAL, echo=False)
        if len(input) > 0 and input[-1]==CR:
            break

chat_line = CHAT_START

def add_chat(s):
    global chat_line

    move_line(chat_line)
    print_part(s)
    chat_line = chat_line + 1
    if (chat_line > CHAT_END):
        chat_line = CHAT_START
        erase_lines(CHAT_START, CHAT_END)

def get_cmd():
    cmd = ""

    while True:
        erase_line(INPUT_LINE)
        print_part("> {}".format(cmd))

        input = input_async(REFRESH_INTERVAL)
        cmd += input
        if len(cmd) > 0 and cmd[-1]==CR:
            cmd = cmd.rstrip()
            done = True
            break
    return cmd

async def idle(session):
    # TODO poll server for chats
    add_chat("TODO: Print other users commands")
    # TODO poll server for round results
    await tryGetVoteResult(session, URL)

async def game_screen(session):
    clear_screen()
    print("Hold down CTRL and press C (and ignore the call stack) to quit ...")
    print()

    WumpusGameEngine.displayRoomInfo()
    while True:
        cmd = get_cmd()
        idle(session)
        print()
        await convert_cmd_to_request(cmd, session)
        print("TODO: Send '{}' to server".format(cmd))

def isInteger(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

async def convert_cmd_to_request(command, session):
    # JSH Assumption: It is better to have parsed the command into constituent parts for the backend
    # Move (M), Shoot (S), or Quit (Q)
    # TODO: We need to validate input sent to server.
    split_command = command.split()
    if len(split_command) > 1:
        if (isInteger(split_command[1])):
            if (split_command[0] == "MOVE" or split_command[0] == "M"):
                print("Sending Server Vote for MOVE")
                await postMoveVote(session, URL, {"MOVE" : split_command[1]})
            elif (split_command[0] == "SHOOT" or split_command[0] == "S"):
                print("Sending Server Vote for SHOOT")
                await postMoveVote(session, URL, {"SHOOT" : split_command[1]})
    else:
        if (command == "QUIT" or command == "Q"):
            sys.exit(0)
            # TODO: Client gracefully exits the game
            print("TODO: Client gracefully exits the game")
        if (command == "HELP" or command == "H"):
            print("Requesting help...")
            WumpusGameEngine.show_instructions()

async def postMoveVote(session, url, data):
    # InsertValue API call
    async with session.post(url, json=data) as response:
        return await response.text()

async def postStartGame(session, url, data):
    # StartGame API call
    async with session.post(url, json=data) as response:
        return await response.text()

async def postRegisterUser(session, url, data):
    # RegisterUser API call
    async with session.post(url, json=data) as response:
        return await response.text()

async def getListUsers(session, url):
    # ListUsers API call
    async with session.get(url) as response:
        return await response.text()

# TODO: need to add round number...
async def tryGetVoteResult(session, url):
    # TryGetAgreggate API call
    async with session.get(url) as response:
        return await response.text()

async def main():
    global URL
    
    enable_ansi()
    WumpusGameEngine.init()

    clear_screen()
    print("Welcome to PI Wumpus!")
    print()
    print("Please enter your name, handle, or other identifier:")

    login = input()
    lobby_screen(login)

    clear_screen()
    WumpusGameEngine.banner()

    async with aiohttp.ClientSession() as session:
        URL = 'http://{}:{}'.format(HOST, PORT)
        await game_screen(session)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
