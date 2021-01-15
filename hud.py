import pygame as pg
from settings import *
from os import path

class HUD:
    def __init__(self, x, y, player):
        self.player = player
        self.x = x
        self.y = y
    
    def update(self):
        pass

    def draw(self, game):
        self.update()
        game.screen.blit(self.image, (self.x, self.y))

class Life_HUD(HUD):
    def __init__(self, x, y, player):
        super(Life_HUD,self).__init__(x, y, player)
        self.source_image = resize(pg.image.load(path.join(assets_folder, f'life.png')), 200,200)
        self.image_rect = self.source_image.get_rect()
        self.image = self.source_image.subsurface(self.image_rect)
        self.image_rect.height = 20

    def update(self):
        self.image_rect.width = 200 * (self.player.hp/self.player.hp_max)
        self.image_rect.y = 180 * (self.player.hp/self.player.hp_max)
        self.image = self.source_image.subsurface(self.image_rect)

class Exp_HUD(HUD):
    def __init__(self, x, y, player):
        super(Exp_HUD,self).__init__(x, y, player)
        self.source_image = resize(pg.image.load(path.join(assets_folder, f'life.png')), 200,200)
        self.image_rect = self.source_image.get_rect()
        self.image = self.source_image.subsurface(self.image_rect)
        self.image_rect.height = 20

    def update(self):
        self.image_rect.width = 200 * (self.player.xp/self.player.xp_max)
        self.image_rect.y = 180 * (self.player.xp/self.player.xp_max)
        self.image = self.source_image.subsurface(self.image_rect)

class Character_HUD(HUD):
    def __init__(self, x, y, player):
        super(Character_HUD,self).__init__(x, y, player)
        self.source_image = resize(self.player.main_champ.walk_bot[0], HEIGHT//15,HEIGHT//15)
        self.image_rect = self.source_image.get_rect()
        self.image_rect.x = 5
        self.image_rect.y = 0
        self.image_rect.width = HEIGHT//16
        self.image_rect.height = HEIGHT//17
        self.image = self.source_image.subsurface(self.image_rect)
        
    def update(self):
        self.source_image = resize(self.player.main_champ.walk_bot[0], HEIGHT//15,HEIGHT//15)
        self.image = self.source_image.subsurface(self.image_rect)

class Life_Data_HUD(HUD):
    def __init__(self, x, y, player):
        super(Life_Data_HUD,self).__init__(x, y, player)
        self.image = text_to_screen(f'{self.player.hp}/{self.player.hp_max}')

    def update(self):
        self.image = text_to_screen(f'{self.player.hp}/{self.player.hp_max}', color=(255*(1-self.player.hp/self.player.hp_max),255*self.player.hp/self.player.hp_max,0), l = 40)
        self.outline = text_to_screen(f'{self.player.hp}/{self.player.hp_max}', color=(255,255,255), l = 40)

    def draw(self, game):
        self.update()
        game.screen.blit(self.outline, (self.x-1, self.y-1))
        game.screen.blit(self.outline, (self.x-1, self.y+1))
        game.screen.blit(self.outline, (self.x+1, self.y-1))
        game.screen.blit(self.outline, (self.x+1, self.y+1))
        game.screen.blit(self.image, (self.x, self.y))

class Exp_Data_HUD(HUD):
    def __init__(self, x, y, player):
        super(Exp_Data_HUD,self).__init__(x, y, player)
        self.image = text_to_screen(f'{self.player.xp}/{self.player.xp_max}')

    def update(self):
        self.image = text_to_screen(f'{self.player.xp}/{self.player.xp_max}', color=(50,50,255*(self.player.xp/self.player.xp_max)), l = 40)
        self.outline = text_to_screen(f'{self.player.xp}/{self.player.xp_max}', color=(255,255,255), l = 40)

    def draw(self, game):
        self.update()
        game.screen.blit(self.outline, (self.x-1, self.y-1))
        game.screen.blit(self.outline, (self.x-1, self.y+1))
        game.screen.blit(self.outline, (self.x+1, self.y-1))
        game.screen.blit(self.outline, (self.x+1, self.y+1))
        game.screen.blit(self.image, (self.x, self.y))
