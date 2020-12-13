from settings import WIDTH
from item import *
import pygame as pg

class Inventory():
    def __init__(self):  # width, x, y
        self.inventory = []
        # for i in range(len(self.inventory)):
        #     self.inventory.append()
        self.rect = (400, 400)
        self.fond = pg.Surface(self.rect)
        self.fond.fill((255, 0, 0))
        self.width = 3
        self.pos_x = 50
        self.pos_y = 50

    def add(self, item):
        item.pos_x = (len(self.inventory) % self.width) * 100 + 5
        item.pos_y = (len(self.inventory) // self.width) * 100 + 5
        self.inventory.append(item)

    def remove(self, item):
        for i in len(self.inventory):
            if self.inventory[i] == item:
                self.inventory[i] = None

    def draw(self, screen):
        for items in self.inventory:
            screen.blit(items.print, (self.pos_x + items.pos_x, self.pos_y + items.pos_y))
