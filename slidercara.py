import os
import pygame as pg
import sys
from pygame.locals import *


class Slider():
    def __init__(self, x, y, name):
        # barre
        self.height_barre = 10
        self.end = 120

        self.y_center = y
        self.y_barre = self.y_center - self.height_barre/2
        self.x_barre = x

        self.barre_fond = pg.Surface((self.end, self.height_barre))
        self.barre_fond.fill((255, 0, 0))
        # slider
        self.witdh_slider = 5
        self.height_slider = 50

        self.slider_center = self.y_center
        self.y_slider = self.slider_center - self.height_slider / 2
        self.nb_division = 11

        self.slider_fond = pg.Surface((self.witdh_slider, self.height_slider))
        self.slider_fond.fill((255, 255, 255))
        self.x = self.x_barre + self.end/2  # position du curseur

        # text and name
        self.size_font = 50
        self.font = pg.font.SysFont("Blue Eyes.otf", self.size_font)
        self.name = name

        self.value = str(
            int((self.x-self.x_barre) // (self.end/self.nb_division)))

    def maj(self):
        self.x = self.x_barre + self.end/2
        self.y_barre = self.y_center - self.height_barre/2
        self.slider_center = self.y_center
        self.y_slider = self.slider_center - self.height_slider / 2

    def update(self, button, pos):
        if self.y_slider < pos[1] < self.y_slider + self.height_slider and self.x_barre < pos[0] < self.x_barre + self.end and button[0] != 0:
            y = pos[1]
            self.x = pos[0]

        if self.x < self.x_barre:  # check begin
            self.x = self.x_barre
        if self.x >= self.end - self.witdh_slider + self.x_barre:  # check end
            self.x = self.end - self.witdh_slider + self.x_barre

        self.value = str(int((self.x-self.x_barre) //
                             (self.end/self.nb_division)))

    def draw(self, screen):
        font_surface = self.font.render(
            self.name + " :    "+self.value, True, (255, 255, 255))
        if self.name == "WIS" or self.name == "CHA":
            screen.blit(font_surface, (self.x_barre - font_surface.get_rect()[2] -
                                       20, self.y_barre - self.size_font / 3))
        else:
            screen.blit(font_surface, (self.x_barre + self.end +
                                       50, self.y_barre - self.size_font / 3))

        screen.blit(self.barre_fond, (self.x_barre, self.y_barre))
        screen.blit(self.slider_fond, (self.x, self.y_slider))
        
    


    
