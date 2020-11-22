import pygame
import os
import random
import sys
from os import path
import Accueil



pygame.init()

run =True
FPS = 60
WIDTH, HEIGTH  = 1097, 720
clock = pygame.time.Clock()

main_font = pygame.font.SysFont("Blue Eyes.otf",30)
screen = pygame.display.set_mode((WIDTH,HEIGTH))
pygame.display.set_caption("First screen")



img_dir=path.join(path.dirname(__file__),'Jeu exemple' ,'imgs')
sprite_dir=path.join(img_dir , 'img_sprite')

#BACKGROUND
bg=pygame.image.load(path.join(img_dir,"map.png")).convert_alpha()

# Play

tab_buttons = ["play", "ok","exit"]
_button = dict()
for x in tab_buttons:
    _button[x] =  pygame.image.load(x+".png").convert()
    _button[x].set_colorkey((93,94,94))
    _button[x+"_clicked"] = pygame.image.load(x+"_clicked.png").convert()
    _button[x+"_clicked"].set_colorkey((93,94,94))


pos_x = WIDTH/2 - _button["play"].get_size()[0]/2
pos_y = HEIGTH/2 - _button["play"].get_size()[1]/2
play=Accueil.Button(pos_x,pos_y,_button["play"],_button["play_clicked"])
exit=Accueil.Button(pos_x ,pos_y + 100,_button["exit"],_button["exit_clicked"])

buttons = pygame.sprite.Group()
buttons.add(play)
buttons.add(exit)

pygame.display.flip()
i=0
game_launch = False
var = "rien"

while run:
    clock.tick(FPS)
    
    mouse = pygame.mouse.get_pressed()
    x,y = pygame.mouse.get_pos()

    var = Accueil.accueil(screen,bg,buttons,mouse,x,y,play,game_launch,exit)
    print(var)

    if var == "exit" :
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run  = False



    pygame.display.update()

pygame.quit()

# w = Window()
# w.main()