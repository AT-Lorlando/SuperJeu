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
from bullets import *
import time
vec = pg.math.Vector2


def resize(img, size):
    return pg.transform.scale(img, (size+2, size+2))

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.frontLayer.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(path.join(dark_wizard_folder,'b0.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.playerpos = ([floor(pos/TILESIZE) for pos in self.pos])
        self.isPlaying = False
        self.explode = [(pg.image.load(path.join(explode_folder, f'f ({x}).gif'))) for x in range(1, 23)]

        self.inv = Inventory()
        self.inv.add(Sword("sprite1"))
        self.inv.add(Sword("sprite2"))
        self.inv.add(Sword("sprite3"))
        self.level = 1
        self.champion_pool = []
        self.champion_pool.append(Dark_Wizard(self))
        self.champion_pool.append(Sun_Wizard(self))
        self.champion_pool.append(Hunter(self))
        self.main_champ = self.champion_pool[0]

        self.looking_at = 'Bot'
        self.is_moving = False
        self.health = 100
        self.last_shot =0

    def set_pos(self, x, y):
        self.pos.x = x
        self.pos.y = y

    def add_to_pool(self, champion):
        self.champion_pool.add(champion)

    def attacking(self):
        img_rot=-90
        dir =vec(1,0).rotate(90)
        keys = pg.key.get_pressed()
        self.time = pg.time.get_ticks() #get the time in milliseconds
        if self.time - self.last_shot > BULLET_RATE:
            self.last_shot = self.time

            #ROTATION OF BULLETS
            if self.looking_at == 'Right': 
                img_rot = 0
                dir = vec(1,0).rotate(0)   
            if self.looking_at == 'Left':
                img_rot = 180
                dir = vec(1,0).rotate(180)                   
            if self.looking_at == 'Bot':
                img_rot = -90
                dir = vec(1,0).rotate(90)
            if self.looking_at == 'Top':
                img_rot = 90
                dir = vec(1,0).rotate(-90)
            if keys[pg.K_UP] and keys[pg.K_RIGHT]:
                img_rot = 45
                dir = vec(1,0).rotate(-45)
            if keys[pg.K_UP] and keys[pg.K_LEFT]:
                img_rot = 135
                dir = vec(1,0).rotate(-135)
            if keys[pg.K_DOWN] and keys[pg.K_RIGHT]:
                img_rot = -45
                dir = vec(1,0).rotate(45)
            if keys[pg.K_DOWN] and keys[pg.K_LEFT]:
                img_rot = -135
                dir = vec(1,0).rotate(135)    
            Bullet(self.game, (self.pos.x + 32, self.pos.y + 32), dir, img_rot) 

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.is_moving = False
            else:
                self.looking_at = 'Left'
                self.vel.x = -PLAYER_SPEED
                self.is_moving = True
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.looking_at = 'Right'
            self.vel.x = PLAYER_SPEED
            self.is_moving = True
        if keys[pg.K_UP] or keys[pg.K_w]:
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.is_moving = False
            else:
                self.looking_at = 'Top'
                self.vel.y = -PLAYER_SPEED
                self.is_moving = True
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.looking_at = 'Bot'
            self.vel.y = PLAYER_SPEED
            self.is_moving = True
        if keys[pg.K_SPACE] :
            self.attacking()
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        if keys[pg.K_0]:
            print((self.pos[0],self.pos[1]))
            print(self.game.camera.apply(self))
            print(self.rect)
            # print(self.main_champ)
        elif keys[pg.K_1]:
            self.switch(0)
        elif keys[pg.K_2]:
            self.switch(1)
        elif keys[pg.K_3]:
            self.switch(2)

    def switch(self, x):
        self.vel = vec(0, 0)
        self.isPlaying = False
        self.main_champ = self.champion_pool[x]
        bg = self.game.screen.copy()
        for img in self.explode:
            self.game.screen.blit(bg,(0,0))
            self.game.screen.blit(pg.transform.scale(img,(150,150)), (WIDTH/2 - 50, HEIGHT/2 - 85, 100, 100))
            pg.display.flip()
            time.sleep(.02)
        self.isPlaying = True

    def collide_with_obstacle(self, dir):
        # self.game.interactif_dialogue(0)

        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.obstacle, False)
            if hits:
                self.collide_interaction(hits[0])
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        elif dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.obstacle, False)
            if hits:
                self.collide_interaction(hits[0])
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def collide_interaction(self, sprite):
        if sprite in self.game.doors:
            self.vel = vec(0, 0)
            self.isPlaying = False
            self.passing_door(sprite)
        elif sprite in self.game.stairs:
            self.vel = vec(0, 0)
            self.isPlaying = False
            self.go_upstair()
        elif isinstance(sprite, Shoper):
            self.game.interactif_dialogue(sprite)
            sprite.shop.run(self.game.screen.copy(), self.inv)
        else:
            self.game.interactif_dialogue(0)

    def passing_door(self, door):
        self.game.known_tiles = []
        if(door.door_type > 0):  # Door linked to a dungeon
            self.game.load_dungeon(
                door.instance_behind[0], door.instance_behind[1])
            self.game.actual_stage += 1
            self.game.draw_instance(
                self.game.actual_dungeon.stage_tab[self.game.actual_stage-1])
        else:  # Door linked to menu
            self.game.actual_stage = 0
            self.game.draw_instance(self.game.hub)

    def go_upstair(self):
        assert(self.game.actual_dungeon)
        self.game.known_tiles = []
        self.game.actual_stage += 1
        self.game.draw_instance(
            self.game.actual_dungeon.stage_tab[self.game.actual_stage-1])

    def update(self):
        self.main_champ.animation()
        self.image = self.main_champ.image
        hits = pg.sprite.spritecollide(self, self.game.obstacle, False)
        self.collide_interaction(hits)
        if(self.isPlaying):
            self.get_keys()
            self.pos += 2*self.vel * self.game.clock.tick(FPS) / 1000
            self.rect.x = self.pos.x
            self.collide_with_obstacle('x')
            self.rect.y = self.pos.y
            self.collide_with_obstacle('y')
            self.playerpos = [floor(pos/TILESIZE) for pos in self.pos]
        if(self.vel == (0, 0)):
            self.is_moving = False