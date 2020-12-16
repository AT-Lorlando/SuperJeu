import pygame as pg
import sys
from os import path
from shop import *
from settings import HEIGHT, WIDTH
from Mother_screen import *


class Screen_shop(Mother_screen):
    def __init__(self, screen):
        super(Screen_shop, self).__init__()
        self.screen = screen
        # 180 is the argument to change the blur
        self.fond.fill((0, 0, 0, 180))
        self.shop = create_shop()
        self.player_inventory = None

    def update(self):
        self.mouse = pg.mouse.get_pressed()
        self.pos_mouse = pg.mouse.get_pos()
        self.liberty = (self.player_inventory.update(
            self.mouse, self.pos_mouse, self.liberty) and self.shop.inv.update(self.mouse, self.pos_mouse, self.liberty))
        if self.is_over(self.shop):
            self.shop.fond.fill((255, 255, 255))
        else:
            self.shop.fond.fill((0, 0, 0))

    def draw(self):
        self.screen.blit(
            self.shop.fond, (self.shop.inv.pos_x, self.shop.inv.pos_y))  # fond
        self.shop.draw(self.screen)  # shop
        self.player_inventory.draw(self.screen)  # player inv

    def is_over(self, target):
        return target.inv.pos_x < self.pos_mouse[0] < target.inv.pos_x + target.rect[0] and target.inv.pos_y < self.pos_mouse[1] < target.inv.pos_y + target.rect[1]

    def run(self, background, player_inventory):
        self.running = True
        self.player_inventory = player_inventory
        self.player_inventory.shift(500)

        while self.running:
            self.print_background(background)
            self.events()
            self.update()
            # player_inventory.draw(self.screen)
            self.draw()
            pg.display.update()
