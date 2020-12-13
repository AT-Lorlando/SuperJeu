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
        self.fond.fill((0, 0, 0, 0))
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
        # self.save(self.attributs)

    def draw(self):
        for slid in self.attributs.values():
            slid.draw(self.screen)

    def save(self, dictionary):
        with open("attribut.json", mode='w') as f:
            new = dict()
            for x in dictionary.items():
                new[x[0]] = x[1].value

            json.dump(new, f)

    def run(self, background):

        self.running = True
        # set the coor of center of the hex of attributs
        self.coord((400, 1000), 250)
        for x in self.attributs.items():
            x[1].maj()

        while self.running:
            self.print_background(background)
            self.events()
            self.update()
            self.draw()
            pg.display.update()
        self.save(self.attributs)

    def coord(self, center, radius):
        self.attributs["STR"].x_barre = center[1]
        self.attributs["STR"].y_center = center[0] + radius

        self.attributs["DEX"].x_barre = center[1] + radius * 0.866
        self.attributs["DEX"].y_center = center[0] + radius * 0.5

        self.attributs["CON"].x_barre = center[1] + radius * 0.866
        self.attributs["CON"].y_center = center[0] - radius * 0.5

        self.attributs["INT"].x_barre = center[1]
        self.attributs["INT"].y_center = center[0] - radius

        self.attributs["WIS"].x_barre = center[1] - radius * 0.866
        self.attributs["WIS"].y_center = center[0] - radius * 0.5

        self.attributs["CHA"].x_barre = center[1] - radius * 0.866
        self.attributs["CHA"].y_center = center[0] + radius * 0.5

    # def draw_hex(self) :
