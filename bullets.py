from Dungeon import New_Stage
import pygame as pg
from settings import *
from os import path
from Dungeon import *
from inventory_clem import *
from shop import *
from screen_shop import *
from character import *
from sprites import *
import time
from random import uniform
vec = pg.math.Vector2

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, img_rot=0):
        self.groups = game.frontLayer.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = pg.transform.scale(pg.image.load(path.join(bullet_forder,'fire.png')),(32,32))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center =pos


        spread = uniform (-GUN_SPREAD,GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawm_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill() #remove the sprite. 
        if pg.time.get_ticks() - self.spawm_time > BULLET_LIFETIME:
            self.kill()