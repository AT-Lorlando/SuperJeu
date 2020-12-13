import pygame as pg
import sys
from os import path
from inventory_clem import *
import random


class Shop():
    def __init__(self):
        self.rect = (900, 500)
        self.fond = pg.Surface(self.rect)
        self.fond.fill((0, 0, 0))
        self.pos_x = 50
        self.pos_y = 50
        self.inv = Inventory()

    def update(self):
        pass


def create_shop():
    shop = Shop()
    shop.inv.add(Sword("epee"))
    return shop
