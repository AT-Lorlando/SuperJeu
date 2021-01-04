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
        self.groups = game.frontLayer.all_sprites ,game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))

        self.rect = self.image.get_rect()
        self.pos = vec(x,y)* TILESIZE #position of enemy
        self.vel = vec(0,0) #velocity of enemy
        self.rect.center = self.pos
        self.rot = 0 #rotation

        self.health = 5
        self.is_moving = True
        self.visible = True

        self.moveRight = [(pg.image.load(path.join(sprite_folder,f'R{x}E.png')).convert_alpha()) for x in range(1,9)]
        self.moveLeft = [(pg.image.load(path.join(sprite_folder,f'L{x}E.png')).convert_alpha()) for x in range(1,9)]
        """ self.attackLeft = [(pg.image.load(path.join(sprite_folder,'goblin',f'attack{x}L.png')).convert_alpha()) for x in range(1,7)]
        self.attackRight = [(pg.image.load(path.join(sprite_folder,'goblin',f'attack{x}R.png')).convert_alpha()) for x in range(1,7)] """


        self.walkCount = 0
        self.maxCount1 = len(self.moveRight)
        self.maxCount2 = len(self.moveLeft)
    
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
  
    def collide_with_bullet(self):
        hited = pg.sprite.spritecollide(self, self.game.bullets, True)
        for hit in hited:
            if self.health > 0:
                self.health -=1
            else:
                self.visible = False
                self.kill()
        
          

    def move(self):
        if (self.pos.x < self.game.player.pos.x and self.is_moving):
            self.image = pg.transform.(self.moveRight[self.walkCount], (TILESIZE,TILESIZE))
            self.walkCount = self.walkCount + 1 if self.walkCount <= self.maxCount2 - 2 else 0          
        elif (self.pos.x > self.game.player.pos.x and self.is_moving) :
            self.image = pg.transform.(self.moveLeft[self.walkCount], (TILESIZE,TILESIZE))
            self.walkCount = self.walkCount + 1 if self.walkCount <= self.maxCount1 - 2 else 0 
            
        
    def update(self):
        self.move()
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.acc = vec(ENEMY_SPEED, 0).rotate(-self.rot) #acceleration
        self.acc += -self.vel  
        self.vel += self.acc * self.game.clock.tick(FPS) / 1000
        self.pos += self.vel * self.game.clock.tick(FPS) / 1000

        self.collide_with_bullet()
        self.rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.rect.centery = self.pos.y
        self.collide_with_walls('y')