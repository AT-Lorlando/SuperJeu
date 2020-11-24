import pygame 
from settings import *
from random import uniform


vec = pygame.math.Vector2 #vector

# COLLISION
def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width / 2
            if sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right + sprite.rect.width / 2
            sprite.vel.x = 0
            sprite.rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height / 2
            if sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom + sprite.rect.height / 2
            sprite.vel.y = 0
            sprite.rect.centery = sprite.pos.y

#PLAYER
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.transform.scale(game.player_img, (48, 48))
        self.rect = self.image.get_rect()
        self.vel = vec(0,0) # velociy
        self.pos = vec(x,y) * TILESIZE #position

        self.left = False
        self.right = False
        self.up = False
        self.down = False

        self.walkCount = 0
        self.maxCount1 = len(game.player_img_left)
        self.maxCount2 = len(game.player_img_right)
        self.maxCount3 = len(game.player_img_up)
        self.maxCount4 = len(game.player_img_down)

        self.heal = 100
        self.last_shot =0
     
    
    def get_keys(self):
        self.vel = vec(0,0)
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_UP] :
            self.vel.y = -PLAYER_SPEED
            self.left = False
            self.right = False
            self.up = True
            self.down = False
            self.image = pygame.transform.scale(self.game.player_img_up[self.walkCount], (48,48))
            self.walkCount = self.walkCount + 1 if self.walkCount <= self.maxCount3 - 2 else 0       
            
        if keys[pygame.K_DOWN] :
            self.vel.y = PLAYER_SPEED
            self.left = False
            self.right = False
            self.up = False
            self.down = True
            self.image = pygame.transform.scale(self.game.player_img_down[self.walkCount], (48,48))
            self.walkCount = self.walkCount + 1 if self.walkCount <= self.maxCount4 - 2 else 0 

        if keys[pygame.K_LEFT] :
            self.vel.x = -PLAYER_SPEED
            self.left = True
            self.right =False
            self.up = False
            self.down = False
            self.image = pygame.transform.scale(self.game.player_img_left[self.walkCount], (48,48))
            self.walkCount = self.walkCount + 1 if self.walkCount <= self.maxCount1 - 2 else 0

        if keys[pygame.K_RIGHT] :
            self.vel.x = PLAYER_SPEED
            self.left = False
            self.right = True
            self.up = False
            self.down = False
            self.image = pygame.transform.scale(self.game.player_img_right[self.walkCount], (48,48))
            self.walkCount = self.walkCount +1 if self.walkCount <= self.maxCount2 -2 else 0

        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

        img_rot=-90
        dir =vec(1,0).rotate(90)
        if keys[pygame.K_SPACE]:
         
            now = pygame.time.get_ticks() #get the time in milliseconds
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now

                #ROTATION OF BULLETS
                if self.right == True: 
                    img_rot = 0
                    dir = vec(1,0).rotate(0)    
                if self.left == True:
                    img_rot = 180
                    dir = vec(1,0).rotate(180)                   
                if self.down == True:
                    img_rot = -90
                    dir = vec(1,0).rotate(90)
                if self.up == True:
                    img_rot = 90
                    dir = vec(1,0).rotate(-90)
                if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                    img_rot = 45
                    dir = vec(1,0).rotate(-45)
                if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                    img_rot = 135
                    dir = vec(1,0).rotate(-135)
                if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
                    img_rot = -45
                    dir = vec(1,0).rotate(45)
                if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
                    img_rot = -135
                    dir = vec(1,0).rotate(135)
                
                Bullet(self.game, self.pos, dir, img_rot)
            

    def update(self):
        self.get_keys()
        self.pos += self.vel* self.game.dt
        self.rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')

#ENEMY
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.transform.scale(game.enemy_img, (TILESIZE*2, TILESIZE*2))

        self.rect = self.image.get_rect()
        self.pos = vec(x,y)* TILESIZE #position of enemy
        self.vel = vec(0,0) #velocity of enemy
        self.rect.center = self.pos
        self.rot = 0 #rotation
        self.heal = 100

        self.walkCount = 0
        self.maxCount1 = len(game.enemy_img_left)
        self.maxCount2 = len(game.enemy_img_right)
       
   
    def move(self):
        if self.pos.x < self.game.player.pos.x:
            self.image = pygame.transform.scale(self.game.enemy_img_right[self.walkCount], (TILESIZE*2,TILESIZE*2))
            self.walkCount = self.walkCount + 1 if self.walkCount <= self.maxCount2 - 2 else 0               
        else:
            self.image = pygame.transform.scale(self.game.enemy_img_left[self.walkCount], (TILESIZE*2,TILESIZE*2))
            self.walkCount = self.walkCount + 1 if self.walkCount <= self.maxCount1 - 2 else 0 
        
    def update(self):
        self.move()
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.acc = vec(ENEMY_SPEED, 0).rotate(-self.rot) #acceleration
        self.acc += -self.vel  
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt

        self.rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
         

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, pos, dir, img_rot=0):
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = pygame.transform.scale(game.bullet_img, (8, 8))
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center =pos

        spread = uniform (-GUN_SPREAD,GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawm_time = pygame.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pygame.sprite.spritecollideany(self, self.game.walls):
            self.kill() #remove the sprite. 
        if pygame.time.get_ticks() - self.spawm_time > BULLET_LIFETIME:
            self.kill()

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type_img):
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game  

        self.x = x
        self.y = y
        
        if type_img == 1:
            self.image = pygame.transform.scale(game.wall_img1, (TILESIZE, TILESIZE))
        if type_img == 2:
            self.image = pygame.transform.scale(game.wall_img2, (43, 65))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE  



        
       