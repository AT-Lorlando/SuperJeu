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
        # self.dragged = False

    def shift(self, x):
        self.pos_x += x
        for item in self.inventory:
            item.pos_x += x
            item.image.fill((255, 0, 255))

    def add(self, item):
        item.pos_x = self.pos_x + (len(self.inventory) % self.width) * 100 + 5
        item.pos_y = self.pos_y + (len(self.inventory) // self.width) * 100 + 5
        self.inventory.append(item)
        print("inventaire", item.pos_x, item.pos_y, item.name)

    def remove(self, item):
        for i in len(self.inventory):
            if self.inventory[i] == item:
                self.inventory[i] = None

    def draw(self, screen):
        for items in self.inventory:
            screen.blit(items.print, (items.pos_x, items.pos_y))

    def update(self, mouse, pos_mouse, liberty):
        tab = []
        for item in self.inventory:
            #print("name :", item.name, "len :", len(self.inventory))
            # print("dragged :", self.dragged)
            # print(liberty)
            tab.append(item.update(mouse, pos_mouse, liberty))
            # if dragged != None:
            #     return dragged
        # print(tab)
        return not (0 in tab)
