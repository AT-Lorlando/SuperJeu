import pygame
from os import path
from math import sqrt, pi, cos, sin
from Hex import *
from settings import *
from CombatCharacter import *
from spell_copy import *
from random import randint

(WIDTH, HEIGHT)=(1097,720)
pygame.init()

WINDOWSIZE = pygame.display.list_modes()[PYGAMESIZE]
size=WINDOWSIZE
#print(size)
screen = pygame.display.set_mode(size)
#screen = pygame.display.set_mode((1080, 720))
#screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Combat mode")
pygame.display.set_icon(Sword)

##Init



largeurHex=largeurHex*GoldenX
hauteurHex=hauteurHex*GoldenY
layout = Layout(orientation_pointy, (largeurHex, hauteurHex),(
    0+(0.5*size[0]-largeurHex*(Column-0.5)),
    0+(0.4*size[1]-hauteurHex*(1.5*Line-1)/2)
    ))

#print(SHIFT*size[0]//(2*largeurHex)-2,SHIFT*size[1],2*SHIFT*size[1]/(hauteurHex-0.5)//3-2)




thunder.owner=man
sunburn.owner=man
bomb.owner=man
heal.owner=man
man.spellsname.extend((thunder,sunburn,bomb,heal))
man.spells.extend((False,False,False,False))


attack.owner=skeleton
skeleton.spellsname.append(attack)

attack.owner=gobelin
gobelin.spellsname.append(attack)


man.animator=[([Playersprite],[Playersprite],1),([Playersprite],[Playersprite],1),([Playersprite],[Playersprite],1)]
man.spellsanimations=[  (Spell_thunder,Spell_thunder,20),(Spell_sunburn,Spell_sunburn,18), (Spell_bomb,Spell_bomb,20),(Spell_heal,Spell_heal,24)]
man.static=[PlayerRight,PlayerLeft,9,Playersprite,Playersprite]
man.ranged=True

skeleton.animator=[(SkeletonDeadflip,SkeletonDead,30),(SkeletonAttackflip,SkeletonAttack,36),(SkeletonHitflip,SkeletonHit,16),(SkeletonShieldflip,SkeletonShield,38)]
skeleton.spellsanimations=[(SkeletonAttackflip,SkeletonAttack,36)]
skeleton.static=[SkeletonRight,SkeletonLeft,18,Skeletonsprite,Skeletonsrpiteflip]


gobelin.animator=[(GobelinDeadflip,GobelinDead,16),(GobelinAttackflip,GobelinAttack,16),(GobelinHitflip,GobelinHit,8),(GobelinBomb,GobelinBomb,37)]
gobelin.spellsanimations=[(GobelinAttackflip,GobelinAttack,16)]
gobelin.static=[GobelinRight,GobelinLeft,18,Gobelinsprite,Gobelinsrpiteflip]


Characters=[man,skeleton,gobelin]
Friendly=[man]

main_font = pygame.font.SysFont("Blue Eyes.otf", int(30*GoldenY))
spell_font = pygame.font.SysFont("Blue Eyes.otf", int(25*GoldenY))

""" Line = int(2*SHIFT*size[1]/(hauteurHex-0.5)//3-2) 
Column= int(SHIFT*size[0]//(2*largeurHex)-2)
 """

#print(2*Line*hauteurHex,0.8*size[0],3/4*Column*largeurHex,0.8*size[1])
#assert(Line*hauteurHex>=0.8*size[0],Column*largeurHex>=0.8*size[1])
Grid = initgrid(Line, Column)
waitforspell=False
castzone=[]
currentchar=0
for c in Characters :
    update_grid(Grid,c.poshex)
TilesHex=[]
for k in range(10):
    if randint(0,1)%2==0:
        _Line=randint(1,Line-2)
        _Column=randint(1,Column-2)
        if Hex(_Column,_Line) in Grid and Grid[Grid.index(Tile(Hex(_Column,_Line)))].object==None:
            TilesHex.append(Hex(_Column,_Line))

for t in TilesHex:
    t=Tile(t)
    t.set_object("Rock")
    update_grid(Grid,t)

fond = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
bg= bg.convert_alpha()




def redraw_window():
    
    screen.fill(DARKGREY)
    screen.blit(bg, (0+(1-SHIFT)/2*size[0], 0))  #Background
    global x
    global y
    x, y = pygame.mouse.get_pos()
    currentchar=Characters[indice%len(Characters)]
    
    Spell_range()
    GridOverlay()
    Rocky()
    PathAnimation()
    
   
        
    skeleton.draw(screen)
    gobelin.draw(screen)
    man.draw(screen)
    
    HealthView()
    #Button turn
    inventory()
    endbutton()
    
    
def Rocky():
    for elmt in TilesHex:
        pos=(hex_to_pixel(layout,elmt))
        __a=int(pos[0]-Rocks[0].get_width()/2)
        __b=int(pos[1]-Rocks[0].get_height()/2)
        screen.blit(Rocks[(elmt.q+elmt.r)%3],(__a,__b))

def Spell_range():
    if waitforspell:
        for element in castzone:
            pygame.draw.polygon(screen, MEDIUMGREY, hex_corner(layout, element))  #Grid layout

        if pixel_to_hex(layout, (x, y)) in castzone :
            for element in currentspell.computedamagezone(Grid,pixel_to_hex(layout, (x, y))):
                pygame.draw.polygon(screen, DARKGREY, hex_corner(layout, element))

def GridOverlay():
    for element in Grid:
        pygame.draw.polygon(screen, BLACK, hex_corner(layout, element),1)  #Grid layout
    #pygame.draw.polygon(screen, (255, 0, 0), hex_corner(layout, Hex(1, 1)))
StatsX=0.2*size[0]+40*GoldenX
MiddleInventory=((1-SHIFT)/4+SHIFT)*size[1]

def PathAnimation():
    L=[]
    if not (waitforspell):
        if listecase==[]:
            #pygame.draw.circle(screen, BLACK,hex_to_pixel(layout,man.poshex),largeurHex,2)
            if (pixel_to_hex(layout, (x, y)) in Grid) and Grid[Grid.index(pixel_to_hex(layout, (x, y)))].object == None and currentchar in Friendly:
                    L=pathfinding(man.poshex,Tile(pixel_to_hex(layout,(x,y))),Grid,Friendly)
                    for k in range(len(L)):
                        if len(L)<man.movementpoints+2 and k>0:
                            pygame.draw.polygon(screen, WHITE,hex_corner(layout,L[k]),2)
                    if len(L)>man.movementpoints+1:
                        pygame.draw.polygon(screen, BLACK,hex_corner(layout, pixel_to_hex(layout, (x, y))),3)  #Mouse cap
            
    if 1<len(L) and len(L)<(man.movementpoints+2):
        Movement_label = main_font.render(f"MP: {man.movementpoints} - {len(L)-1}",1,WHITE)
    else:
        Movement_label = main_font.render(f"MP: {man.movementpoints}",1,WHITE)
    if waitforspell:
        if man.mana>= currentspell.manacost:
            Mana_level = main_font.render(f"AP: {man.mana} - {currentspell.manacost}",10,WHITE)
        else:
            Mana_level = main_font.render(f"Not enough AP ",1,WHITE)
    else:
        Mana_level = main_font.render(f"AP: {man.mana}",1,WHITE)
    up = MiddleInventory -12*GoldenY
    down= MiddleInventory +37*GoldenY
    screen.blit(Movement_label,(StatsX+50*GoldenX,up+(Icons[1].get_height()-Movement_label.get_height())/2))
    screen.blit(Mana_level,(StatsX+50*GoldenX,down+(Icons[0].get_height()-Mana_level.get_height())/2))
    screen.blit(Icons[0],(StatsX,up))
    screen.blit(Icons[1],(StatsX,down))


def HealthView():
    for k in range(len(Characters)):
        if Characters[k].healthpoint==0:
            (Characters[k].poshex).remove_object()
            update_grid(Grid,(Characters[k].poshex))
            break

        #if Characters[k] not in Friendly:
        #if Characters[k].healthpoint<100:
            
                    #(healtposx,healtposy)=hex_to_pixel(layout,pixel_to_hex(layout,(x,y)))
        (healtposx,healtposy)=hex_to_pixel(layout,pixel_to_hex(layout,((Characters[k].playerX,Characters[k].playerY))))
        healtposx-=largeurHex-7
        healtposy-=hauteurHex
        #if not Characters[k].animation[0]:
            #screen.blit(Dialog,(x,y-Dialog.get_height()))

        A,B=hex_to_pixel(layout,Characters[k].poshex)
        A,B=A-SHIFT*largeurHex,B-hauteurHex
        #pygame.draw.rect(screen, BLACK,(healtposx,healtposy,largeurHex,20),2)
        pygame.draw.rect(screen, lifecolor(Characters[k].healthpoint),(A,B,SHIFT*Characters[k].healthpoint/100*largeurHex*2,10*GoldenY))
        pygame.draw.rect(screen, BLACK,(A,B,SHIFT*largeurHex*2,10*GoldenY),1)
        if pixel_to_hex(layout,(Characters[k].playerX,Characters[k].playerY))==pixel_to_hex(layout, (x, y)):
            CharacterDescriptor(k)
            #screen.blit(Health[Characters[k].healthpoint//10],(healtposx,healtposy))
    #for k in range(len(Characters)):
            
                
    
    hp =  main_font.render(f"{man.healthpoint}",1,WHITE)
    HeartX=(1-SHIFT)/2*size[0]+SHIFT*size[0]*1/8
    HeartY=MiddleInventory+(Spellbar.get_height()-heart.get_height())/2
    pygame.draw.rect(screen, lifecolor(man.healthpoint),pygame.Rect(
        HeartX-100*GoldenX,
        HeartY-0.85*man.healthpoint*GoldenY+85*GoldenY,100*GoldenX,90*GoldenY))
    pygame.draw.rect(screen, DARKGREY,pygame.Rect(HeartX-100*GoldenX,HeartY+90*GoldenY,100*GoldenX,90*GoldenY))
    screen.blit(heart,(HeartX-heart.get_width(),HeartY))
    pygame.draw.rect(screen, DARKGREY,pygame.Rect(HeartX-heart.get_width()-1,HeartY,1,heart.get_height()))
    screen.blit(hp,(HeartX-(heart.get_width()+hp.get_width())/2,HeartY+(heart.get_height()-hp.get_height())/2-5*GoldenY))

def CharacterDescriptor(k):
    screen.blit(Dialog,(x,y-Dialog.get_height()))
    width,height = Dialog.get_width(),Dialog.get_height()

    Character_description_name = spell_font.render(f"{Characters[k].name}",1,WHITE)
    Character_description_Health= spell_font.render(f"{Characters[k].healthpoint} HP",1,WHITE)
    screen.blit(Character_description_name,(
        x+(width-Character_description_name.get_width())/2,
        y-(3*Dialog.get_height()/4+Character_description_name.get_height()/2))
    )
    screen.blit(Character_description_Health,(
        x+(width-Character_description_Health.get_width())/2,
        y-(height/4+Character_description_Health.get_height()/2))
    )

    


def lifecolor(lifelevel):
    if lifelevel>50:
        return (round(2*(1-lifelevel/100)*250),255-lifelevel//100,0)
    return (255,round(2*lifelevel/100*250),0)

inventory_cases=[((SHIFT-0.1)*size[0]-Spellbar.get_width()/2+GoldenX*(60*k+8)) for k in range (9)]

def inventory():
    screen.blit(Spellbar,(
        (SHIFT-0.1)*size[0]-Spellbar.get_width()/2,
        MiddleInventory))
    if currentchar.activespell !=None and waitforspell:
        pygame.draw.rect(screen, RED,pygame.Rect(inventory_cases[currentchar.activespell]+2,MiddleInventory+6*GoldenY,59*GoldenX,59*GoldenY),2)
    for k in range(len(man.spellsname)):
        screen.blit(Spell_icons[k],(inventory_cases[k]+2*k,MiddleInventory+8*GoldenY))
    for k in range(len(man.spellsname)):
        if x>inventory_cases[k] and x<inventory_cases[k+1] and y>MiddleInventory and y<MiddleInventory+Spellbar.get_height():
                Spelldescriptor(k)

def Spelldescriptor(k):
    screen.blit(Dialog,(x,y-Dialog.get_height()))
    width,height = Dialog.get_width(),Dialog.get_height()

    spell_description_name = spell_font.render(f"{man.spellsname[k].name}",1,WHITE)
    spell_description_cost= spell_font.render(f"{man.spellsname[k].manacost}",1,WHITE)
    spell_description_aim= spell_font.render(f"{man.spellsname[k].dammagerange}",1,WHITE)
   
    
    screen.blit(spell_description_name,(
        x+(width-spell_description_name.get_width())/2,
        y-(3*Dialog.get_height()/4+spell_description_name.get_height()/2))
    )

    cut = 6
    
    

    screen.blit(Manacost,(
        x+((1*width/cut-Manacost.get_width())/2),
        y-(height/4+Manacost.get_height()/2))
    )

    screen.blit(spell_description_cost,(
        x+((3*width/cut-spell_description_cost.get_width())/2),
        y-(height/4+spell_description_cost.get_height()/2))
    )

    screen.blit(Aim,(
        x+((5*width/cut-Aim.get_width())/2),
        y-(height/4+Aim.get_height()/2))
    )

    screen.blit(spell_description_aim,(
        x+((7*width/cut-spell_description_aim.get_width())/2),
        y-(height/4+spell_description_aim.get_height()/2))
    )
    if k!=3:
        screen.blit(Sword,(
            x+((9*width/cut-Sword.get_width())/2),
            y-(height/4+Sword.get_height()/2))
        )
        spell_description_dammage = spell_font.render(f"{man.spellsname[k].dammage}",1,WHITE)
    else:
        screen.blit(Medicine,(
            x+((9*width/cut-Medicine.get_width())/2),
            y-(height/4+Medicine.get_height()/2))
        )
        spell_description_dammage = spell_font.render(f"{-man.spellsname[k].dammage}",1,WHITE)

    screen.blit(spell_description_dammage,(
        x+((11*width/cut-spell_description_dammage.get_width())/2),
        y-(height/4+spell_description_dammage.get_height()/2))
    )


Button_position =((0.1+3/4*0.4)*size[0],MiddleInventory+(Spellbar.get_height()-End_button[0].get_height())/2)
def endbutton():
    if whosturn():
        
        if AmIOnendbutton():
            screen.blit(End_button[1],Button_position)
        elif currentchar.movementpoints==0 and currentchar.mana==0:
            screen.blit(End_button[3],Button_position)
        else:
            screen.blit(End_button[0],Button_position)
    else:
        screen.blit(End_button[2],Button_position)

def AmIOnendbutton():
    return x>Button_position[0] and x<Button_position[0]+End_button[0].get_width() and y>Button_position[1] and y<Button_position[1]+End_button[0].get_width() and listecase==[]




run =True
FPS = 30
clock = pygame.time.Clock()
listecase = []
i = 0
Try=[]
TurnCount=0


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
    
def IsAnyoneDoingSomething():
    
    for k in range (len(Characters)):
        for elmt in Characters[k].animation:
            if elmt:
                return True
        for elmt in Characters[k].spells:
            if elmt:
                return True
    return False


def whosturn():
    return currentchar==man

def eastorwest():
    if listecase[-1]-Tile(man.poshex) in [Hex(1, -1),Hex(0, 1),Hex(1,0)]:
        currentchar.faceleft=True
            

    elif listecase[-1]-Tile(man.poshex) in [Hex(0, -1),Hex(-1, 0),Hex(-1, 1)] :
        currentchar.faceleft=False
    
        
stopreach=False
Canfight=False
global x
global y
x,y=0,0
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    #x, y = pygame.mouse.get_pos()
    currentchar=Characters[indice%len(Characters)]
    
    if keys[pygame.K_k]:
        PYGAMESIZE+=1
        WINDOWSIZE = pygame.display.list_modes()[PYGAMESIZE%21]
        size=WINDOWSIZE
        screen = pygame.display.set_mode(size)

    if keys[pygame.K_KP_MINUS]:
        if man.healthpoint>0:
            man.healthpoint-=1

    if keys[pygame.K_KP_PLUS]:
        if man.healthpoint<100:
            man.healthpoint+=1


    ##############################################Player Interaction ###############################################
    if whosturn():          
        if mouse[0]:
            for k in range(len(currentchar.spellsname)):
                if x>inventory_cases[k] and x<inventory_cases[k+1] and y>MiddleInventory and y<MiddleInventory+Spellbar.get_height():
                    #if not waitforspell:
                        currentchar.activespell=k
                        waitforspell=True
                        currentspell=currentchar.spellsname[currentchar.activespell]
                        castzone=currentspell.computecastzone(Grid,currentchar.poshex)
        
                elif (pixel_to_hex(layout,(x,y)) not in castzone) and not(x>(SHIFT-0.1)*size[0]-Spellbar.get_width()/2 and x<(SHIFT-0.1)*size[0]+Spellbar.get_width()/2 and y>MiddleInventory and y<MiddleInventory+Spellbar.get_height()):
                    waitforspell=False  
                    currentchar.activespell=None
                pygame.time.delay(10)
                

            if waitforspell:
                if not any( currentchar.spells):
                    if canispell(pixel_to_hex(layout,(x,y))):
                        
                        currentchar.spells[currentchar.activespell]=True
                        currentchar.spellpos=hex_to_pixel(layout,pixel_to_hex(layout,(x,y)))
                        #Scriptprint(currentchar.name+' uses '+currentchar.spellsname[currentchar.activespell].name+', cost : '+str(currentchar.spellsname[currentchar.activespell].manacost)+' action point(s)')
                        currentchar.spellsname[currentchar.activespell].cast(Grid,pixel_to_hex(layout,(x,y)))
                        waitforspell=False
                    
            
            #if AmIOnendbutton() and not IsAnyoneDoingSomething():
            if AmIOnendbutton():
                waitforspell=False
                indice+=1
                pygame.time.delay(100)
                currentchar=Characters[indice%len(Characters)]
                currentchar.mana=currentchar.maxmana
                currentchar.movementpoints=currentchar.maxmovement
                currentchar.activespell=None
                pygame.time.delay(50)


        if mouse[2] and not waitforspell:
            if listecase == []:    #Right click
                hextogo = Tile(pixel_to_hex(layout, (x, y)))
                if hextogo in Grid :
                    if Grid[Grid.index(hextogo)].object == None :
                        listecase = pathfinding(currentchar.poshex, hextogo, Grid,Friendly)
                        if len(listecase)>currentchar.movementpoints+1:
                            listecase=[]
                        elif listecase == [] :
                            print("Pas de chemin")
                        else:
                            currentchar.movementpoints-=len(listecase)-1
                    
    ##############################################################################################


    ############################IA################################################################
    
    else:
        if currentchar.animation[0]:
            indice+=1
            stopreach=False
            currentchar=Characters[indice%len(Characters)]
            currentchar.mana=currentchar.maxmana
            currentchar.movementpoints=currentchar.maxmovement
            currentchar.activespell=None
            
        elif listecase == []:    
                hextogo = man.poshex
                if hextogo in Grid and not stopreach :
                    listecase = pathfinding(currentchar.poshex, hextogo, Grid,Friendly)
                    #print(len(listecase),len(listecase)>currentchar.movementpoints+3)
                    if len(listecase)>currentchar.movementpoints+2:
                        listecase=listecase[:currentchar.movementpoints+1]
                        
                    
                    else :
                        listecase=listecase[:-1]
                        Canfight=True
                    stopreach=True
                    if listecase == [] :
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
        tile_left = copy(currentchar.poshex)
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
        tile_left = copy(currentchar.poshex)
        tile_left.remove_object()
        update_grid(Grid, tile_left)
        goto(currentchar,listecase[i] - currentchar.poshex,False,False)
        currentchar.poshex = listecase[i].set_object(currentchar)
        i += 1
        #if not (whosturn()) and not IsAnyoneDoingSomething():
        if not(whosturn()):
            indice+=1
            stopreach=False
            if Canfight:
                eastorwest()
                Canfight=False

                currentchar.activespell=0
                currentspell=currentchar.spellsname[currentchar.activespell]
                currentchar.spells[currentchar.activespell]=True
                currentchar.spellpos=man.poshex
                #Scriptprint(currentchar.name+' uses '+currentchar.spellsname[currentchar.activespell].name+', cost : '+str(currentchar.spellsname[currentchar.activespell].manacost)+' action point(s)')
                currentchar.spellsname[currentchar.activespell].cast(Grid,man.poshex)

            currentchar=Characters[indice%len(Characters)]
            currentchar.mana=currentchar.maxmana
            currentchar.movementpoints=currentchar.maxmovement
            currentchar.activespell=None
        
    else:
        listecase = []
        i = 0
    if all([Characters[k].animation[0] for k in range(len(Characters)) if Characters[k] in Friendly ]):
        print("Perdu")
        run =False

    if all([Characters[k].animation[0] for k in range(len(Characters)) if Characters[k] not in Friendly ]):
        print("Gagné")
        run =False

    redraw_window()
    pygame.display.update()

pygame.quit()