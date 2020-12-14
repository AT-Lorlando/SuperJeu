import pygame as pg
import sys
from os import path
from settings import *
import time

class Mother_screen():
    def __init__(self):
        self.running = False
        self.fond = pg.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.liberty = True
        # self.egality
        # self.fratenity

    def print_background(self, background):
        self.screen.blit(background, (0, 0))
        self.screen.blit(self.fond, (0, 0))
        if(self.image):
            for img in self.image:
                self.screen.blit(background, (0, 0))
                self.screen.blit(self.fond, (0, 0))
                self.screen.blit(img, self.image_pos)
                pg.display.flip()
                time.sleep(.03)
              

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

    def run(self, background):
        self.running = True
        self.print_background(background)
        while self.running:
            self.events()
            self.update()
            self.draw()
            pg.display.update()
