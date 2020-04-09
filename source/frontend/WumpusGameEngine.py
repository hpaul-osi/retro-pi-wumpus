#Hunt the Wumpus
#From a vintage BASIC game program
#by CREATIVE COMPUTING MORRISTOWN, NEW JERSEY
#Rewritten in Python by Gordon Reeder
# Python 3.4
# ** To do **
# - Make connections within cave random. So that no two caves are the same.

import random
import sys
import threading
import time
import datetime
import signal

# globals
Cave = []
moveCount = 1
GameOver = False

def show_instructions():
    print ("""
        WELCOME TO 'PI_WUMPUS'
        THE WUMPUS LIVES IN A DUNGEON UNDERNEATH THE OSISOFT(TM) 
        HEADQUARTERS IN SAN LEANDRO, CA.OF 20 ROOMS. EACH ROOM
        HAS 3 TUNNELS LEADING TO OTHER ROOMS. (LOOK AT A
        DODECAHEDRON TO SEE HOW THIS WORKS-IF YOU DON'T KNOW
        WHAT A DODECHADRON IS, ASK SOMEONE, OR USE ALTA VISTA.)
        """)
    temp = input('PRESS [ENTER] TO CONTINUE...')

    print ("""    
    HAZARDS:
        BOTTOMLESS PITS: TWO ROOMS HAVE BOTTOMLESS PITS IN THEM
        IF YOU GO THERE, YOU FALL INTO THE PIT (& LOSE!)
        SUPER BATS: TWO OTHER ROOMS HAVE SUPER BATS. IF YOU
        GO THERE, A BAT GRABS YOU AND TAKES YOU TO SOME OTHER
        ROOM AT RANDOM. (WHICH MIGHT BE TROUBLESOME)

        """)
    temp = input("PRESS [ENTER] TO CONTINUE...")

    print("""
    WUMPUS:
        THE WUMPUS, A NON-NATIVE AND INVASIVE SPECIES, HAS A 
        HABIT FOR REORGANIZING ETHERNET CABLES THAT CAUSE 
        NETWORK INTERUPTION ACROSS A COMPANY. THE WUMPUS IS NOT 
        BOTHERED BY THE HAZARDS (HE HAS SUCKER FEET AND IS TOO 
        BIG FOR A BAT TO LIFT). USUALLY HE IS ASLEEP. TWO THINGS 
        THAT WAKE HIM UP: YOUR ENTERING HIS ROOM OR YOUR SHOOTING 
        AN ARROW. IF THE WUMPUS WAKES, HE MOVES (P=.75) ONE ROOM
        OR STAYS STILL (P=.25). AFTER THAT, IF HE IS WHERE YOU
        ARE, HE TRAMPLES YOU (& YOU LOSE!).
        """)
    temp = input("PRESS [ENTER] TO CONTINUE...")

    print ("""
    YOU:
        YOUR ARE AN OSISOFT ENGINEER WHO, ALONG WITH THEIR FELLOW
        ENGINEERS, HAVE BEEN SENT INTO THE DUNGEON TO STOP THE 
        WUMPUS. EACH TURN YOU MAY MOVE OR SHOOT AN ARROW
        MOVING: YOU CAN GO ONE ROOM (THRU ONE TUNNEL)
        ARROWS: YOU HAVE 5 ARROWS. YOU LOSE WHEN YOU RUN
        OUT. YOU AIM BY TELLING
        THE COMPUTER THE ROOM YOU WANT THE ARROW TO GO TO.
        IF THE ARROW HITS THE WUMPUS, YOU WIN.

        """)
    temp = input("PRESS [ENTER] TO CONTINUE...")
    
    print ("""
    WARNINGS:
        WHEN YOU ARE ONE ROOM AWAY FROM WUMPUS OR A HAZARD,
        THE COMPUTER SAYS:
        WUMPUS:   'I SMELL A WUMPUS'
        BAT   :   'BATS NEAR BY'
        PIT   :   'I FEEL A DRAFT'
        
        """)
    temp = input("PRESS [ENTER] TO CONTINUE...")

class Room:
    """Defines a room. 
    A room has a name (or number),
    a list of other rooms that it connects to.
    and a description. 
    How these rooms are built into something larger 
    (cave, dungeon, skyscraper) is up to you.
    """

    def __init__(self, **kwargs):
        self.number = 0
        self.name =''
        self.connects_to = [] #These are NOT objects
        self.description = ""

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return str(self.number)

    def remove_connect(self, arg_connect):
        if arg_connect in self.connects_to:
            self.connects_to.remove(arg_connect)

    def add_connect(self, arg_connect):
        if arg_connect not in self.connects_to:
            self.connects_to.append(arg_connect)

    def is_valid_connect(self, arg_connect):
        return arg_connect in self.connects_to

    def get_number_of_connects(self):
        return len(self.connects_to)

    def get_connects(self):
        return self.connects_to

    def describe(self):
        if len(self.description) > 0:
            print(self.description)
        else:
            print("YOU ARE IN ROOM {}.\nPASSAGES LEAD TO {}".format(self.number, self.connects_to))
        

class Thing:
    """Defines the things that are in the cave.
    That is the Wumpus, Player, pits and bats.
    """

    def __init__(self, **kwargs):
        self.location = 0 # this is a room object
        
        for key, value in kwargs.items():
            setattr(self, key, value)

    def move(self, a_new_location):
        if a_new_location.number in self.location.connects_to or a_new_location == self.location:
            self.location = a_new_location
            return True
        else:
            return False

    def validate_move(self, a_new_location):
        return a_new_location.number in self.location.connects_to or a_new_location == self.location
                
    def get_location(self):
        return self.location.number

    def wakeup(self, a_cave):
        if random.randint(0, 3): # P=.75 that we will move.
            self.location = a_cave[random.choice(self.location.connects_to) -1]
 
    def is_hit(self, a_room):
        return self.location == a_room

def create_things(a_cave):

    Things = []
    Samples = random.sample(a_cave, 6)
    for room in Samples:
        Things.append(Thing(location = room))

    return Things


def create_cave():
    global Cave

    # First create a list of all the rooms.
    for number in range(20):
        Cave.append(Room(number = number +1))

    # Then stich them together.
    for idx, room in enumerate(Cave):

        #connect to room to the right
        if idx == 9:
            room.add_connect(Cave[0].number)
        elif idx == 19:
            room.add_connect(Cave[10].number)
        else:    
            room.add_connect(Cave[idx +1].number)

        #connect to the room to the left
        if idx == 0:
            room.add_connect(Cave[9].number)
        elif idx == 10:
            room.add_connect(Cave[19].number)
        else:
            room.add_connect(Cave[idx -1].number)

        #connect to the room in the other ring
        if idx < 10:
            room.add_connect(Cave[idx +10].number) #I connect to it.
            Cave[idx +10].add_connect(room.number) #It connects to me.

def executeMove(raw_command):
    moveCount = moveCount + 1

    command_list = raw_command.split(' ')
    command = command_list[0].upper()
    if len(command_list) > 1:
        try:
            move = Cave[int(command_list[1]) -1]
        except:
            print("\n **WHAT??")
            return
    else:
        move = Player.location

    if command == 'HELP' or command == 'H':
        show_instructions()
        return

    elif command == 'QUIT' or command == 'Q':
        print("\nOK, BYE.")
        GameOver = True

    elif command == 'MOVE' or command == 'M':
        if Player.move(move):
            if Player.location == Wumpus.location:
                print("... OOPS! BUMPED A WUMPUS!")
                Wumpus.wakeup(Cave)
        else:
            print("\n **YOU CAN'T GET THERE FROM HERE.")
            return

    elif command == 'SHOOT' or command == 'S':
        if Player.validate_move(move):
            print("\n-TWANG-") 
            if Wumpus.location == move:
                print("\n GOOD SHOOTING!! YOU HIT THE WUMPUS. \n THE WUMPI WILL HAVE THEIR REVENGE.\n")
                print ("PRESS [ENTER] TO EXIT.\n")
                input()
                GameOver = True    
        else:
            print("\n** STOP TRYING TO SHOOT THROUGH WALLS.")

        Wumpus.wakeup(Cave)
        Arrows -= 1
        if Arrows == 0:
            print("\n YOU ARE OUT OF ARROWS\n BETTER LUCK NEXT TIME\n")
            print ("PRESS [ENTER] KEY TO EXIT\n")
            input()
            GameOver = True  
    
    else:
        print("\n **WHAT?")
        return

    # By now the player has moved. See what happened.
    # Handle problems with pits, bats and wumpus.
 
    if Player.location == Bats1.location or Player.location == Bats2.location:
        print("ZAP--SUPER BAT SNATCH! ELSEWHEREVILLE FOR YOU!")
        Player.location = random.choice(Cave)

    if Player.location == Wumpus.location:
        print("TROMP TROMP - WUMPUS GOT YOU!\n")
        print ("PRESS [ENTER] KEY TO EXIT\n")
        input()
        GameOver = True

    elif Player.location == Pit1.location or Player.location == Pit2.location:
        print("YYYIIIIEEEE . . . FELL INTO A PIT!\n PHILADELPHIA HERE WE COME!\n")
        print ("PRESS [ENTER] KEY TO EXIT\n")
        input()
        GameOver = True    

    else: # Keep playing
        pass   

def displayRoomInfo():
    global Player

    Player.location.describe()
    #Check each <Player.location.connects_to> for hazards.
    for room in Player.location.connects_to:
        if Wumpus.location.number == room:
            print("I SMELL A WUMPUS!")
        if Pit1.location.number == room or Pit2.location.number == room:
            print("I FEEL A DRAFT!")
        if Bats1.location.number == room or Bats2.location.number == room:
            print("BATS NEARBY!")

def init():
    global Arrows
    global Wumpus
    global Player
    global Pit1
    global Pit2
    global Bats1
    global Bats2

    #seed so that everyone has same random map
    random.seed(1000)

    create_cave()

    # Make player, wumpus, bats, pits and put into cave.

    Wumpus, Player, Pit1, Pit2, Bats1, Bats2 = create_things(Cave)

    Arrows = 5

def banner():
    print("""\n   WELCOME TO THE CAVE, GREAT WHITE HUNTER.
    YOU ARE HUNTING THE WUMPUS.
    ON ANY TURN YOU CAN MOVE OR SHOOT.
    COMMANDS ARE ENTERED IN THE FORM OF ACTION LOCATION
    IE: 'SHOOT 12' OR 'MOVE 8'
    TYPE 'HELP' FOR INSTRUCTIONS.
    'QUIT' TO END THE GAME.
    """)
