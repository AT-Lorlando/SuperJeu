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
from random import uniform
import math
vec = pg.math.Vector2

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos,des):
        self.groups = game.frontLayer.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = pg.transform.scale(pg.image.load(path.join(bullet_forder,'fire.png')),(32,32))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.des = des
        self.rect.center =pos

        distance = math.hypot(des[0] - WIDTH//2,des[1] - HEIGHT//2)
        if des[0] - WIDTH//2 > 0:
            img_rot = math.asin((des[1] - HEIGHT//2)/distance)*180/math.pi
        else: 
            img_rot = 180 - math.asin((des[1] - HEIGHT//2)/distance)*180/math.pi
        dir = vec(1,0).rotate(img_rot)

        #spread = uniform(-GUN_SPREAD,GUN_SPREAD)
        self.vel = dir * BULLET_SPEED
        self.spawm_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill() #remove the sprite. 
        if pg.time.get_ticks() - self.spawm_time > BULLET_LIFETIME:
            self.kill()
