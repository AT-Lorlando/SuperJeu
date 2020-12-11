import os
import pygame as pg
import sys
from pygame.locals import *


class Slider():
    def __init__(self):
        # barre
        self.height_barre = 10
        self.end = 640

        self.y_center = 120
        self.y_barre = self.y_center - self.height_barre/2
        self.x_barre = 0

        self.barre_fond = pg.Surface((self.end, self.height_barre))
        self.barre_fond.fill((255, 0, 0))
        # slider
        self.witdh_slider = 20
        self.height_slider = 120

        self.slider_center = self.y_center
        self.y_slider = self.slider_center - self.height_slider / 2
        self.nb_division = 11

        self.slider_fond = pg.Surface((self.witdh_slider, self.height_slider))
        self.slider_fond.fill((255, 0, 0))
        self.x = 100  # position du curseur

        # other
        self.value = str(int(self.x // (self.end/self.nb_division)))
