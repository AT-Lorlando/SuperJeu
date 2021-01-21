import pygame
import os
import random
import sys
from os import path

#define colors
WHITE = (255,255,255)
BLACK =(0,0,0)
RED=(255,0,0)
GREEN =(0,255,0)
BLUE =(0,0,255)
WEIRDBLUE =(27,43,64)
YELLOW = (255,255,0)


from math import ceil
from Hexagons.Hex import *

img_dir=path.join(path.dirname(__file__),'Jeu exemple' ,'imgs')
sprite_dir=path.join(img_dir , 'img_sprite')

pygame.init()
class player(object):
    def __init__(self,playerX,playerY,width,heigth):
        self.playerX = playerX = 515-32
        self.playerY = playerY = 363
        self.width = width
        self.heigth = heigth
        self.change = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount =0
        self.CenterX=self.width//2
        self.CenterY=self.heigth//2+8

    def draw(self, screen):
        
        if self.walkCount + 1 >=30:
            self.walkCount = 0

        if man.left:
            screen.blit(walkLeft[(self.walkCount//3)%9], (self.playerX,self.playerY))
            self.walkCount += 1
        elif self.right:
            screen.blit(walkRight[(self.walkCount//3)%9], (self.playerX,self.playerY))
            self.walkCount +=1
        else:
            screen.blit(char, (self.playerX,self.playerY))


WIDTH, HEIGTH  = 1097, 720

level = 1
lives = 5
RED = (255,0,0)
main_font = pygame.font.SysFont("Blue Eyes.otf",30)
screen = pygame.display.set_mode((WIDTH,HEIGTH))
pygame.display.set_caption("Sprite and Animation")

# path.join(sprite_dir,"starfield.png")
#IMAGE
walkRight = [pygame.image.load(path.join(sprite_dir,"R1.png")).convert_alpha(),pygame.image.load(path.join(sprite_dir,"R2.png")).convert_alpha(),pygame.image.load(path.join(sprite_dir,"R3.png")).convert_alpha(),pygame.image.load(path.join(sprite_dir,"R4.png")).convert_alpha(),pygame.image.load(path.join(sprite_dir,"R5.png")).convert_alpha(),pygame.image.load(path.join(sprite_dir,"R6.png")).convert_alpha(),pygame.image.load(path.join(sprite_dir,"R7.png")).convert_alpha(),pygame.image.load(path.join(sprite_dir,"R8.png")).convert_alpha(),pygame.image.load(path.join(sprite_dir,"R9.png")).convert_alpha()]
walkLeft = [pygame.image.load(path.join(sprite_dir,"L1.png")).convert_alpha(),pygame.image.load(path.join(sprite_dir,"L2.png")).convert_alpha(),pygame.image.load(path.join(sprite_dir,"L3.png")).convert_alpha(),pygame.image.load(path.join(sprite_dir,"L4.png")).convert_alpha(),pygame.image.load(path.join(sprite_dir,"L5.png")).convert_alpha(),pygame.image.load(path.join(sprite_dir,"L6.png")).convert_alpha(),pygame.image.load(path.join(sprite_dir,"L7.png")).convert_alpha(),pygame.image.load(path.join(sprite_dir,"L8.png")).convert_alpha(),pygame.image.load(path.join(sprite_dir,"L9.png")).convert_alpha()]

char = pygame.image.load(path.join(sprite_dir,"standing.png")).convert_alpha()


#BACKGROUND
bg = pygame.image.load(path.join(img_dir,"map.png")).convert_alpha()

layout=Layout(orientation_pointy,(35,40),(165,165))


#print(hex_to_pixel(layout,Hex(1,0)))

def initgrid(x,y):
    Grid=[]
    k=1
    for i in range(x) :
        k+=(i)%2 -1
        for j in range(k,y+k):
            Grid.append(Hex(j,i))
    return Grid


def hexpointed(tup,layout):
    x,y=tup[0],tup[1]
    return hex_to_pixel(layout,pixel_to_hex(layout,(x,y)))



Grid=initgrid(8,12)


def redraw_window():
    screen.blit(bg,(0,0)) #Background

    for element in Grid:
        pygame.draw.polygon(screen,(0,0,0),hex_corner(layout,element),2)    #Grid layout

    x,y=pygame.mouse.get_pos()

    if pixel_to_hex(layout,(x,y)) in Grid:
        pygame.draw.polygon(screen,(255,0,0,255),hex_corner(layout,pixel_to_hex(layout,(x,y))),5)  #Mouse cap
    
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
FPS = 60
clock = pygame.time.Clock()

def pathfinding(tup):
    return [Hex(1,0),Hex(0,1),Hex(-1,1),Hex(-1,0),Hex(0,-1),Hex(1,-1)]

def goto(tup):
    #x,y=tup[0]-man.width/2,tup[1]-man.heigth/2-8
    path=pathfinding(tup)
    for tobechangedelmt in path:
        #current pos - destination
        if tobechangedelmt==Hex(0,1):                  #Hex to right
            man.right=True
            for k in range(70//man.change):
                clock.tick(FPS)
                man.playerX+=man.change
                redraw_window()
                pygame.display.update()
            man.right=False

        if tobechangedelmt==Hex(0,-1):                 #Hex to left
            man.left=True
            for k in range(70//man.change):
                clock.tick(FPS)
                man.playerX-=man.change
                redraw_window()
                pygame.display.update()
            man.left=False

        if tobechangedelmt==Hex(1,1):
            man.right=True
            for k in range(70//man.change):
                clock.tick(FPS)
                man.playerY-=man.change*0.866
                man.playerX+=man.change*0.5
                redraw_window()
                pygame.display.update()
            man.right=False

        if tobechangedelmt==Hex(-1,1):
            man.left=True
            for k in range(70//man.change):
                clock.tick(FPS)
                man.playerY-=man.change*0.866
                man.playerX-=man.change*0.5
                redraw_window()
                pygame.display.update()
            man.left=False

        if tobechangedelmt==Hex(1,-1):
            man.right=True
            for k in range(70//man.change):
                clock.tick(FPS)
                man.playerY+=man.change*0.866
                man.playerX+=man.change*0.5
                redraw_window()
                pygame.display.update()
            man.right=False

        if tobechangedelmt==Hex(-1,-1):
            man.left=True
            for k in range(70//man.change):
                clock.tick(FPS)
                man.playerY+=man.change*0.86
                man.playerX-=man.change*0.5
                redraw_window()
                pygame.display.update()
            man.playerY=tup[1]-man.CenterY
            print(man.playerY)
            redraw_window()
            pygame.display.update()
            man.left=False


    #man.playerX = int(x)
    #man.playerY = int(y)
    redraw_window()
    #print(x-man.playerX,y-man.playerY)

    run  = True
    man.left = False
    man.right = False


man = player(200,200,64,64)
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run  = False
        
    #keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()

    x,y = pygame.mouse.get_pos()
    if mouse[2] and pixel_to_hex(layout,(x,y)) in Grid:	#Right click
        goto(hexpointed((x,y),layout))
        print("Coo",hexpointed((x,y),layout))
    	
    redraw_window()
    pygame.display.update()

pygame.quit()