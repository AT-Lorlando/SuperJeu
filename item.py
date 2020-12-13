import pygame
from copy import deepcopy

from pygame.constants import KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP


class Item(pygame.sprite.Sprite):
    def __init__(self):  # , image, name, pos_x, pos_y
        super(Item, self).__init__()
        self.pos_x = 0
        self.pos_y = 0
        self.image = pygame.Surface((90, 90))
        self.image.fill((255, 255, 0))
        self.print = self.image
        self.rect = self.image.get_size()
        self.centerx = self.pos_x + (self.rect[0]/2)
        self.centery = self.pos_y + (self.rect[1]/2)
        # self.name = name
        self.quantity = 1
        self.clicked = False

    # Is true if the mouse is over the sprite
    def is_over(self, pos_mouse):
        return self.pos_x < pos_mouse[0] < self.pos_x + self.rect[0] and self.pos_y < pos_mouse[1] < self.pos_y + self.rect[1]

    # Is true if the user click on the sprite
    def is_clicked(self, mouse, pos_mouse):
        return (mouse[0] and self.pos_x < pos_mouse[0] < self.pos_x + self.rect[0] and self.pos_y < pos_mouse[1] < self.pos_y + self.rect[1])

    def update(self, mouse, pos_mouse, liberty):
        # If you click on the item, it will follows the cursor and becomes bigger

        if self.is_clicked(mouse, pos_mouse) and liberty:
            self.clicked = True
            return 0
        elif not mouse[0] and not liberty:
            self.clicked = False
            return 1
        if self.clicked:
            self.pos_x = pos_mouse[0] - self.rect[0]/2 - 5
            self.pos_y = pos_mouse[1] - self.rect[1]/2 - 5
            self.print = pygame.transform.scale(
                self.image, (self.rect[0]+10, self.rect[1]+10))
            return 0
        else:
            self.print = self.image
            return 1

    # Draw the image at the position given

    def draw(self, screen):
        screen.blit(self.print, (self.pos_x, self.pos_y))


class Stuff(Item):
    def __init__(self):  # , STR, DEX, CON, INT, WIS, CHA
        # Item.__init__(self)
        super(Stuff, self).__init__()
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
    def __init__(self, name, inv="player"):  # , pos_x, pos_y
        Item.__init__(self)
        super(Sword, self).__init__()
        self.STR = 5
        self.name = name
        self.inclued_in = inv
