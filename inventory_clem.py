from settings import WIDTH
from item import *
import pygame as pg


class Inventory():
    def __init__(self):  # width, x, y
        self.inventory = []
        # for i in range(len(self.inventory)):
        #     self.inventory.append()
        self.rect = (420, 400)
        self.fond = pg.Surface(self.rect)
        self.fond.fill((0, 255, 255))
        self.width = 4
        self.pos_x = 50
        self.pos_y = 50
        self.index = -1
        # self.dragged = False

    def shift(self, x):  # shift the positions of all the items of the inventory
        self.pos_x += x
        for item in self.inventory:
            item.pos_x += x
            item.image.fill((255, 0, 255))

    def add(self, item):  # add an item of the inventory
        item.pos_x = self.pos_x + (len(self.inventory) % self.width) * 103 + 10
        item.pos_y = self.pos_y + \
            (len(self.inventory) // self.width) * 103 + 10
        self.inventory.append(item)
        # print("inventaire", item.pos_x, item.pos_y, item.name)

    def remove(self, item):
        for i in len(self.inventory):
            if self.inventory[i] == item:
                self.inventory[i] = None

    def draw(self, screen):
        screen.blit(self.fond, (self.pos_x, self.pos_y))
        for items in self.inventory:
            screen.blit(items.print, (items.pos_x, items.pos_y))
        self.draw_lines()

    def draw_lines(self):
        lines = []
        col = []
        startx = 5
        starty = 5
        endx = self.rect[0]-5
        endy = self.rect[1]-5
        for i in range(self.width + 1):
            col.append(startx + i*(endx//self.width))
        for i in range(4):
            lines.append(starty + i*(endx//self.width))
        for i in range(len(col)):
            for j in range(len(lines)):
                pg.draw.line(self.fond, (0, 0, 0),
                             (col[i], starty), (col[i], endy))
                pg.draw.line(self.fond, (0, 0, 0),
                             (startx, lines[j]), (endx, lines[j]))
        pg.draw.line(self.fond, (0, 0, 0), (startx, endy), (endx, endy))
        pg.draw.line(self.fond, (0, 0, 0), (endx, starty), (endx, endy))

    def update(self, mouse, pos_mouse, liberty):
        tab = []
        for item in self.inventory:
            # update the item
            tab.append(item.update(mouse, pos_mouse, liberty))
        for i in range(len(tab)):
            if tab[i] == 0:
                self.index = i  # bring back the index of the item moved
        if liberty == 1 and self.index != -1:  # test when the item is dropped
            lines = []
            col = []
            startx = 5
            starty = 5
            endx = self.rect[0]-5
            endy = self.rect[1]-5
            for i in range(self.width + 1):
                col.append(startx + i*(endx//self.width))
            for i in range(4):
                lines.append(starty + i*(endx//self.width))
            # replace the item
            i = 0
            while pos_mouse[0] > col[i] + self.pos_x:
                i += 1
            self.inventory[self.index].pos_x = col[i-1] + self.pos_x
            i = 0
            while pos_mouse[1] > lines[i] + self.pos_y:
                i += 1
                if i > len(lines):
                    break
            self.inventory[self.index].pos_y = lines[i-1] + self.pos_y

            # reset
            self.index = -1

        print(self.index)
        return not (0 in tab)
