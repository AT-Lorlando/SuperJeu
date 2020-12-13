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
        self.name = "shop"
        self.inv = Inventory(self.name)

    def update(self, mouse, pos_mouse):
        return self.inv.update(mouse, pos_mouse)

    def draw(self, screen):
        self.inv.draw(screen)


def create_shop():
    shop = Shop()
    shop.inv.add(Sword("shop1", shop.name))
    shop.inv.inventory[0].image.fill((255, 255, 255))
    shop.inv.add(Sword("shop2", shop.name))
    shop.inv.add(Sword("shop3", shop.name))
    shop.inv.add(Sword("shop4", shop.name))
    shop.inv.add(Sword("shop5", shop.name))
    shop.inv.add(Sword("shop6", shop.name))
    shop.inv.add(Sword("shop7", shop.name))
    shop.inv.add(Sword("shop8", shop.name))
    shop.inv.add(Sword("shop9", shop.name))
    return shop
