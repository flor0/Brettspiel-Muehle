import pygame
import numpy as np

BACKGROUND = (190,150,90)
WHITE = (255,255,255)
BLACK = (0,0,0)

def drawPlayer(ring, stelle, color):
    conversions = {(0,0):(50,50), (0,1):(250, 50), (0,2):(450,50), (0,3):(250,450), (0,4):(450,50), (0,5):(250,450),
                   (0,6):(50, 450), (0,7):(50, 250)}
    pygame.draw.circle(screen, color, conversions[(ring,stelle)], 5)

pygame.init()
screen = pygame.display.set_mode((500, 500))
done = False

while not done:
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
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

    for i in range(7):


    pygame.display.flip()
