from item import *


class Inventory():
    def __init__(self, size, width, x, y):
        self.inventory = [size]
        for i in range((size)):
            self.inventory[i] = None
        self.width = width
        self.x = x
        self.y = y

    def add(self, pos, item):
        if self.inventory[pos] == None:
            self.inventory[pos] = item
            return 1
        else:
            if item.name == self.inventory[pos].name:
                self.inventory[pos].quantity += 1
                return 1
            else:
                var = self.inventory[pos]
                self.inventory[pos] = item
                return var

    def remove(self, item):
        for i in len(self.inventory):
            if self.inventory[i] == item:
                self.inventory[i] = None

    def draw(self, screen):
        nb_lines = len(self.inventory) // self.width + 1
        for i in range(len(self.inventory)):

            self.inventory[i].draw(screen)
