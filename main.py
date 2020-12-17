import pygame as pg
import pygame.mixer
import os
import random
import sys
from os import path
from Accueil import *
from Game import *
from Dungeon import *
#from shop import *
from screen_shop import *
from screen_cara import *
from shop import *

pg.init()

run = True
FPS = 60
clock = pg.time.Clock()

main_font = pg.font.SysFont("Blue Eyes.otf", 30)
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("First screen")

# Setup the image directory

# BACKGROUND
bg = pg.image.load(path.join(assets_folder, "menu_background.jpg"))
# dialogue
dialogue = pg.image.load(
    path.join(assets_folder, "dialogue.png")).convert_alpha()

# Dictionnary of buttons
tab_buttons = ["play", "ok", "exit", "options", "restart", "resume", "cancel"]
_button = dict()
for x in tab_buttons:
    _button[x] = pg.image.load(path.join(button_folder, x+".png")).convert()
    _button[x].set_colorkey((93, 94, 94))
    _button[x+"_clicked"] = pg.image.load(
        path.join(button_folder, x+"_clicked.png")).convert()
    _button[x+"_clicked"].set_colorkey((93, 94, 94))

# the coordinates the first buttons
pos_x = WIDTH/2 - _button["play"].get_size()[0]/2
pos_y = HEIGHT/2 - _button["play"].get_size()[1]/2

# Declare the buttons
play = Button(pos_x, pos_y, _button["play"], _button["play_clicked"])
exit = Button(pos_x, pos_y + 100, _button["exit"], _button["exit_clicked"])
options = Button(pos_x, pos_y + 200,
                 _button["options"], _button["options_clicked"])


# Buttons become sprite
buttons = pg.sprite.Group()
buttons.add(play)
buttons.add(exit)
buttons.add(options)

pg.display.flip()
game_launch = False
var = ""
g = Game()
screen_shop = Screen_shop(screen, g)
screen_shop.shop = create_shop()
screen_cara = Screen_cara(screen, g)

while run:
    clock.tick(FPS)

    mouse = pg.mouse.get_pressed()
    x, y = pg.mouse.get_pos()

    var = accueil(screen, bg, buttons, mouse, x, y, play,
                  game_launch, exit, main_font, dialogue, options)
    if var == "exit":
        run = False
    elif var == 'game_launch':
        g.draw_instance(g.hub)
        g.run()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False
            if event.key == pg.K_c:
                screen_cara.run(screen.copy())

    pg.display.update()


pg.quit()
sys.exit()
