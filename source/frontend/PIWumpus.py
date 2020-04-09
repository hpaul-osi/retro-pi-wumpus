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
 
VOTEHOST = 'votepolling.azurewebsites.net'
GAMEHOST = 'gambitwumpus.azurewebsites.net'
PORT = '443'
TOKEN = 'wR3E5E8uSFvjuDs3aH5hEfqRvzzE3na3IeTvaLnfxVfsO65tvdB43w==' # API Key to send votes to Wumpus API.

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
async def list_users(session):
    print("TODO: get and print users")
    userlist = await getListUsers(session)
    print("TODO: Loop through users in {}".format(userlist))

async def lobby_screen(session, login):
    clear_screen()
    print("HELLO {}! YOU ARE NOW IN THE LOBBY. OTHER NERVOUS ENGINEERS THAT ARE AVOIDING EYE CONTACT ARE:".format(login))
    print()
    await list_users(session)
    print()
    print("PRESS THE [ENTER] (OR [RETURN]) KEY TO SIGNAL YOU ARE READY TO START.")
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

async def get_cmd(session):
    cmd = ""

    while True:
        await idle(session)

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
    global last_chat_time

    chats = []
    current_time = time.localtime
    if last_chat_time != "":
        chats = await getRecentChats(session, last_chat_time)
    last_chat_time = current_time

    for chat in chats:
        add_chat(chat)

    await getTryGetResult(session)

async def game_screen(session):
    clear_screen()
    print("Hold down CTRL and press C (and ignore the call stack) to quit ...")
    print()

    WumpusGameEngine.displayRoomInfo()
    while True:
        cmd = await get_cmd(session)
        print()
        
        await convert_cmd_to_request(cmd, session)

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
                await postInsertVote(session, {"WumpusAction" : "Move", "Room" : split_command[1], "MoveNumber" : WumpusGameEngine.moveCount, "UserName" : login})
            elif (split_command[0] == "SHOOT" or split_command[0] == "S"):
                print("Sending Server Vote for SHOOT")
                await postInsertVote(session, {"WumpusAction" : "Shoot", "Room" : split_command[1], "MoveNumber" : WumpusGameEngine.moveCount, "UserName" : login})
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
        print_part(" **WHAT??")
    else:
        erase_line(INPUT_LINE + 1)  

async def postInsertVote(session, data):
    # InsertVote API call
    fullurl = 'https://{}:{}/api/{}?code={}'.format(VOTEHOST,PORT,'InsertVote',TOKEN)
    async with session.post(fullurl, json=data) as response:
        return await response.text()

async def postStartGame(session):
    # StartGame API call
    fullurl = 'https://{}:{}/api/{}/'.format(GAMEHOST,PORT,'StartGame')
    async with session.post(fullurl) as response:
        return await response.text()

async def postStopGame(session):
    # StartGame API call
    fullurl = 'https://{}:{}/api/{}/'.format(GAMEHOST,PORT,'StopGame')
    async with session.post(fullurl) as response:
        return await response.text()

async def postRegisterUser(session):
    # RegisterUser API call
    fullurl = 'https://{}:{}/api/{}/?name={}'.format(GAMEHOST,PORT,'RegisterUser',login)
    async with session.post(fullurl) as response:
        return await response.text()

async def getListUsers(session):
    # ListUsers API call
    fullurl = 'https://{}:{}/api/{}'.format(GAMEHOST,PORT,'ListUsers')
    async with session.get(fullurl) as response:
        return await response.text()

# TODO: need to add round number...
async def getTryGetResult(session):
    # TryGetAgreggate API call
    fullurl = 'https://{}:{}/api/{}?noteroundnumber={}'.format(GAMEHOST,PORT,'TryGetResult',WumpusGameEngine.moveCount) 
    async with session.get(fullurl) as response:
        return await response.text()

# TODO: everything
async def getRecentChats(session, last_chat_time):
    return [ "Jeremy, does this annoy you?"]

async def main():
    global login

    set_font("OCR A Extended")

    enable_ansi()
    WumpusGameEngine.init()

    clear_screen()
    print("WELCOME TO PI WUMPUS!")
    print()
    print("PLEASE ENTER YOUR NAME, HANDLE, OR OTHER IDENTIFIER:")

    async with aiohttp.ClientSession() as session:
        global last_chat_time

        login = input()
        await lobby_screen(session, login)

        clear_screen()
        WumpusGameEngine.banner()

        last_chat_time = ""
        await game_screen(session)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())