import aiohttp
import asyncio
import kbhit
import os
import sys
import time
import ctypes
import WumpusGameEngine

# Constants
ESC = chr(27)
ANSI = ESC + "["
CR = chr(13)

CHAT_START = 8
CHAT_END = 22
INPUT_LINE = 24

REFRESH_INTERVAL = 0.5

HOST = 'votepolling.azurewebsites.net'
PORT = '443'
TOKEN = '' # DON'T CHECK ME IN

# Utils
def set_font(font_name):
    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11

    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class CONSOLE_FONT_INFOEX(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("nFont", ctypes.c_ulong),
                    ("dwFontSize", COORD),
                    ("FontFamily", ctypes.c_uint),
                    ("FontWeight", ctypes.c_uint),
                    ("FaceName", ctypes.c_wchar * LF_FACESIZE)]

    font = CONSOLE_FONT_INFOEX()
    font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
    font.nFont = 12
    font.dwFontSize.X = 11
    font.dwFontSize.Y = 18
    font.FontFamily = 54
    font.FontWeight = 400
    font.FaceName = font_name

    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, ctypes.c_long(False), ctypes.pointer(font))

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
    await tryGetVoteResult(session, BASEURL)

async def game_screen(session):
    clear_screen()
    print("Hold down CTRL and press C (and ignore the call stack) to quit ...")
    print()

    WumpusGameEngine.displayRoomInfo()
    while True:
        cmd = get_cmd()
        print()
        
        await convert_cmd_to_request(cmd, session)
        await idle(session)

def isInteger(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

async def convert_cmd_to_request(command, session):
    # JSH Assumption: It is better to have parsed the command into constituent parts for the backend
    # Move (M), Shoot (S), or Quit (Q)

    error = False
    split_command = command.split()
    if len(split_command) > 1:
        if (isInteger(split_command[1])):
            if (split_command[0] == "MOVE" or split_command[0] == "M"):
                print("Sending Server Vote for MOVE")
                await postMoveVote(session, BASEURL, {"WumpusAction" : "Move", "Room" : split_command[1], "MoveNumber" : WumpusGameEngine.moveCount, "UserName" : login})
            elif (split_command[0] == "SHOOT" or split_command[0] == "S"):
                print("Sending Server Vote for SHOOT")
                await postMoveVote(session, BASEURL, {"WumpusAction" : "Shoot", "Room" : split_command[1], "MoveNumber" : WumpusGameEngine.moveCount, "UserName" : login})
            else:
                error = True
        else:
            error = True
    else:
        if (command == "QUIT" or command == "Q"):
            sys.exit(0)
        elif (command == "HELP" or command == "H"):
            print("Requesting help...")
            WumpusGameEngine.show_instructions()
        else:
            error = True

    if error==True:
        print_part(" **What??")
    else:
        erase_line(INPUT_LINE + 1)

async def postMoveVote(session, baseurl, data):
    # InsertVote API call
    fullurl = '{}/{}?code={}'.format(baseurl,'InsertVote',TOKEN)
    async with session.post(fullurl, json=data) as response:
        return await response.text()

async def postStartGame(session, baseurl, data):
    # StartGame API call
    fullurl = '{}/{}?code={}'.format(baseurl,'StartGame',TOKEN)
    async with session.post(fullurl, json=data) as response:
        return await response.text()

async def postRegisterUser(session, baseurl):
    # RegisterUser API call
    fullurl = '{}/{}?code={}&name={}'.format(baseurl,'RegisterUser',TOKEN,WumpusGameEngine.Player)
    async with session.post(fullurl) as response:
        return await response.text()

async def getListUsers(session, baseurl):
    # ListUsers API call
    fullurl = '{}/{}?code={}'.format(baseurl,'ListUsers',TOKEN)
    async with session.get(fullurl) as response:
        return await response.text()

# TODO: need to add round number...
async def tryGetVoteResult(session, baseurl):
    # TryGetAgreggate API call
    fullurl = '{}/{}?code={}&roundnumber={}'.format(baseurl,'TryGetResult',TOKEN,WumpusGameEngine.moveCount) 
    async with session.get(fullurl) as response:
        return await response.text()

async def main():
    global BASEURL
    global login

    set_font("OCR A Extended")

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
        BASEURL = 'https://{}:{}/api'.format(HOST, PORT)
        await game_screen(session)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
