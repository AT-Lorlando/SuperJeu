from settings import WIDTH
from item import *
import pygame as pg


class Inventory():
    def __init__(self, name="player"):  # width, x, y
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
        self.copyx = 0
        self.copyy = 0
        self.shifted = False
        self.name = name

    def shift(self, x):  # shift the positions of all the items of the inventory
        if not self.shifted:
            self.pos_x += x
            for item in self.inventory:
                item.pos_x += x
                item.image.fill((255, 0, 255))
            self.shifted = True

    def add(self, item):  # add an item of the inventory
        item.pos_x = self.pos_x + (len(self.inventory) % self.width) * 103 + 5
        item.pos_y = self.pos_y + \
            (len(self.inventory) // self.width) * 103 + 5
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
        flag = False
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

        if liberty != 0 and self.index != -1:  # test when the item is dropped

            # find the case where we dropped the item // start
            i = 0
            # find if the mouse is out the inventory
            if pos_mouse[0] < self.pos_x or pos_mouse[0] > self.pos_x + self.rect[0]:
                i = -1
                print("mouse out i")
            else:
                while pos_mouse[0] > col[i] + self.pos_x:  # find the column of the drop
                    i += 1
                    if i >= len(lines):
                        break
            j = 0
            if pos_mouse[1] < self.pos_y or pos_mouse[1] > self.pos_y + self.rect[1]:
                j = -1
                # print("mouse out j")
            else:
                while pos_mouse[1] > lines[j] + self.pos_y:
                    j += 1
                    if j >= len(lines):
                        break
            # find the case where we dropped the item // end

            for item in self.inventory:
                # detect if there is an item at the place
                if item.pos_x == col[i-1] + self.pos_x and item.pos_y == lines[j-1] + self.pos_y and item.name != self.inventory[self.index].name:
                    # print("collision, index :", self.index, "i :", i, "j :", j)
                    item.pos_x = self.copyx
                    item.pos_y = self.copyy

                if i == -1 or j == -1:  # check if the player dropped the item in a correct place
                    # print("invalid place, index :", self.index)
                    self.inventory[self.index].pos_x = self.copyx
                    self.inventory[self.index].pos_y = self.copyy
                    flag = True
                    # return self.index
                else:  # put the item at the rigth place
                    # print("correct place, index :", self.index)
                    self.inventory[self.index].pos_x = col[i-1] + self.pos_x
                    self.inventory[self.index].pos_y = lines[j-1] + self.pos_y

            # reset
            self.index = -1
            # print("reset")

        tab = []
        for item in self.inventory:
            # update the item
            tab.append(item.update(mouse, pos_mouse, liberty))
        for i in range(len(tab)):
            # check if an item is handled
            if tab[i] == 0:
                if self.index == -1 and self.name == self.inventory[i].inclued_in and self.inventory[i].is_clicked(mouse, pos_mouse):
                    # use the copy of the last state to replace the item
                    self.index = i
                    self.copyx = self.inventory[i].pos_x
                    self.copyy = self.inventory[i].pos_y
                    # print("enregistrement", self.copyx,
                    #       self.copyy, self.inventory[i].inclued_in, "i :", i)
                self.index = i  # bring back the index of the item moved
        if flag:
            # print("flag works")
            return self.inventory[self.index]

        return not (0 in tab)

    # def collide(self,pos_mouse):
    #     return (pos_mouse[0] > self.pos_y and pos_mouse[0] < self.pos_y + self.rect[0]) and (pos_mouse[1] > self.pos_y and pos_mouse[1] < self.pos_y + self.rect[1])

    # def switch(self, mouse, pos_mouse, liberty):
    #     if liberty.inclued_in != self.name and self.collide(pos_mouse) :
