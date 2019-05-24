import pygame
import numpy as np

# Variables for the game
spielphase = 1
phase1_remaining = 18
remaining_white = 9
remaining_black = 9
turn = False # iterate white/black
spielfeld = [[0 for i in range(8)] for j in range(3)]  # Besetzung: 0=Unbesetzt, 1=Weiss, 2=Schwarz

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
    print("checking: {}".format(mancolor))
    if stellePos%2 == 0:  # Men on the edge
        if spielfeld[ringPos][(stellePos+1)%8] == mancolor and spielfeld[ringPos][(stellePos+2)%8] == mancolor:
            return True
        if spielfeld[ringPos][(stellePos-1)%8] == mancolor and spielfeld[ringPos][(stellePos-2)%8] == mancolor:
            return True
    else:  # Men in the centre lines
        if spielfeld[(ringPos+1)%3][stellePos] == mancolor and spielfeld[(ringPos+2)%3][stellePos] == mancolor:
            return True
    return False

def removeman(ringpos, stellepos):
    myteam = 1 if turn else 2
    if spielfeld[ringpos][stellepos] == myteam or spielfeld[ringpos][stellepos] == 0:
        return False
    else:
        spielfeld[ringpos][stellepos] = 0
        return True


# Functions for the GUI
def drawPlayer(ring, stelle, color):
    pygame.draw.circle(screen, color, conversions[(ring,stelle)], 15)


def drawState():
    converter = {1:WHITE, 2:BLACK}
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


pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If the user exits
                print("Thanks for playing!")
                done = True
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:  # If a position has been clicked
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

                        if checkmuhle(index[0], index[1]):  # Check if a Mill has been created and remove a man
                            print("Mühle! Wähle einen Stein zum entfernen aus:")
                            temp_done = False
                            while not temp_done:
                                for event1 in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        temp_position = pygame.mouse.get_pos()
                                        for index1 in conversions:
                                            if conversions[index1][0] + 10 >= temp_position[0] >= conversions[index1][0] - 10\
                                                    and conversions[index1][1] + 10 >= temp_position[1] >= conversions[index]\
                                                    [1] - 10:  # Get the selected position to remove a man
                                                if removeman(index1[0], index1[1]):
                                                    temp_done = True
                                                    print("REMOVED")
                                                    break
                                drawBoard()
                                drawState()


                        turn = not turn

                        # Standard rendering done every round
                        drawBoard()
                        drawState()

                        phase1_remaining -= 1  # One less man can be placed
                        break

        screen.blit(textsurface, (0, 0))
        pygame.display.flip()

    # Not yet implemented
    drawBoard()
    drawState()
    pygame.display.flip()


