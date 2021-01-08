import pygame as pg
import sys
from os import path
from settings import *
import time

class Mother_screen():
    def __init__(self, game):
        self.game = game
        self.running = False
        self.fond = pg.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.liberty = True
        # self.egality
        # self.fratenity
        self.animation = None

    def print_background(self, background=None):
        if background:
            self.screen.blit(background, (0, 0))
        self.screen.blit(self.fond, (0, 0))
        if(self.image):
            self.screen.blit(self.image if type(self.image) != list else self.image[len(self.image)-1], self.image_pos)          

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False

    def update(self):
        pass

    def draw(self):
        pass

    def run(self, background=None):
        if self.animation:
            for img in self.animation:
                self.screen.blit(background, (0, 0))
                self.screen.blit(self.fond, (0, 0))
                self.screen.blit(img, self.image_pos)
                pg.display.flip()
                time.sleep(.03)
        self.running = True
        while self.running:
            self.game.dt_update()
            if background:
                self.print_background(background)
            self.events()
            self.update()
            self.draw()
            pg.display.update()
