import pygame as pg
import sys
from os import path
from settings import HEIGHT, WIDTH


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
        while self.running:
            self.print_background(background)
            self.events()
            self.update()
            self.draw()
            pg.display.update()
