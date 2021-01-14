import pygame
from os import path
from math import sqrt, pi, cos, sin
from Hex import *
from settings import *
from CombatCharacter import *
from spell_copy import *



layout = Layout(orientation_pointy, (largeurHex, hauteurHex), (165, 165))
pospix = hex_to_pixel(layout, Hex(5,1))

man = player(pospix[0], pospix[1], *PlayerScale)
man.poshex = Tile(Hex(5, 1)).set_object(man)
man.maxmana=6
man.mana=6
thunder.owner=man
man.spellsname.append(thunder)

skeleton = player(hex_to_pixel(layout,Hex(0, 4))[0],hex_to_pixel(layout,Hex(0, 4))[1],*SkeletonScale)
skeleton.poshex = Tile(Hex(0, 4)).set_object(skeleton)

gobelin = player(hex_to_pixel(layout,Hex(2, 3))[0],hex_to_pixel(layout,Hex(2, 3))[1],*GobelinScale)
gobelin.poshex = Tile(Hex(2, 3)).set_object(gobelin)



Characters=[man,skeleton,gobelin]

WIDTH, HEIGTH = 1097, 720
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("Combat mode")
main_font = pygame.font.SysFont("Blue Eyes.otf", 30)
Grid = initgrid(8, 12)

waitforspell=False
castzone=[]
currentchar=0
for c in Characters :
    update_grid(Grid,c.poshex)

Tiles = [Tile(Hex(1,1)),Tile(Hex(2,4)),Tile(Hex(7,5)),Tile(Hex(9,2))]

for t in Tiles:
    t.set_object("Three")
    update_grid(Grid,t)

fond = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
bg= bg.convert_alpha()
def redraw_window():
    screen.blit(bg, (0, 0))  #Background
    x, y = pygame.mouse.get_pos()
    currentchar=Characters[indice%len(Characters)]
    
    if waitforspell:
        for element in castzone:
            pygame.draw.polygon(screen, (255,183, 85,125), hex_corner(layout, element))  #Grid layout

        if pixel_to_hex(layout, (x, y)) in castzone :
            for element in currentspell.computedamagezone(Grid,pixel_to_hex(layout, (x, y))):
                pygame.draw.polygon(screen, (200, 100, 0,125), hex_corner(layout, element))

    for element in Grid:
        pygame.draw.polygon(screen, (0, 0, 0), hex_corner(layout, element),1)  #Grid layout
    #pygame.draw.polygon(screen, (255, 0, 0), hex_corner(layout, Hex(1, 1)))
    
    

    
    
    pygame.draw.rect(screen, BLACK,(0,0,100,100),2)
    if not(currentchar.left or currentchar.right):
        pygame.draw.circle(screen, BLACK,hex_to_pixel(layout,currentchar.poshex),largeurHex,2)
        if (pixel_to_hex(layout, (x, y)) in Grid) and Grid[Grid.index(pixel_to_hex(layout, (x, y)))].object == None:
                L=pathfinding(currentchar.poshex,Tile(pixel_to_hex(layout,(x,y))),Grid)
                for k in range(len(L)):
                    if len(L)<currentchar.movementpoints+2 and k>0:
                        pygame.draw.polygon(screen, BLUE,hex_corner(layout,L[k]),2)
                if len(L)==2:
                    pygame.draw.polygon(screen, BLUE,hex_corner(layout, pixel_to_hex(layout, (x, y))),2)
                else:
                    pygame.draw.polygon(screen, RED,hex_corner(layout, pixel_to_hex(layout, (x, y))),3)  #Mouse cap
        
    for k in range(len(Characters)):
        if pixel_to_hex(layout,(Characters[k].playerX,Characters[k].playerY))==pixel_to_hex(layout, (x, y)):
                (healtposx,healtposy)=hex_to_pixel(layout,pixel_to_hex(layout,(x,y)))
                #(healtposx,healtposy)=hex_to_pixel(layout,pixel_to_hex(layout,((Characters[k].playerX,Characters[k].playerY))))
                healtposx-=largeurHex-7
                healtposy-=hauteurHex
                if not Characters[k].animation[0]:
                    screen.blit(Health[Characters[k].healthpoint//10],(healtposx,healtposy) )
    man.drawPlayer(screen)
    skeleton.drawSkeleton(screen)
    gobelin.drawGobelin(screen)

    level_label = main_font.render(f"Movement Points: {currentchar.movementpoints}",1,RED)
    mana_level = main_font.render(f"Action Points: {currentchar.mana}",1,BLUE)
    hp =  main_font.render(f"{currentchar.healthpoint}",1,BLACK)
    screen.blit(level_label,(110,650))
    screen.blit(mana_level,(110,675))
    pygame.draw.rect(screen, lifecolor(man.healthpoint),pygame.Rect(0,710-0.85*currentchar.healthpoint,100,90))
    screen.blit(heart,(0,620))
    screen.blit(hp,(50-hp.get_width()/2,655))
    

def lifecolor(lifelevel):
    if lifelevel>50:
        return (round(2*(1-lifelevel/100)*250),255-lifelevel//100,0)
    return (255,round(2*lifelevel/100*250),0)





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



def canispell(target):
    return target in castzone and currentchar.mana>= currentspell.manacost
    
    





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
        currentchar.healthpoint=0
        #pygame.time.delay(100)
        #Characters.remove(currentchar)

    if keys[pygame.K_m] :
        currentchar.animation[3]=True

    if keys[pygame.K_b] :
        if not waitforspell:
            currentchar.activespell=0
            waitforspell=True
            print("Spell mode")
            currentspell=currentchar.spellsname[currentchar.activespell]
            castzone=currentspell.computecastzone(Grid,currentchar.poshex)
        else:
            waitforspell=False
            currentchar.activespell=None
            print("Deplacement mode")
            castzone=[]
        pygame.time.delay(100)
        
        
        
        

    if keys[pygame.K_h] and not (currentchar.animation[2] or currentchar.animation[0]):

        if currentchar.healthpoint>5:
            currentchar.animation[2]=True
            currentchar.healthpoint-=5
        else:
            currentchar.animation[0]=True
            currentchar.healthpoint-=5

    if keys[pygame.K_KP_PLUS] :
        currentchar.animation[0]=False
        currentchar.countdown=0
        if currentchar.healthpoint!=100:
            currentchar.healthpoint+=1
    if keys[pygame.K_KP_MINUS] :
        if currentchar.healthpoint >0:
            currentchar.healthpoint-=1
        elif currentchar.healthpoint==0 and not currentchar.animation[2]:
            currentchar.animation[0]=True

    if keys[pygame.K_r]:
        currentchar.animation[0]=False
        currentchar.countdown=0
        currentchar.healthpoint=100


    if mouse[0]:
        if waitforspell and not any( currentchar.spells):
            if canispell(pixel_to_hex(layout,(x,y))):
                currentchar.spells[currentchar.activespell]=True
                currentchar.spellpos=hex_to_pixel(layout,pixel_to_hex(layout,(x,y)))
                currentchar.spellsname[currentchar.activespell].cast(Grid,pixel_to_hex(layout,(x,y)))
        elif 0<x<100 and 0<y<100 and not (currentchar.left or currentchar.right):
            indice+=1
            pygame.time.delay(100)
            currentchar=Characters[indice%len(Characters)]
            currentchar.mana=currentchar.maxmana
            currentchar.movementpoints=currentchar.maxmovement

    if mouse[2] and not waitforspell:
        if listecase == [] and not any([pixel_to_hex(layout,(Characters[k].playerX,Characters[k].playerY))==pixel_to_hex(layout, (x, y)) for k in range (len(Characters))]):    #Right click
            hextogo = pixel_to_hex(layout, (x, y))
            if hextogo in Grid :
                if Grid[Grid.index(hextogo)].object == None :
                    listecase = pathfinding(currentchar.poshex, hextogo, Grid)
                    if len(listecase)>currentchar.movementpoints+1:
                        listecase=[]
                    elif listecase == [] :
                        print("Pas de chemin")
                    else:
                        currentchar.movementpoints-=len(listecase)-1
                    

    if i < (len(listecase)-1) and listecase!=[] :
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