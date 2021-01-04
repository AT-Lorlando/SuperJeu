import pygame
from os import path
from math import sqrt, pi, cos, sin
from Hex import *
from settings import *
from CombatCharacter import *

WIDTH, HEIGTH = 1097, 720

screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("Combat mode")

Grid = initgrid(8, 12)
Grid.remove(Hex(1, 1))


def redraw_window():
    screen.blit(bg, (0, 0))  #Background

    for element in Grid:
        pygame.draw.polygon(screen, (0, 0, 0), hex_corner(layout, element),1)  #Grid layout
    pygame.draw.polygon(screen, (255, 0, 0), hex_corner(layout, Hex(1, 1)))

    x, y = pygame.mouse.get_pos()

    if pixel_to_hex(layout, (x, y)) in Grid:
        pygame.draw.polygon(screen, (255, 0, 0, 255),
                            hex_corner(layout, pixel_to_hex(layout, (x, y))),3)  #Mouse cap

    for k in range(len(Characters)):
        if pixel_to_hex(layout,(Characters[k].playerX,Characters[k].playerY))==pixel_to_hex(layout, (x, y)):
            (healtposx,healtposy)=hex_to_pixel(layout,pixel_to_hex(layout,(x,y)))
            #(healtposx,healtposy)=hex_to_pixel(layout,pixel_to_hex(layout,((Characters[k].playerX,Characters[k].playerY))))
            healtposx-=largeurHex-7
            healtposy-=hauteurHex
            screen.blit(health[hp],(healtposx,healtposy) )
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

global hp
hp=5
run =True
FPS = 30
clock = pygame.time.Clock()
listecase = []
i = 0
Try=[]

def goto(elmt,KeepRight,KeepLeft):
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
        vertical_step = (hauteurHex + largeurHex * sin(pi / 6)) // stepnumber
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
        vertical_step = (hauteurHex + largeurHex * sin(pi / 6)) // stepnumber
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
    redraw_window()

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
    
    if keys[pygame.K_h] :
        skeleton.hit=True

    if keys[pygame.K_KP_PLUS] :
        if hp!=11:
            hp+=1
    if keys[pygame.K_KP_MINUS] :
        if hp !=0:
            hp-=1
        elif hp==0:
            skeleton.dead=True



    if mouse[2] and listecase == []:    #Right click
        hextogo = pixel_to_hex(layout, (x, y))
        if hextogo in Grid:
            listecase = pathfinding(poshex, hextogo, Grid)

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
