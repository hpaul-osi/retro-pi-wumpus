# retro-pi-wumpus
Repository for the Retro PI Challenge.

        WELCOME TO 'PI_WUMPUS'
        THE WUMPUS LIVES IN A DUNGEON UNDERNEATH THE OSISOFT(TM) 
        HEADQUARTERS IN SAN LEANDRO, CA. OF 20 ROOMS. EACH ROOM
        HAS 3 TUNNELS LEADING TO OTHER ROOMS. (LOOK AT A
        DODECAHEDRON TO SEE HOW THIS WORKS-IF YOU DON'T KNOW
        WHAT A DODECHADRON IS, ASK SOMEONE, OR USE ALTA VISTA.)
        
    HAZARDS:
        BOTTOMLESS PITS: TWO ROOMS HAVE BOTTOMLESS PITS IN THEM
        IF YOU GO THERE, YOU FALL INTO THE PIT (& LOSE!)
        SUPER BATS: TWO OTHER ROOMS HAVE SUPER BATS. IF YOU
        GO THERE, A BAT GRABS YOU AND TAKES YOU TO SOME OTHER
        ROOM AT RANDOM. (WHICH MIGHT BE TROUBLESOME)

    WUMPUS:
        THE WUMPUS, A NON-NATIVE AND INVASIVE SPECIES, HAS A 
        PENCHANT FOR REORGANIZING ETHERNET CABLES AND TENDS TO 
        CAUSE NETWORK INTERUPTION ACROSS A COMPANY, TYPICALLY SEEN 
        IN TEAMS MEETINGS THE WUMPUS IS NOT BOTHERED BY THE 
        HAZARDS (HE HAS SUCKER FEET AND IS TOO BIG FOR A BAT TO 
        LIFT). USUALLY HE IS ASLEEP. TWO THINGS THAT WAKE HIM UP: 
        YOUR ENTERING HIS ROOM OR YOUR SHOOTING AN ARROW.
        IF THE WUMPUS WAKES, HE MOVES (P=.75) ONE ROOM
        OR STAYS STILL (P=.25). AFTER THAT, IF HE IS WHERE YOU
        ARE, HE TRAMPLES YOU (& YOU LOSE!).

    YOU:
        YOUR ARE AN OSISOFT ENGINEER WHO, ALONG WITH THEIR FELLOW
        ENGINEERS, HAVE BEEN SENT INTO THE DUNGEON TO STOP THE 
        WUMPUS. EACH TURN YOU MAY MOVE OR SHOOT AN ARROW
        MOVING: YOU CAN GO ONE ROOM (THRU ONE TUNNEL)
        ARROWS: YOU HAVE 5 ARROWS. YOU LOSE WHEN YOU RUN
        OUT. YOU AIM BY TELLING
        THE COMPUTER THE ROOM YOU WANT THE ARROW TO GO TO.
        IF THE ARROW HITS THE WUMPUS, YOU WIN.

    WARNINGS:
        WHEN YOU ARE ONE ROOM AWAY FROM WUMPUS OR A HAZARD,
        THE COMPUTER SAYS:
        WUMPUS:   'I SMELL A WUMPUS'
        BAT   :   'BATS NEAR BY'
        PIT   :   'I FEEL A DRAFT'

Manufacturing steps
    If you don't have Python installed, you can install the latest version
    from the Windows Store (We tested with Python 3.8).
    Clone the repo to get the python code.
    Open up a Powershell Window and go to the directory {repo}/source/frontend
    The execute 'py PIWumpus.py' to start the gaem.
    
