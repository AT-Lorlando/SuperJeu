import pygame as pg
import sys
from os import path
from shop import *
from settings import HEIGHT, WIDTH
from _screen import *


class Screen_shop(Mother_screen):
    def __init__(self, screen):
        super(Screen_shop, self).__init__()
        self.screen = screen
        # 180 is the argument to change the blur
        self.fond.fill((0, 0, 0, 180))
        self.shop = Shop()

    def update(self):
        self.mouse = pg.mouse.get_pressed()
        self.pos_mouse = pg.mouse.get_pos()
        if self.is_over(self.shop):
            self.shop.fond.fill((255, 255, 255))
        else:
            self.shop.fond.fill((0, 0, 0))

    def draw(self):
        self.screen.blit(self.shop.fond, (self.shop.pos_x, self.shop.pos_y))

    def is_over(self, target):
        return target.pos_x < self.pos_mouse[0] < target.pos_x + target.rect[0] and target.pos_y < self.pos_mouse[1] < target.pos_y + target.rect[1]


