from Dungeon import New_Stage
import pygame as pg
from settings import *
from os import kill, path
from Dungeon import *
from inventory_clem import *
from shop import *
from screen_shop import *
from character import *
from sprites import *
import time
vec = pg.math.Vector2

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.Layers[LAYER_NUMBER-1], game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(pg.image.load(path.join(enemy_folder,'idel1.png')),(64,64))

        self.rect = self.image.get_rect()
        self.pos = vec(x,y)* TILESIZE #position of enemy
        self.vel = vec(0,0) #velocity of enemy
        self.rect.center = self.pos
        self.rot = 0 #rotation

        self.health = 5
        self.is_moving = True
        self.visible = True

        self.moveRight = [(pg.image.load(path.join(enemy_folder,f'move{x}.png')).convert_alpha()) for x in range(1,6)]
        self.moveLeft = [pg.transform.flip(img, True, False) for img in self.moveRight]
        


        self.walkCount = 0
        self.maxCount1 = len(self.moveRight)
        self.maxCount2 = len(self.moveLeft)
    
    def set_pos(self, x, y):
        self.pos.x = x
        self.pos.y = y
    
    # COLLISION
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.obstacle, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width / 2
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.rect.width / 2
                self.vel.x = 0
                self.rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.obstacle, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height / 2
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.rect.height / 2
                self.vel.y = 0
                self.rect.centery = self.pos.y 
    
          

    def move(self):
        if (self.pos.x < self.game.player.pos.x and self.is_moving):
            self.image = pg.transform.scale(self.moveRight[self.walkCount], (TILESIZE,TILESIZE))
            self.walkCount = self.walkCount + 1 if self.walkCount <= self.maxCount2 - 2 else 0          
        elif (self.pos.x > self.game.player.pos.x and self.is_moving) :
            self.image = pg.transform.scale(self.moveLeft[self.walkCount], (TILESIZE,TILESIZE))
            self.walkCount = self.walkCount + 1 if self.walkCount <= self.maxCount1 - 2 else 0 
            
        
    def update(self):
        self.move()
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.pos += self.vel * self.game.clock.tick(FPS) / 1000


        #self.collide_with_bullet()
        self.rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.rect.centery = self.pos.y
        self.collide_with_walls('y')