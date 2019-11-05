import pygame
import numpy as np
import sys
import copy
import datahandler
import neural_ai
import math


# Variables for the game
spielphase = 1
phase1_remaining = 18
remaining = {1: 9, 2: 9}  # White, Black
turn = False  # iterate white/black; white begins
spielfeld = [[0 for i in range(8)] for j in range(3)]  # Occupation: 0=Unoccupied, 1=White, 2=Black
spielfeld_muhlen = [[0 for i1 in range(8)] for j1 in range(3)]  # Mills on board are marked with 1's ij this projection

# Variables for the GUI
BACKGROUND = (190,150,90)
WHITE = (255,255,255)
BLACK = (0,0,0)
conversions = {(0,0):(50,50), (0,1):(250, 50), (0,2):(450,50), (0,3):(450,250), (0,4):(450,450), (0,5):(250,450), (0,6):(50, 450), (0,7):(50, 250),
                   (1,0):(100, 100), (1,1):(250,100), (1,2):(400, 100), (1,3):(400,250), (1,4):(400,400), (1,5):(250, 400), (1,6):(100,400), (1,7):(100,250),
                   (2,0):(150, 150), (2,1):(250, 150), (2,2):(350, 150), (2,3):(350, 250), (2,4):(350, 350), (2,5):(250, 350), (2,6):(150,350), (2,7):(150,250)}


# Functions for the game
def checkmuhle(ringPos, stellePos):
    mancolor = 1 if turn else 2
    if stellePos%2 == 0:  # Men on the edge
        if spielfeld[ringPos][(stellePos+1)%8] == mancolor and spielfeld[ringPos][(stellePos+2)%8] == mancolor:
            spielfeld_muhlen[ringPos][(stellePos + 1) % 8] = 1  # Set mill in projection
            spielfeld_muhlen[ringPos][(stellePos + 2) % 8] = 1
            spielfeld_muhlen[ringPos][stellePos] = 1
            return True
        if spielfeld[ringPos][(stellePos-1)%8] == mancolor and spielfeld[ringPos][(stellePos-2)%8] == mancolor:
            spielfeld_muhlen[ringPos][(stellePos - 1) % 8] = 1  # Set mill in projection
            spielfeld_muhlen[ringPos][(stellePos - 2) % 8] = 1
            spielfeld_muhlen[ringPos][stellePos] = 1
            return True
    else:  # Men in the centre lines
        if spielfeld[(ringPos+1)%3][stellePos] == mancolor and spielfeld[(ringPos+2)%3][stellePos] == mancolor:
            spielfeld_muhlen[(ringPos + 1) % 3][stellePos] = 1  # Set mill in projection
            spielfeld_muhlen[(ringPos + 2) % 3][stellePos] = 1
            spielfeld_muhlen[ringPos][stellePos] = 1
            return True
        if spielfeld[ringPos][(stellePos + 1) % 8] == mancolor and spielfeld[ringPos][(stellePos - 1) % 8] == mancolor:
            spielfeld_muhlen[ringPos][(stellePos + 1) % 8] = 1
            spielfeld_muhlen[ringPos][(stellePos - 1) % 8] = 1
            spielfeld_muhlen[ringPos][stellePos] = 1
            return True
    return False

def clearmuhlen():
    for ring in range(3):
        for stelle in range(8):
            if (not checkmuhle(ring, stelle)) and (spielfeld_muhlen[ring][stelle] != 0):
                spielfeld_muhlen[ring][stelle] = 0
    print("BRETT MUHLEN")
    print(spielfeld_muhlen)

def removeman(ringpos, stellepos):
    myteam = 1 if turn else 2
    if spielfeld[ringpos][stellepos] == myteam or spielfeld[ringpos][stellepos] == 0 or spielfeld_muhlen[ringpos]\
            [stellepos] == 1:
        if not hasnotonlymills(1 if myteam == 2 else 2):
            spielfeld[ringpos][stellepos] = 0
            remaining[myteam] -= 1
            return True
        return False
    else:
        spielfeld[ringpos][stellepos] = 0
        remaining[myteam] -= 1
        return True


def canmove(ringpos, stellepos):
    if stellepos % 2 == 0:  # Men on the edges
        if spielfeld[ringpos][(stellepos+1) % 8] == 0 or spielfeld[ringpos][(stellepos-1) % 8] == 0:  # Sideways
            return True
    else:  # Men on the center fields
        if spielfeld[ringpos][(stellepos+1) % 8] == 0 or spielfeld[ringpos][(stellepos-1) % 8] == 0:  # Sideways
            return True
        if ringpos == 0:  # Outer ring
            if spielfeld[1][stellepos] == 0:
                return True
        if ringpos == 1:  # Center ring
            if spielfeld[0][stellepos] == 0 or spielfeld[2][stellepos] == 0:
                return True
        if ringpos == 2:  # Inner ring
            if spielfeld[1][stellepos] == 0:
                return True
    return False


def canjump():
    for reihe in spielfeld:
        for stelle in reihe:
            if stelle == 0:
                return True
    return False


def checkremaining(player):
    if remaining[player] < 3:
        return True
    return False


def canmoveatall(player):
    for ring in range(len(spielfeld)):
        for stelle in range(len(spielfeld[ring])):
            if spielfeld[ring][stelle] == player:
                if canmove(ring, stelle):
                    return True
    return False

def hasnotonlymills(player):
    for i in range(len(spielfeld_muhlen)):
        for j in range(len(spielfeld_muhlen[i])):
            if spielfeld_muhlen[i][j] == 0:
                if spielfeld[i][j] == player:
                    return True
    return False


def isneighbor(select_ring, select_stelle, origin_ring, origin_stelle):
    if ((origin_stelle + 1) % 8 == select_stelle or (origin_stelle - 1) % 8 == select_stelle) and origin_ring == select_ring:
        print("1isneighbor true")
        return True  # Left/Right
    if origin_stelle % 2 != 0:  # Center positions
        if ((origin_stelle + 1) % 8 == select_stelle or (origin_stelle - 1) % 8 == select_stelle) and origin_ring == select_ring:
            print("2isneightbor true")
            return True
        if origin_ring == 0:
            if select_ring == origin_ring + 1 and select_stelle == origin_stelle:
                print("3isneighbor true")
                return True
        if origin_ring == 1:
            if origin_ring + 1 == select_ring or origin_ring - 1 == select_ring and select_stelle == origin_stelle:
                print("4isneighbor true")
                return True
        if origin_ring == 2:
            if origin_ring - 1 == select_ring and select_stelle == origin_stelle:
                print("5isneighbor true")
                return True
    print("isneighbor false")
    return False


# Functions for the GUI
def drawPlayer(ring, stelle, color):
    pygame.draw.circle(screen, color, conversions[(ring,stelle)], 15)


def drawState():
    converter = {1: WHITE, 2: BLACK}
    for ring in range(len(spielfeld)):
        for stelle in range(len(spielfeld[ring])):
            if spielfeld[ring][stelle] != 0:
                drawPlayer(ring, stelle, converter[spielfeld[ring][stelle]])


def drawBoard():
    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, BLACK, pygame.Rect(50, 50, 400, 400))
    pygame.draw.rect(screen, BACKGROUND, pygame.Rect(52, 52, 396, 396))

    pygame.draw.rect(screen, BLACK, pygame.Rect(100, 100, 300, 300))
    pygame.draw.rect(screen, BACKGROUND, pygame.Rect(102, 102, 296, 296))

    pygame.draw.rect(screen, BLACK, pygame.Rect(150, 150, 200, 200))
    pygame.draw.rect(screen, BACKGROUND, pygame.Rect(152, 152, 196, 196))

    pygame.draw.line(screen, BLACK, (50, 250), (150, 250))
    pygame.draw.line(screen, BLACK, (350, 250), (448, 250))
    pygame.draw.line(screen, BLACK, (250, 50), (250, 150))
    pygame.draw.line(screen, BLACK, (250, 448), (250, 350))



def drawwinner(winner_player):
    winner_textsurface = myfont.render("{} gewinnt!".format("Weiss" if winner_player == 1 else "Schwarz"), False, (255,215,0))
    screen.blit(winner_textsurface, (150, 0))
    pygame.display.flip()


def endgameloop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                sys.exit(0)

def drawremove():
    textscreen = myfont.render("Entferne einen Stein", False, (51, 25, 0))
    screen.blit(textscreen, (0, 500-40))
    pygame.display.flip()


# ----------------------------------------------------------------------------------------------------------------------



pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Cambria', 30)

screen = pygame.display.set_mode((500, 500))
done = False
textsurface = myfont.render('Schwarz', False, (0, 0, 0))

# Main game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             done = True
    # Draw board
    drawBoard()
    pygame.display.flip()

    # 1. Game phase: Place men
    while phase1_remaining and not done:
        if not turn:
            clearmuhlen()
            board_ai = 0
            board_human = 0
            for i in range(3):
                for j in range(8):
                    if spielfeld[i][j] == 1:
                        board_human += 1
                    elif spielfeld[i][j] == 2:
                        board_ai += 1
            print("CALLING AI...")
            ai_move = neural_ai.makemove(spielfeld, math.ceil(phase1_remaining/2), phase1_remaining//2, board_human, board_ai)
            print("Generated move: {}".format(ai_move))
            if not type(ai_move) == tuple:
                print("Uh, oh. It's retarded!")
                ai_move = ai_move[0]
            if spielfeld[ai_move[0]][ai_move[1]] == 0:
                spielfeld[ai_move[0]][ai_move[1]] = 2
            else:   # Uh, oh. The AI has made a terrible mistake!
                print("Uh, oh. It's made a mistake!")

            turn = not turn
            phase1_remaining -= 1
            drawBoard()
            drawState()
            pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user presses esc
                print("Thanks for playing!")
                done = True
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:  # If a position has been clicked
                clearmuhlen()
                position = pygame.mouse.get_pos()
                for index in conversions:
                    if conversions[index][0]+10 >= position[0] >= conversions[index][0]-10 and conversions[index][1]+10\
                            >= position[1] >= conversions[index][1]-10:  # Get the selected position to place the man
                        # Check if the move is valid
                        if spielfeld[index[0]][index[1]] != 0:
                            print("Invalid Move! Men can't be place on top of others.")
                            break

                        elif turn:  # Whites turn
                            spielfeld[index[0]][index[1]] = 1
                            textsurface = myfont.render('Schwarz', False, (0, 0, 0))

                        else:  # Blacks turn
                            spielfeld[index[0]][index[1]] = 2
                            textsurface = myfont.render('Weiss', False, (255, 255, 255))

                        # Show the fresh man
                        drawBoard()
                        drawState()
                        pygame.display.flip()

                        # Check if a Mill has been created and remove a man
                        if checkmuhle(index[0], index[1]):
                            print("Mühle! Wähle einen Stein zum entfernen aus:")
                            drawremove()
                            temp_done = False
                            while not temp_done:  # Wait for user input
                                for event1 in pygame.event.get():
                                    if event1.type == pygame.QUIT:
                                        sys.exit(0)
                                    if event1.type == pygame.MOUSEBUTTONDOWN:
                                        temp_position = pygame.mouse.get_pos()  # Clicked position
                                        for index1 in conversions:
                                            if conversions[index1][0] + 20 >= temp_position[0] >= conversions[index1][0] - 20\
                                                    and conversions[index1][1] + 20 >= temp_position[1] >= conversions[index1]\
                                                    [1] - 20:  # Get the selected position to remove a man
                                                if removeman(index1[0], index1[1]):  # Try to remove the selected man
                                                    temp_done = True
                                                    break
                                                else:
                                                    print("Dieser Stein kann von dir nicht entfernt werden")
                                                    print(spielfeld_muhlen)

                        clearmuhlen()  # Remove mills that have been destroyed this turn
                        turn = not turn  # Switch turn
                        print(remaining)
                        # Standard rendering done every round
                        drawBoard()
                        drawState()
                        phase1_remaining -= 1  # One less man can be placed
                        break
        # Standard rendering done in while loop
        screen.blit(textsurface, (0, 0))
        pygame.display.flip()


    # Once the first phase is over, switch to the next
    spielphase = 2
    print("Keine Steine zum setzen übrig.")

    # Making sure the right turn gets displayed
    if not turn:
        textsurface = myfont.render('Weiss', False, (255, 255, 255))
    else:
        textsurface = myfont.render('Schwarz', False, (0, 0, 0))

    screen.blit(textsurface, (0, 0))
    pygame.display.flip()

# ----------------------------------------------------------------------------------------------------------------------

    # Second phase: moving men around the board
    while remaining[1] > 0 and remaining[2] > 0 and spielphase == 2 and not done:  # While loop phase 2
        if not turn:
            clearmuhlen()
            board_ai = 0
            board_human = 0
            for i in range(3):
                for j in range(8):
                    if spielfeld[i][j] == 1:
                        board_human += 1
                    elif spielfeld[i][j] == 2:
                        board_ai += 1
            print("CALLING AI...")
            ai_move = neural_ai.makemove(spielfeld, math.ceil(phase1_remaining / 2), phase1_remaining // 2, board_human,
                                         board_ai)
            print("Generated move: {}".format(ai_move))
            if len(ai_move) < 2:
                print("Uh, oh. It's retarded!")
            else:
                spielfeld[ai_move[0][0]][ai_move[0][1]] = 0
                spielfeld[ai_move[1][0]][ai_move[1][1]] = 2
            turn = not turn
            drawBoard()
            drawState()
            pygame.display.flip()
        myteam = 1 if turn else 2
        textsurface = myfont.render('Schwarz', False, (0, 0, 0)) if myteam == 2 else myfont.render("Weiss", False,
                                                                                                   (255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If the user presses esc
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:  # If the user presses a mouse button
                clearmuhlen()
                position = pygame.mouse.get_pos()  # Get position of the mouse click
                for index1 in conversions:
                    if conversions[index1][0] + 10 >= position[0] >= conversions[index1][0] - 10 \
                            and conversions[index1][1] + 10 >= position[1] >= conversions[index1] \
                            [1] - 10:  # Get the selected man/index

                        if spielfeld[index1[0]][index1[1]] == myteam:  # Man has to be yours
                            if remaining[2 if myteam == 1 else 1] > 3:  # When the player has more than 3 men left -> moving, not jumping
                                if canmove(index1[0], index1[1]):  # Man has to be movable
                                    # Select destination location
                                    temp_done = False
                                    while not temp_done:
                                        for event1 in pygame.event.get():
                                            if event1.type == pygame.MOUSEBUTTONDOWN:
                                                temp_pos = pygame.mouse.get_pos()
                                                for index in conversions:
                                                    if conversions[index][0] + 10 >= temp_pos[0] >= conversions[index][0] - 10 and \
                                                            conversions[index][1] + 10 >= temp_pos[1] >= conversions[index][1] - 10:  # Get the selected position to move the man to
                                                        if spielfeld[index[0]][index[1]] == 0 and isneighbor(index[0], index[1], index1[0], index1[1]):
                                                            #  Execute move
                                                            spielfeld[index[0]][index[1]] = myteam
                                                            spielfeld[index1[0]][index1[1]] = 0
                                                            temp_done = True
                                                            print(spielfeld_muhlen)
                                                            if checkmuhle(index[0], index[1]):
                                                                print("Mühle! Wähle einen Stein zum entfernen aus:")
                                                                temp_done = False
                                                                drawBoard()
                                                                drawState()
                                                                pygame.display.flip()
                                                                while not temp_done:
                                                                    for event1 in pygame.event.get():
                                                                        if event1.type == pygame.MOUSEBUTTONDOWN:
                                                                            temp_position = pygame.mouse.get_pos()
                                                                            for index1 in conversions:
                                                                                if conversions[index1][0] + 20 >= temp_position[0] >= conversions[index1][0] - 20\
                                                                                        and conversions[index1][1] + 20 >= temp_position[1] >= conversions[index1]\
                                                                                        [1] - 20:  # Get the selected position to remove a man
                                                                                    if removeman(index1[0], index1[1]):  # Try to remove the selected man
                                                                                        temp_done = True
                                                                                        # No need to check for remaining men
                                                                                        break
                                                                                    else:
                                                                                        print("Dieser Stein kann von dir nicht entfernt werden")
                                                                                        print(spielfeld_muhlen)
                                                            if not canmoveatall(1 if myteam == 2 else 2):
                                                                print("{} kann keine Züge mehr machen, {} gewinnt!".format("Weiss" if myteam == 2 else "Schwarz", "Schwarz" if myteam == 2 else "Weiss"))
                                                                drawwinner(myteam)
                                                                endgameloop()
                                                                done = True
                                                        else:
                                                            print("Hierhin kannst du deinen Stein nicht bewegen.")
                                    clearmuhlen()
                                    turn = not turn  # Switch turn
                                    pygame.display.flip()
                            else:  # Jumping, not moving
                                print("Enabled jumping mode, things could break!")
                                # Select destination location
                                temp_done = False
                                while not temp_done:
                                    for event1 in pygame.event.get():
                                        if event1.type == pygame.MOUSEBUTTONDOWN:
                                            temp_pos = pygame.mouse.get_pos()
                                            for index in conversions:
                                                if conversions[index][0] + 10 >= temp_pos[0] >= conversions[index][
                                                    0] - 10 and \
                                                        conversions[index][1] + 10 >= temp_pos[1] >= conversions[index][
                                                    1] - 10:  # Get the selected position to move the man to
                                                    if spielfeld[index[0]][index[1]] == 0:
                                                        #  Execute move
                                                        spielfeld[index[0]][index[1]] = myteam
                                                        spielfeld[index1[0]][index1[1]] = 0
                                                        temp_done = True
                                                        print(spielfeld_muhlen)
                                                        if checkmuhle(index[0], index[1]):
                                                            print("Mühle! Wähle einen Stein zum entfernen aus:")
                                                            temp_done = False
                                                            drawBoard()
                                                            drawState()
                                                            pygame.display.flip()
                                                            while not temp_done:
                                                                for event1 in pygame.event.get():
                                                                    if event1.type == pygame.MOUSEBUTTONDOWN:
                                                                        temp_position = pygame.mouse.get_pos()
                                                                        for index1 in conversions:
                                                                            if conversions[index1][0] + 10 >= \
                                                                                    temp_position[0] >= \
                                                                                    conversions[index1][0] - 10 \
                                                                                    and conversions[index1][1] + 10 >= \
                                                                                    temp_position[1] >= \
                                                                                    conversions[index1][1] - 10:  # Get the selected position to remove a man
                                                                                if removeman(index1[0], index1[1]):  # Try to remove the selected man
                                                                                    temp_done = True
                                                                                    # TODO: Check if game is over, insert checkremaining
                                                                                    if checkremaining(1 if myteam == 2 else 2):
                                                                                        print("{} gewinnt weil {} keine Steine hat!".format("Weiss" if myteam == 1 else "Schwarz", "Schwarz" if myteam == 2 else "Weiss"))
                                                                                        drawwinner(myteam)
                                                                                        endgameloop()
                                                                                else:
                                                                                    print("Dieser Stein kann von dir nicht entfernt werden")
                                                                                    print(spielfeld_muhlen)
                                                        # TODO: Check if this works
                                                        if not canmoveatall(1 if myteam == 2 else 2):
                                                            print("{} kann keine Züge mehr machen, {} gewinnt!".format(
                                                                "Weiss" if myteam == 2 else "Schwarz",
                                                                "Schwarz" if myteam == 2 else "Weiss"))
                                                            done = True
                                                            drawwinner(myteam)
                                                            endgameloop()
                                                    else:
                                                        print("Hierhin kannst du deinen Stein nicht bewegen.")
                                turn = not turn

                        else:
                            print("Waehle einen deiner Steine aus.")
        #  Standard rendering done every round
        drawBoard()
        drawState()
        screen.blit(textsurface, (0,0))
        pygame.display.flip()

    if remaining[1] == 0:
        print("Schwarz gewinnt!")
    elif remaining[2] == 0:
        print("Weiss gewinnt!")
    #  Not yet implemented
    drawBoard()
    drawState()
    pygame.display.flip()
