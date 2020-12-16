import pygame
import os
import random
import sys
from math import ceil, sqrt, pi, cos, sin
path = os.getcwd()
sys.path.append(path.removesuffix("Jeu exemple") + '/Hexagons')
from Hex import *
pygame.init()


class player(object):
    def __init__(self, playerX, playerY, width, heigth):
        self.playerX = playerX
        self.playerY = playerY
        self.width = width
        self.heigth = heigth
        self.change = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.CenterX = self.width // 2
        self.CenterY = self.heigth // 2 + 8

    def draw(self, screen):
        relativeX = self.playerX - 32
        relativeY = self.playerY - 40
        if self.walkCount + 1 >= 30:
            self.walkCount = 0
        if man.left:
            screen.blit(walkLeft[(self.walkCount // 3) % 9],
                        (relativeX, relativeY))
            self.walkCount += 1
        elif self.right:
            screen.blit(walkRight[(self.walkCount // 3) % 9],
                        (relativeX, relativeY))
            self.walkCount += 1
        else:
            screen.blit(char, (relativeX, relativeY))


WIDTH, HEIGTH = 1097, 720

RED = (255, 0, 0)
main_font = pygame.font.SysFont("Blue Eyes.otf", 30)
screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("Sprite and Animation")

#IMAGE
walkRight = [
    pygame.image.load('assets/img_sprite/R1.png'),
    pygame.image.load('assets/img_sprite/R2.png'),
    pygame.image.load('assets/img_sprite/R3.png'),
    pygame.image.load('assets/img_sprite/R4.png'),
    pygame.image.load('assets/img_sprite/R5.png'),
    pygame.image.load('assets/img_sprite/R6.png'),
    pygame.image.load('assets/img_sprite/R7.png'),
    pygame.image.load('assets/img_sprite/R8.png'),
    pygame.image.load('assets/img_sprite/R9.png')
]
walkLeft = [
    pygame.image.load('assets/img_sprite/L1.png'),
    pygame.image.load('assets/img_sprite/L2.png'),
    pygame.image.load('assets/img_sprite/L3.png'),
    pygame.image.load('assets/img_sprite/L4.png'),
    pygame.image.load('assets/img_sprite/L5.png'),
    pygame.image.load('assets/img_sprite/L6.png'),
    pygame.image.load('assets/img_sprite/L7.png'),
    pygame.image.load('assets/img_sprite/L8.png'),
    pygame.image.load('assets/img_sprite/L9.png')
]
char = pygame.image.load('assets/img_sprite/standing.png')
#BACKGROUND
bg = pygame.image.load(os.path.join("assets", "map.png"))

largeurHex = 35
hauteurHex = 40
layout = Layout(orientation_pointy, (largeurHex, hauteurHex), (165, 165))

#print(hex_to_pixel(layout,Hex(1,0)))


def hexpointed(tup, layout):
    x, y = tup[0], tup[1]
    return hex_to_pixel(layout, pixel_to_hex(layout, (x, y)))


Grid = initgrid(8, 12)
Grid.remove(Hex(1, 1))


def redraw_window():
    screen.blit(bg, (0, 0))  #Background

    for element in Grid:
        pygame.draw.polygon(screen, (0, 0, 0), hex_corner(layout, element),
                            2)  #Grid layout
    pygame.draw.polygon(screen, (255, 0, 0), hex_corner(layout, Hex(1, 1)))

    x, y = pygame.mouse.get_pos()
    if pixel_to_hex(layout, (x, y)) in Grid:
        pygame.draw.polygon(screen, (255, 0, 0, 255),
                            hex_corner(layout, pixel_to_hex(layout, (x, y))),
                            5)  #Mouse cap

    man.draw(screen)
    #Player
    """Draw text:
    lives_label = main_font.render(f"LIVES: {lives}",1,RED)
    level_label = main_font.render(f"LEVEL: {level}",1,RED)
    screen.blit(lives_label,(10,10))
    screen.blit(level_label,(WIDTH - level_label.get_width()-10, 10))
    pygame.draw.rect(screen,(255,0,255),(100,100,100,100))
    """


run = True
FPS = 30
clock = pygame.time.Clock()


def goto(tobechangedelmt):
    #x,y=tup[0]-man.width/2,tup[1]-man.heigth/2-8
    if tobechangedelmt == Hex(1, 0):  #Hex to right
        man.right = True
        stepnumber = int((2 * largeurHex) // man.change)
        horizon_step = man.change
        for k in range(stepnumber):
            clock.tick(FPS)
            man.playerX += horizon_step
            redraw_window()
            pygame.display.update()
        clock.tick(FPS)
        man.playerX += 2 * largeurHex - stepnumber * horizon_step
        redraw_window()
        pygame.display.update()
        man.right = False

    if tobechangedelmt == Hex(0, 1):  #Hex down right
        man.right = True
        stepnumber = int(
            sqrt(largeurHex * largeurHex + 4 * hauteurHex * hauteurHex) //
            man.change)
        #vertical_step = man.change* sin(pi/6)
        vertical_step = (hauteurHex + largeurHex * sin(pi / 6)) // stepnumber
        #print(f"{hauteurHex+largeurHex*sin(pi/6)}//{stepnumber} ={vertical_step}")
        #horizon_step= man.change * cos(pi/6)
        horizon_step = largeurHex // stepnumber
        for k in range(stepnumber):
            clock.tick(FPS)
            man.playerY += vertical_step
            man.playerX += horizon_step
            redraw_window()
            pygame.display.update()
        clock.tick(FPS)
        man.playerX += largeurHex - stepnumber * horizon_step
        man.playerY += (hauteurHex + largeurHex *
                        sin(pi / 6)) - stepnumber * vertical_step + 2
        redraw_window()
        pygame.display.update()
        man.right = False

    if tobechangedelmt == Hex(-1, 1):  #Hex down left
        man.left = True
        stepnumber = int(
            sqrt(largeurHex * largeurHex + 4 * hauteurHex * hauteurHex) //
            man.change)
        vertical_step = (hauteurHex + largeurHex * sin(pi / 6)) // stepnumber
        horizon_step = largeurHex // stepnumber
        for k in range(stepnumber):
            clock.tick(FPS)
            man.playerY += vertical_step
            man.playerX -= horizon_step
            redraw_window()
            pygame.display.update()
        clock.tick(FPS)
        man.playerX -= largeurHex - stepnumber * horizon_step
        man.playerY += (hauteurHex + largeurHex *
                        sin(pi / 6)) - stepnumber * vertical_step + 2
        redraw_window()
        pygame.display.update()
        man.left = False

    if tobechangedelmt == Hex(-1, 0):  #Hex to left
        man.left = True
        stepnumber = int((2 * largeurHex) // man.change)
        horizon_step = man.change
        for k in range(stepnumber):
            clock.tick(FPS)
            man.playerX -= horizon_step
            redraw_window()
            pygame.display.update()
        clock.tick(FPS)
        man.playerX -= 2 * largeurHex - stepnumber * horizon_step
        redraw_window()
        pygame.display.update()
        man.left = False

    if tobechangedelmt == Hex(0, -1):  #Hex up left
        man.left = True
        stepnumber = int(
            sqrt(largeurHex * largeurHex + 4 * hauteurHex * hauteurHex) //
            man.change)
        vertical_step = (hauteurHex + largeurHex * sin(pi / 6)) // stepnumber
        horizon_step = largeurHex // stepnumber
        for k in range(stepnumber):
            clock.tick(FPS)
            man.playerY -= vertical_step
            man.playerX -= horizon_step
            redraw_window()
            pygame.display.update()
        clock.tick(FPS)
        man.playerX -= largeurHex - stepnumber * horizon_step
        man.playerY -= (hauteurHex + largeurHex *
                        sin(pi / 6)) - stepnumber * vertical_step + 2
        redraw_window()
        pygame.display.update()
        man.left = False

    if tobechangedelmt == Hex(1, -1):  #Hex up right
        man.right = True
        stepnumber = int(
            sqrt(largeurHex * largeurHex + 4 * hauteurHex * hauteurHex) //
            man.change)
        #vertical_step = man.change* sin(pi/6)
        vertical_step = (hauteurHex + largeurHex * sin(pi / 6)) // stepnumber
        #print(f"{hauteurHex+largeurHex*sin(pi/6)}//{stepnumber} ={vertical_step}")
        #horizon_step= man.change * cos(pi/6)
        horizon_step = largeurHex // stepnumber
        for k in range(stepnumber):
            clock.tick(FPS)
            man.playerY -= vertical_step
            man.playerX += horizon_step
            redraw_window()
            pygame.display.update()
        clock.tick(FPS)
        man.playerX += largeurHex - stepnumber * horizon_step
        man.playerY -= (hauteurHex + largeurHex *
                        sin(pi / 6)) - stepnumber * vertical_step + 2
        redraw_window()
        pygame.display.update()
        man.right = False
    #man.playerX = int(x)
    #man.playerY = int(y)
    redraw_window()
    #print(x-man.playerX,y-man.playerY)


poshex = Hex(0, 1)
pospix = hex_to_pixel(layout, poshex)
man = player(pospix[0], pospix[1], 64, 64)
run = True
man.left = False
man.right = False
redraw_window()
listecase = []
i = 0

while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

    x, y = pygame.mouse.get_pos()

    ###############################################DANGER###########################################
    #pygame.draw.polygon(screen,(0,0,0),hex_corner(layout,pixel_to_hex(layout,(x,y))))

    if mouse[2] and listecase == []:  #Right click
        print(x, y)
        hextogo = pixel_to_hex(layout, (x, y))

        #print(poshex)
        print(hextogo)
        if hextogo in Grid:
            listecase = pathfinding(poshex, hextogo, Grid)
            print(listecase)

    if i != len(listecase):
        goto(listecase[i] - poshex)
        poshex = listecase[i]
        i += 1
        clock.tick(5)
    else:
        listecase = []
        i = 0

    if keys[K_i]:
        print(8)
    """
    if keys[pygame.K_LEFT] and man.playerX > man.change:
        man.playerX -= man.change
        man.left = True
        man.right = False
    elif keys[pygame.K_RIGHT] and man.playerX < WIDTH - man.change - man.width:
        man.playerX += man.change
        man.left = False
        man.right = True
    else:
        man.left = False
        man.right = False


    if keys[pygame.K_UP] and man.playerY > man.change:
        man.playerY -= man.change
    if keys[pygame.K_DOWN] and man.playerY < HEIGTH - man.change - man.heigth:
        man.playerY += man.change
        
    if not(man.isJump):
        if keys[pygame.K_SPACE]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.playerY -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    """
    redraw_window()
    pygame.display.update()

pygame.quit()