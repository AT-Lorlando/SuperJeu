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
for c in Characters :
    update_grid(Grid,c.poshex)
update_grid(Grid, Tile(Hex(1,1)).set_object("Wall"))

def redraw_window():
    screen.blit(bg, (0, 0))  #Background

    for element in Grid:
        pygame.draw.polygon(screen, (0, 0, 0), hex_corner(layout, element),1)  #Grid layout
    pygame.draw.polygon(screen, (255, 0, 0), hex_corner(layout, Hex(1, 1)))

    x, y = pygame.mouse.get_pos()
    pygame.draw.rect(screen, BLACK,(0,0,100,100),2)
    if pixel_to_hex(layout, (x, y)) in Grid and not any([pixel_to_hex(layout,(Characters[k].playerX,Characters[k].playerY))==pixel_to_hex(layout, (x, y)) for k in range(len(Characters))]):

        pygame.draw.polygon(screen, RED,
                            hex_corner(layout, pixel_to_hex(layout, (x, y))),3)  #Mouse cap

    for k in range(len(Characters)):
        #if pixel_to_hex(layout,(Characters[k].playerX,Characters[k].playerY))==pixel_to_hex(layout, (x, y)):
        #(healtposx,healtposy)=hex_to_pixel(layout,pixel_to_hex(layout,(x,y)))
        (healtposx,healtposy)=hex_to_pixel(layout,pixel_to_hex(layout,((Characters[k].playerX,Characters[k].playerY))))
        healtposx-=largeurHex-7
        healtposy-=hauteurHex
        if not Characters[k].animation[0]:
            screen.blit(health[Characters[k].healthpoint],(healtposx,healtposy) )
    man.drawPlayer(screen)
    skeleton.drawSkeleton(screen)
    gobelin.drawGobelin(screen)
    #Player
    """Draw text:
    lives_label = main_font.render(f"LIVES: {lives}",1,RED)
    level_label = main_font.render(f"LEVEL: {level}",1,RED)
    screen.blit(lives_label,(10,10))
    screen.blit(level_label,(WIDTH - level_label.get_width()-10, 10))
    pygame.draw.rect(screen,(255,0,255),(100,100,100,100))
    """


run =True
FPS = 30
clock = pygame.time.Clock()
listecase = []
i = 0
Try=[]

def goto(whoitis,elmt,KeepRight,KeepLeft):
    if elmt == Hex(1, 0):  #Hex to right
        whoitis.right = True
        stepnumber = int((2 * largeurHex) // whoitis.change)
        horizon_step = whoitis.change
        for k in range(stepnumber):
            clock.tick(FPS)
            whoitis.playerX += horizon_step
            redraw_window()
            pygame.display.update()
        clock.tick(FPS)
        whoitis.playerX += 2 * largeurHex - stepnumber * horizon_step
        redraw_window()
        pygame.display.update()
        if not(KeepRight):whoitis.right = False

    if elmt == Hex(0, 1):  #Hex down right
        whoitis.right = True
        stepnumber = int(
            sqrt(largeurHex * largeurHex + 4 * hauteurHex * hauteurHex) //
            whoitis.change)
        vertical_step = (hauteurHex + largeurHex * sin(pi / 6)) // stepnumber
        horizon_step = largeurHex // stepnumber
        for k in range(stepnumber):
            clock.tick(FPS)
            whoitis.playerY += vertical_step
            whoitis.playerX += horizon_step
            redraw_window()
            pygame.display.update()
        clock.tick(FPS)
        whoitis.playerX += largeurHex - stepnumber * horizon_step
        whoitis.playerY += (hauteurHex + largeurHex *
                        sin(pi / 6)) - stepnumber * vertical_step + 2
        redraw_window()
        pygame.display.update()
        if not(KeepRight):whoitis.right = False

    if elmt == Hex(-1, 1):  #Hex down left
        whoitis.left = True
        stepnumber = int(
            sqrt(largeurHex * largeurHex + 4 * hauteurHex * hauteurHex) //
            whoitis.change)
        vertical_step = (hauteurHex + largeurHex * sin(pi / 6)) // stepnumber
        horizon_step = largeurHex // stepnumber
        for k in range(stepnumber):
            clock.tick(FPS)
            whoitis.playerY += vertical_step
            whoitis.playerX -= horizon_step
            redraw_window()
            pygame.display.update()
        clock.tick(FPS)
        whoitis.playerX -= largeurHex - stepnumber * horizon_step
        whoitis.playerY += (hauteurHex + largeurHex *
                        sin(pi / 6)) - stepnumber * vertical_step + 2
        redraw_window()
        pygame.display.update()
        if not(KeepLeft):whoitis.left = False

    if elmt == Hex(-1, 0):  #Hex to left
        whoitis.left = True
        stepnumber = int((2 * largeurHex) // whoitis.change)
        horizon_step = whoitis.change
        for k in range(stepnumber):
            clock.tick(FPS)
            whoitis.playerX -= horizon_step
            redraw_window()
            pygame.display.update()
        clock.tick(FPS)
        whoitis.playerX -= 2 * largeurHex - stepnumber * horizon_step
        redraw_window()
        pygame.display.update()
        if not(KeepLeft):whoitis.left = False

    if elmt == Hex(0, -1):  #Hex up left
        whoitis.left = True
        stepnumber = int(
            sqrt(largeurHex * largeurHex + 4 * hauteurHex * hauteurHex) //
            whoitis.change)
        vertical_step = (hauteurHex + largeurHex * sin(pi / 6)) // stepnumber
        horizon_step = largeurHex // stepnumber
        for k in range(stepnumber):
            clock.tick(FPS)
            whoitis.playerY -= vertical_step
            whoitis.playerX -= horizon_step
            redraw_window()
            pygame.display.update()
        clock.tick(FPS)
        whoitis.playerX -= largeurHex - stepnumber * horizon_step
        whoitis.playerY -= (hauteurHex + largeurHex *
                        sin(pi / 6)) - stepnumber * vertical_step + 2
        redraw_window()
        pygame.display.update()
        if not(KeepLeft):whoitis.left = False

    if elmt == Hex(1, -1):  #Hex up right
        whoitis.right = True
        stepnumber = int(
            sqrt(largeurHex * largeurHex + 4 * hauteurHex * hauteurHex) //
            whoitis.change)
        vertical_step = (hauteurHex + largeurHex * sin(pi / 6)) // stepnumber
        horizon_step = largeurHex // stepnumber
        for k in range(stepnumber):
            clock.tick(FPS)
            whoitis.playerY -= vertical_step
            whoitis.playerX += horizon_step
            redraw_window()
            pygame.display.update()
        clock.tick(FPS)
        whoitis.playerX += largeurHex - stepnumber * horizon_step
        whoitis.playerY -= (hauteurHex + largeurHex *
                        sin(pi / 6)) - stepnumber * vertical_step + 2
        redraw_window()
        pygame.display.update()
        if not(KeepRight):whoitis.right = False
    whoitis.poshex = Tile(whoitis.poshex+elmt).set_object(whoitis)
    update_grid(Grid, whoitis.poshex)
    redraw_window()
indice=0
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    currentchar=Characters[indice%len(Characters)]

    if keys[pygame.K_a] :
        currentchar.animation[1]=True
    if keys[pygame.K_d] :
        currentchar.animation[0]=True
        #pygame.time.delay(100)
        #Characters.remove(currentchar)

    if keys[pygame.K_b] :
        currentchar.animation[3]=True

    if keys[pygame.K_h] and not currentchar.animation[2]:

        if currentchar.healthpoint>1:
            currentchar.animation[2]=True
            currentchar.healthpoint-=1
        else:
            currentchar.animation[0]=True

    if keys[pygame.K_KP_PLUS] :
        currentchar.animation[0]=False
        currentchar.countdown=0
        if currentchar.healthpoint!=11:
            currentchar.healthpoint+=1
    if keys[pygame.K_KP_MINUS] :
        if currentchar.healthpoint !=0:
            currentchar.healthpoint-=1
        elif currentchar.healthpoint==0 and not currentchar.animation[2]:
            currentchar.animation[0]=True

    if keys[pygame.K_r]:
        currentchar.animation[0]=False
        currentchar.countdown=0
        currentchar.healthpoint=11

    if mouse [0] and 0<x<100 and 0<y<100:
        indice+=1
        pygame.time.delay(100)



    if mouse[2] and listecase == [] and not any([pixel_to_hex(layout,(Characters[k].playerX,Characters[k].playerY))==pixel_to_hex(layout, (x, y)) for k in range (len(Characters))]):    #Right click
        hextogo = pixel_to_hex(layout, (x, y))
        if hextogo in Grid :
            if Grid[Grid.index(hextogo)].object == None :
                listecase = pathfinding(currentchar.poshex, hextogo, Grid)
                if listecase == -1 :
                    print("baisé")
                    pygame.time.delay(1000)
                    continue

    if i < (len(listecase)-1) and listecase!=[]:
        if listecase[i+1]-listecase[i] in [Hex(1, -1),Hex(0, 1),Hex(1,0)] and listecase[i]-currentchar.poshex in [Hex(1, -1),Hex(0, 1),Hex(1,0)]:
            KeepRight=True
            currentchar.faceleft=False

        elif listecase[i+1]-listecase[i] in [Hex(0, -1),Hex(-1, 0),Hex(-1, 1)] and listecase[i]-currentchar.poshex in [Hex(0, -1),Hex(-1, 0),Hex(-1, 1)]:
            KeepLeft=True
            currentchar.faceleft=True
        else:
            KeepRight,KeepLeft=False,False
        tile_left = deepcopy(currentchar.poshex)
        tile_left.remove_object()
        update_grid(Grid, tile_left)
        print(currentchar.poshex.object == None)
        goto(currentchar,listecase[i] - currentchar.poshex,KeepRight,KeepLeft)
        currentchar.poshex = listecase[i].set_object(currentchar)
        i += 1
    elif i == (len(listecase)-1) and listecase!=[]:
        if listecase[i]-currentchar.poshex in [Hex(1, -1),Hex(0, 1),Hex(1,0)]:
            currentchar.faceleft=False
        elif listecase[i]-currentchar.poshex in [Hex(0, -1),Hex(-1, 0),Hex(-1, 1)]:
            currentchar.faceleft=True
        tile_left = deepcopy(currentchar.poshex)
        tile_left.remove_object()
        update_grid(Grid, tile_left)
        goto(currentchar,listecase[i] - currentchar.poshex,False,False)
        currentchar.poshex = listecase[i].set_object(currentchar)
        i += 1
    else:
        listecase = []
        i = 0

    redraw_window()
    pygame.display.update()

pygame.quit()