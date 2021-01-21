from settings import *
import pygame as pg
from Items import *


class Inventory():
    def __init__(self, width, heigth, rows, columns):
        self.width = WIDTH
        self.heigth = HEIGHT
        self.rows = Inventory_Rows
        self.columns = Inventory_Columns

    def drawInventory(self):
        screen.blit(items[1], (600, 500))


#main_font = pg.font.SysFont("Blue Eyes.otf",30)
screen = pg.display.set_mode((WIDTH, HEIGHT))
screen.fill(BROWN)
pg.display.set_caption("Inventory")

#IMAGE
items = LISTITEMS
#BACKGROUND
bg = pg.image.load(path.join(inventory_folder, "background.png"))


def redraw_window():
    screen.blit(bg, (192, 108))  #Background
    screen.blit(items[0], (500, 500))
    screen.blit(items[1], (600, 500))

    #for element in Grid:
    #    pg.draw.polygon(screen,(0,0,0),hex_corner(layout,element),2)    #Grid layout

    x, y = pg.mouse.get_pos()
    #if pixel_to_hex(layout,(x,y)) in Grid:
    #    pg.draw.polygon(screen,(255,0,0,255),hex_corner(layout,pixel_to_hex(layout,(x,y))),5)  #Mouse cap

    invent.drawInventory()
    #Player
    """Draw text:
    lives_label = main_font.render(f"LIVES: {lives}",1,RED)
    level_label = main_font.render(f"LEVEL: {level}",1,RED)
    screen.blit(lives_label,(10,10))
    screen.blit(level_label,(WIDTH - level_label.get_width()-10, 10))
    pg.draw.rect(screen,(255,0,255),(100,100,100,100))
    """


invent = Inventory(WIDTH, HEIGHT, Inventory_Rows, Inventory_Columns)

FPS = 30
clock = pg.time.Clock()
run = True

while run:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    keys = pg.key.get_pressed()
    mouse = pg.mouse.get_pressed()
    x, y = pg.mouse.get_pos()

    if mouse[0]:
        print(x, y)
    if keys[pg.K_LEFT] and man.playerX > man.change:
        man.playerX -= man.change
        man.left = True
        man.right = False

    redraw_window()
    pg.display.update()

pg.quit()
