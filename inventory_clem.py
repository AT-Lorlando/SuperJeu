from settings import assets_folder
from item import *
import pygame as pg
from os import path


class Inventory(pygame.sprite.Sprite):
    def __init__(self, name="player"):  # width, x, y
        self.inventory = []
        super(Inventory, self).__init__()
        self.width = 4
        self.rect = (420, 400)
        self.fond = pg.Surface(self.rect)
        self.fond.fill((0, 255, 255))
        self.pos_x = 0
        self.pos_y = 0
        self.index = -1  # no item is handled
        self.name = name
        for i in range(16):
            case = Case()
            self.add_case(case)

    def shift(self, x):  # shift the positions of all the items of the inventory
        if not self.shifted:
            self.pos_x += x
            for item in self.inventory:
                item.pos_x += x
                item.image.fill((255, 0, 255))
            self.shifted = True

    def remove(self, item):
        i = 0
        copy = []
        for i in range(len(self.inventory)):
            if self.inventory[i] == item:
                pass
            else:
                copy.append(self.inventory[i])
        self.inventory = copy
        print(item.name)

    def draw(self, screen):
        screen.blit(self.fond, (self.pos_x, self.pos_y))
        for i, case in enumerate(self.inventory):
            case.pos_x = self.pos_x + (i % self.width)*100
            case.pos_y = self.pos_y + (i // self.width)*100
            case.draw(screen)

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

    def update(self, mouse, pos_mouse):
        for case in self.inventory:
            case.update(mouse, pos_mouse)

    def add_case(self, case):
        self.inventory.append((case))

    def add_without_case(self, item):
        for case in self.inventory:
            if case.item == None:
                case.item = item
                break

    def add(self, case, item):
        for _case in self.inventory:
            if case == _case:
                case.item = item


class Case(pygame.sprite.Sprite):
    def __init__(self):
        super(Case, self).__init__()
        self.rect = (100, 100)
        self.fond = pg.image.load(
            path.join(assets_folder, "inv_sprite.png"))
        self.fond = pygame.transform.scale(self.fond, self.rect)
        self.width = 4
        self.pos_x = 0
        self.pos_y = 0
        self.item = None

    def update(self, mouse, pos_mouse):
        if self.item != None:
            # print("name :", self.item.name, "coor :",
            #       self.item.pos_x, self.item.pos_y)
            self.item.pos_x = self.pos_x + \
                self.rect[0]//2 - self.item.rect[0]//2
            self.item.pos_y = self.pos_y + \
                self.rect[1]//2 - self.item.rect[1]//2
            self.item.update(mouse, pos_mouse)

    def draw(self, screen):
        screen.blit(self.fond, (self.pos_x, self.pos_y))
        if self.item != None:
            self.item.draw(screen)

    def add(self, item):
        self.item = item

    def remove(self):
        self.item = None
