import pygame as pg
from copy import deepcopy
from settings import *
from pygame.constants import KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP


class Item(pg.sprite.Sprite):
    def __init__(self, ID, name):  # , image, name, pos_x, pos_y
        super(Item, self).__init__()
        self.pos_x = 0
        self.pos_y = 0
        self.ID = ID
        self.name = name
        self.image = resize(pg.image.load(
            path.join(item_folder, f'i ({self.ID}).png')), ITEM_SIZE)
        self.to_print = self.image
        self.rect = self.image.get_size()
        self.centerx = self.pos_x + (self.rect[0]/2)
        self.centery = self.pos_y + (self.rect[1]/2)
        # self.name = name
        self.quantity = 1
        self.clicked = False
        self.price = 100

    # Is true if the mouse is over the sprite
    def is_over(self, pos_mouse):
        return self.pos_x < pos_mouse[0] < self.pos_x + self.rect[0] and self.pos_y < pos_mouse[1] < self.pos_y + self.rect[1]

    # Is true if the user click on the sprite
    def is_clicked(self, mouse, pos_mouse):
        return (mouse[0] and self.pos_x < pos_mouse[0] < self.pos_x + self.rect[0] and self.pos_y < pos_mouse[1] < self.pos_y + self.rect[1])

    def update(self, mouse, pos_mouse):
        # If you click on the item, it will follows the cursor and becomes bigger
        if self.is_clicked(mouse, pos_mouse):
            # print("clicked in item")
            self.pos_x = pos_mouse[0] - self.rect[0]/2 - 5
            self.pos_y = pos_mouse[1] - self.rect[1]/2 - 5
            self.to_print = resize(self.image, ITEM_SIZE+10)
        else:
            self.to_print = self.image

    # Draw the image at the position given
    def draw(self, screen):
        screen.blit(self.to_print, (self.pos_x, self.pos_y))
        self.draw_quantity(screen)

    def draw_quantity(self, screen):
        nb = str(self.quantity)
        font_surface = pg.font.SysFont(
            "Blue Eyes.otf", 20).render(nb, True, (255, 255, 255))
        font_size = [font_surface.get_rect()[2], font_surface.get_rect()[3]]
        screen.blit(
            font_surface, (self.pos_x + self.rect[0]-font_size[0]/2, self.pos_y + self.rect[1]-font_size[1]/2))


class Stuff(Item):
    def __init__(self, ID, name):  # , STR, DEX, CON, INT, WIS, CHA
        # Item.__init__(self)
        super(Stuff, self).__init__(ID, name)
        self.STR = 0
        # self.DEX = DEX
        # self.CON = CON
        # self.INT = INT
        # self.WIS = WIS
        # self.CHA = CHA


class Consumable(Item):
    def __init__(self, health):
        super(Consumable, self).__init__()
        self.health = health


class Sword(Stuff):
    def __init__(self, ID, name, inv="player"):  # , pos_x, pos_y
        super(Sword, self).__init__(ID, name)
        self.STR = 5
        self.inclued_in = inv


class Quest_Item(Item):
    def __init__(self, ID, name):
        super(Quest_Item, self).__init__(ID, name)
        self.price = 2


Lost_ring = Quest_Item(98, "Lost ring", )
Empowered_Sword = Sword(56, "Empowered sword")
Empowered_Staff = Sword(73, "Empowered staff")

Apple = Item(192, "Apple")
Egg = Item(205, "Egg")
Meat = Item(202, "Meat")
Shovel = Item(122, "Shovel")
Pickaxe = Item(121, "Pickaxe")
Axe = Item(120, "Axe")
# Ring = Item(192, "Apple")
# Apple = Item(192, "Apple")
ITEM_DICT = {192:Item(192, "Apple"),205:Item(205, "Egg"),202:Item(202, "Meat"),122:Item(122, "Shovel"),121:Item(121, "Pickaxe"),120:Item(120, "Axe"),98:Lost_ring,56:Empowered_Sword,73:Empowered_Staff}
