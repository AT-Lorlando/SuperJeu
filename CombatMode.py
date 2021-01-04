import pygame
from os import path
import random

from math import ceil, sqrt, pi, cos, sin
from Hex import *
from settings import *



class player(object):
    def __init__(self, playerX, playerY, width, heigth):
        self.playerX = playerX
        self.playerY = playerY
        self.width = width
        self.heigth = heigth
        self.change = 5
        self.attack=False
        self.attackCount = 0
        self.dead=False
        self.deadcount = 0
        
        self.left = False
        self.right = False
        self.walkCount = 0
        self.CenterX = self.width // 2
        self.CenterY = self.heigth // 2 + 8

    def drawPlayer(self, screen):
        relativeX = self.playerX - Playercombathorizontalshift
        relativeY = self.playerY - Playercombatverticalshift
        
        if man.left:
            screen.blit(walkLeft[self.walkCount%9],
                        (relativeX, relativeY))
            self.walkCount += 1
        elif self.right:
            screen.blit(walkRight[self.walkCount%9],
                        (relativeX, relativeY))
            self.walkCount += 1
        else:
            screen.blit(char, (relativeX, relativeY))

    def drawSkeleton(self, screen):
        relativeX = self.playerX - Skeletoncombathorizontalshift
        relativeY = self.playerY - Skeletoncombatverticalshift
        
        if self.attackCount==18:
            self.attack=False
            self.attackCount=0
        elif self.attack and self.attackCount<18:
            print(self.attackCount)
            screen.blit(SkeletonAttack[self.attackCount],(relativeX, relativeY))
            self.attackCount += 1
        elif self.deadcount==28:
            self.dead=False
            self.deadcount=0
        elif self.dead and self.deadcount<28:
            print(self.deadcount)
            screen.blit(SkeletonDead[self.deadcount],(relativeX, relativeY))
            self.deadcount += 1
        elif self.right:
            screen.blit(walkRight[self.walkCount%9],
                        (relativeX, relativeY))
            self.walkCount += 1
        else:
            screen.blit(skeletonsprite, (relativeX, relativeY))


WIDTH, HEIGTH = 1097, 720

RED = (255, 0, 0)
#main_font = pygame.font.SysFont("Blue Eyes.otf", 30)
screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("Combat mode")

#IMAGE

SkeletonAttack = [pygame.transform.scale(pygame.image.load(path.join(skeleton_attack,'Sk'+str(k)+'.png')),SkeletonScale) for k in range(18)]
SkeletonDead = [pygame.transform.scale(pygame.image.load(path.join(skeleton_dead,str(k//2+1)+'.png')),SkeletonScale) for k in range(28)]

walkRight = [pygame.transform.scale(pygame.image.load(path.join(champ_folder,'R'+str(k//3+1)+'.png')),PlayerScale) for k in range(9)]
walkLeft = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(path.join(champ_folder,'R'+str(k//3+1)+'.png')),PlayerScale),True,False) for k in range(9)]

char = pygame.transform.scale(pygame.image.load(path.join(champ_folder,'B1.png')),PlayerScale)
skeletonsprite = pygame.transform.scale(pygame.image.load(path.join(skeleton_folder,'standing.png')),(64,64))
#BACKGROUND
bg = pygame.image.load(path.join(assets_folder,'map.png'))

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

    man.drawPlayer(screen)
    skeleton.drawSkeleton(screen)
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





def goto(elmt,KeepRight,KeepLeft):
    #x,y=tup[0]-man.width/2,tup[1]-man.heigth/2-8
    if elmt == Hex(1, 0):  #Hex to right
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
        if not(KeepRight):man.right = False

    if elmt == Hex(0, 1):  #Hex down right
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
        if not(KeepRight):man.right = False

    if elmt == Hex(-1, 1):  #Hex down left
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
        if not(KeepLeft):man.left = False

    if elmt == Hex(-1, 0):  #Hex to left
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
        if not(KeepLeft):man.left = False

    if elmt == Hex(0, -1):  #Hex up left
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
        if not(KeepLeft):man.left = False

    if elmt == Hex(1, -1):  #Hex up right
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
        if not(KeepRight):man.right = False
    #man.playerX = int(x)
    #man.playerY = int(y)
    redraw_window()
    #print(x-man.playerX,y-man.playerY)


poshex = Hex(0, 1)
pospix = hex_to_pixel(layout, poshex)
man = player(pospix[0], pospix[1], 64, 64)
skeleton = player(hex_to_pixel(layout,Hex(0, 4))[0],hex_to_pixel(layout,Hex(0, 4))[1],64,64)

Characters=man,skeleton
run = True
man.left = False
man.right = False
redraw_window()
listecase = []
i = 0
Try=[]

while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

    x, y = pygame.mouse.get_pos()

    if keys[pygame.K_a] :
        skeleton.attack=True

    if keys[pygame.K_d] :
        skeleton.dead=True

    if mouse[0]:                        #Left Click
        if pixel_to_hex(layout, (x, y)) not in Try:
            Try.append(pixel_to_hex(layout, (x, y)))
            print(Try)
            print(hex_circle(Try[0],100))
            clock.tick(10000)

    

    if mouse[2] and listecase == []:    #Right click
        #print(x, y)
        hextogo = pixel_to_hex(layout, (x, y))

        #print(poshex)
        #print(hextogo)
        if hextogo in Grid:
            listecase = pathfinding(poshex, hextogo, Grid)
            print(listecase)

    if i < (len(listecase)-1) and listecase!=[]:
        if listecase[i+1]-listecase[i] in [Hex(1, -1),Hex(0, 1),Hex(1,0)] and listecase[i]-poshex in [Hex(1, -1),Hex(0, 1),Hex(1,0)]:
            KeepRight=True
        elif listecase[i+1]-listecase[i] in [Hex(0, -1),Hex(-1, 0),Hex(-1, 1)] and listecase[i]-poshex in [Hex(0, -1),Hex(-1, 0),Hex(-1, 1)]:
            KeepLeft=True
        else:
            KeepRight,KeepLeft=False,False

        goto(listecase[i] - poshex,KeepRight,KeepLeft)
        poshex = listecase[i]
        i += 1
    elif i == (len(listecase)-1) and listecase!=[]:
        goto(listecase[i] - poshex,False,False)
        poshex = listecase[i]
        i += 1
    else:
        listecase = []
        i = 0

    redraw_window()
    pygame.display.update()

pygame.quit()
