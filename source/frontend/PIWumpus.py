import kbhit
import os
import sys
import time
import WumpusGameEngine

ESC = chr(27)
CR = chr(13)
REFRESH_INTERVAL = 1

# Utils
def enable_ansi():
    if sys.platform[0 : 3] == "win":
        os.system('')

def clear_screen():
    print(ESC + "[2J")

def print_part(s):
    print(s, end="", flush=True)

def input_async(timeout, echo=True):
    kb = kbhit.KBHit()

    ret = ""
    elapsed = 0
    while True:
        if kb.kbhit():
            c = kb.getch()
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
    print("Hello {}! You are now in the lobby. Other people here are:".format(login))
    print()
    list_users()
    print()
    print("Press the ENTER (or RETURN) key to start with the current players")
    while True:
        input = input_async(REFRESH_INTERVAL, echo=False)
        if len(input) > 0 and input[-1]==CR:
            break

def get_cmd():
    print_part("> ")

    while True:
        input = input_async(REFRESH_INTERVAL)
        if len(input) > 0 and input[-1]==CR:
            break
        print("TODO: Print other users commands")
    return input

def game_screen():
    print("Hold down CTRL and press C to quit ...")

    WumpusGameEngine.displayRoomInfo()
    while True:
        cmd = get_cmd()
        print()
        print("TODO: Send to server")

def main():
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
    WumpusGameEngine.start_game()
    game_screen()

if __name__ == "__main__":
    main()

