import pygame as pg
import sys
from os import path
from inventory_clem import *
import random


class Shop():
    def __init__(self):
        self.rect = (900, 400)
        self.fond = pg.Surface(self.rect)
        self.fond.fill((0, 0, 0))
        self.inv = Inventory()

    def update(self, mouse, pos_mouse):
        return self.inv.update(mouse, pos_mouse)

    def draw(self, screen):
        self.inv.draw(screen)


def create_shop():
    shop = Shop()
    shop.inv.add(Sword("shop1"))
    shop.inv.add(Sword("shop2"))
    shop.inv.add(Sword("shop3"))
    shop.inv.add(Sword("shop4"))
    shop.inv.add(Sword("shop1"))
    shop.inv.add(Sword("shop2"))
    shop.inv.add(Sword("shop3"))
    shop.inv.add(Sword("shop4"))
    shop.inv.add(Sword("shop4"))
    return shop
