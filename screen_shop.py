import pygame as pg
import sys
from os import path
from shop import *
from settings import HEIGHT, WIDTH


class Screen_shop() :
    def __init__(self,screen):
        self.running = False
        self.screen = screen
        self.fond = pg.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.fond.fill((0,0,0,180))#180 is the argument to change the blur
        self.shop = Shop()


    def print_background(self,background) :
        self.screen.blit(background,(0,0))
        self.screen.blit(self.fond,(0,0))

    def events(self):
        # catch all events here                                                                                                                                                                                        
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running= False

    def update (self):
        self.mouse = pg.mouse.get_pressed()
        self.pos_mouse = pg.mouse.get_pos()
        if self.is_over(self.shop) :
            self.shop.fond.fill((255,255,255))
        else :
            self.shop.fond.fill((0,0,0))
    

    def draw(self):
        self.screen.blit(self.shop.fond,(self.shop.pos_x,self.shop.pos_y))

    def is_over(self,target) :
        return target.pos_x < self.pos_mouse[0]< target.pos_x + target.rect[0] and target.pos_y < self.pos_mouse[1]< target.pos_y + target.rect[1]

    def run(self,background):
        while self.running : 
            self.print_background(background)
            self.events()
            self.update()
            self.draw()
            pg.display.update()