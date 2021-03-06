import pygame as pg
from settings import *
from os import path
from spell import *
from player import *

class Champion():
    def __init__(self, player):
        self.player = player
        self.actual_frame = 1
        self.time_since_anime = 0
        self.image = pg.Surface((CHARACTER_SIZE, CHARACTER_SIZE))
        self.rect = self.image.get_rect()
        self.spell = pg.sprite.Group()

    def animation(self):
        now = pg.time.get_ticks()
        if(now> self.time_since_anime + 150):
            self.time_since_anime = now
            if(self.player.is_moving == True):
                self.actual_frame = (self.actual_frame + 1) % 3
            else:
                self.actual_frame = 1
            if(self.player.looking_at == 'Right'):
                self.image = self.walk_right[self.actual_frame]
            elif(self.player.looking_at == 'Left'):
                self.image = self.walk_left[self.actual_frame]
            elif(self.player.looking_at == 'Top'):
                self.image = self.walk_top[self.actual_frame]
            elif(self.player.looking_at == 'Bot'):
                self.image = self.walk_bot[self.actual_frame]
        self.image = pg.transform.scale(self.image, (CHARACTER_SIZE,CHARACTER_SIZE))
        self.rect = self.image.get_rect()

class Dark_Wizard(Champion):
    def __init__(self, player):
        super(Dark_Wizard,self).__init__(player)
        self.walk_right = [(pg.image.load(path.join(dark_wizard_folder, f'r{x}.png'))) for x in range(0, 3)] 
        self.walk_left = [(pg.image.load(path.join(dark_wizard_folder, f'l{x}.png'))) for x in range(0, 3)]
        self.walk_top = [(pg.image.load(path.join(dark_wizard_folder, f't{x}.png'))) for x in range(0, 3)]
        self.walk_bot = [(pg.image.load(path.join(dark_wizard_folder, f'b{x}.png'))) for x in range(0, 3)]

class Sun_Wizard(Champion):
    def __init__(self, player):
        super(Sun_Wizard,self).__init__(player)
        self.walk_right = [(pg.image.load(path.join(sun_wizard_folder, f'r{x}.png'))) for x in range(0, 3)]
        self.walk_left = [(pg.image.load(path.join(sun_wizard_folder, f'l{x}.png'))) for x in range(0, 3)]
        self.walk_top = [(pg.image.load(path.join(sun_wizard_folder, f't{x}.png'))) for x in range(0, 3)]
        self.walk_bot = [(pg.image.load(path.join(sun_wizard_folder, f'b{x}.png'))) for x in range(0, 3)]

class Hunter(Champion):
    def __init__(self, player):
        super(Hunter,self).__init__(player)
        self.walk_right = [(pg.image.load(path.join(hunter_folder, f'r{x}.png'))) for x in range(0, 3)]
        self.walk_left = [(pg.image.load(path.join(hunter_folder, f'l{x}.png'))) for x in range(0, 3)]
        self.walk_top = [(pg.image.load(path.join(hunter_folder, f't{x}.png'))) for x in range(0, 3)]
        self.walk_bot = [(pg.image.load(path.join(hunter_folder, f'b{x}.png'))) for x in range(0, 3)]

    