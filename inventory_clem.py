from item import *


class Inventory():
    def __init__(self):  # width, x, y
        self.inventory = []
        # for i in range(len(self.inventory)):
        #     self.inventory.append()

        self.width = 9
        self.x = 10
        self.y = 10

    def add(self, item):
        self.inventory.append(item)

    def remove(self, item):
        for i in len(self.inventory):
            if self.inventory[i] == item:
                self.inventory[i] = None

    def draw(self, screen):
        nb_lines = len(self.inventory) // self.width + 1
        for i in range(len(self.inventory)):

            self.inventory[i].draw(screen)
