import pygame as pg
import sys
from os import path
from slidercara import *
from settings import HEIGHT, WIDTH
from _screen import *


class Screen_cara(Mother_screen):
    def __init__(self, screen):
        super(Screen_cara, self).__init__()
        self.screen = screen
        self.STR = Slider()
        self.DEX = Slider()
        self.CON = Slider()
        self.INT = Slider()
        self.WIS = Slider()
        self.CHA = Slider()
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
            if slid.y_slider < pos[1] < slid.y_slider + slid.height_slider and button[0] != 0:
                y = pos[1]
                slid.x = pos[0]

            a = slid.x - 5
            if a < 0:
                a = 0
            if slid.x >= slid.end - slid.witdh_slider:
                slid.x = slid.end - slid.witdh_slider
            slid.value = str(int(slid.x // (slid.end/slid.nb_division)))

    def draw(self):
        for x in self.attributs.values():
            self.screen.blit(x.slider_fond, x.x, x.y_slider)
            self.screen.blit(x.barre_fond, x.x_barre, x.y_barre)
