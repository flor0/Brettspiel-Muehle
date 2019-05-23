import pygame
import numpy as np

spielphase = 1
remaining = 9
amzug = False # iteriere weiss/schwarz

BACKGROUND = (190,150,90)
WHITE = (255,255,255)
BLACK = (0,0,0)

conversions = {(0,0):(50,50), (0,1):(250, 50), (0,2):(450,50), (0,3):(450,250), (0,4):(450,450), (0,5):(250,450), (0,6):(50, 450), (0,7):(50, 250),
                   (1,0):(100, 100), (1,1):(250,100), (1,2):(400, 100), (1,3):(400,250), (1,4):(400,400), (1,5):(250, 400), (1,6):(100,400), (1,7):(100,250),
                   (2,0):(150, 150), (2,1):(250, 150), (2,2):(350, 150), (2,3):(350, 250), (2,4):(350, 350), (2,5):(250, 350), (2,6):(150,350), (2,7):(150,250)}

def drawPlayer(ring, stelle, color):
    pygame.draw.circle(screen, color, conversions[(ring,stelle)], 15)

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

screen = pygame.display.set_mode((500, 500))
done = False
textsurface = myfont.render('Weiss', False, (0, 0, 0))

# Main game loop
while not done:
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
    #Spielbrett
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

    #1. Spielphase: Setzen
    while spielphase == 1:
        pygame.event.wait()
        if pygame.mouse.get_pressed()[0]:
            event = pygame.event.get()
            position = pygame.mouse.get_pos()
            print(position)
            for index in conversions:
                if conversions[index][0]+10>=position[0]>=conversions[index][0]-10 and conversions[index][1]+10>=position[1]>=conversions[index][1]-10:
                    print("Found position: {}".format(conversions[index]))
                    if amzug:
                        drawPlayer(index[0], index[1], WHITE)
                        textsurface = myfont.render('Weiss', False, (0, 0, 0))
                        amzug = False
                    else:
                        drawPlayer(index[0], index[1], BLACK)
                        textsurface = myfont.render('Schwarz', False, (0, 0, 0))
                        amzug = True
                screen.blit(textsurface, (0, 0))


        pygame.display.flip()

    pygame.display.flip()


