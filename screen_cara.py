import pygame as pg
import sys
from os import path
from slidercara import *
from settings import HEIGHT, WIDTH
from Mother_screen import *
import json


class Screen_cara(Mother_screen):
    def __init__(self, screen):
        super(Screen_cara, self).__init__()
        self.screen = screen
        self.STR = Slider(0, 120, "STR")
        self.DEX = Slider(0, 240, "DEX")
        self.CON = Slider(0, 360, "CON")
        self.INT = Slider(0, 480, "INT")
        self.WIS = Slider(0, 600, "WIS")
        self.CHA = Slider(0, 720, "CHA")
        self.attributs = {
            "STR": self.STR,
            "DEX": self.DEX,
            "CON": self.CON,
            "INT": self.INT,
            "WIS": self.WIS,
            "CHA": self.CHA
        }

    def update(self):
        button = pg.mouse.get_pressed()
        pos = pg.mouse.get_pos()
        for slid in self.attributs.values():
            slid.update(button, pos)
        self.save(self.attributs)

    def draw(self):
        for slid in self.attributs.values():
            slid.draw(self.screen)

    def save(self, dictionary):
        with open("attribut.json", mode='w') as f:
            new = dict()
            for x in range(len(dictionary)):
                name = list(dictionary.values())[x].name
                new[name] = list(dictionary.values())[x].value

            json.dump(new, f)
