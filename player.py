from Dungeon import New_Stage
import pygame as pg
from settings import *
from os import path
from Dungeon import *
from inventory_clem import *
from shop import *
from screen_shop import *
from sprites import *
from character import *
import time
vec = pg.math.Vector2


def resize(img, size):
    return pg.transform.scale(img, (size, size))


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.Layers[LAYER_NUMBER-1]
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((CHARACTER_SIZE, CHARACTER_SIZE))
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.playerpos = ([floor(pos/TILESIZE) for pos in self.pos])
        self.isPlaying = False
        self.explode = [
            (pg.image.load(path.join(explode_folder, f'f ({x}).gif'))) for x in range(1, 23)]

        self.inv = Inventory()
        self.inv.add_without_case(Axe)

        self.stuff = Inventory("stuff", 5)

        self.level = 1
        self.xp = 100
        self.xp_max = 200
        self.hp = 100
        self.hp_max = 200
        self.champion_pool = []
        self.champion_pool.append(Dark_Wizard(self))
        self.champion_pool.append(Sun_Wizard(self))
        self.champion_pool.append(Hunter(self))
        self.main_champ = self.champion_pool[0]

        self.money = 1000

        self.quest_list = []
        self.finished_quest = []

        self.looking_at = 'Bot'
        self.is_moving = False

        self.pause = 0
        self.time_since_last_spell = 0

    def gain_xp(self, amount):
        self.xp += amount

    def gain_money(self, amount):
        self.money += amount
        

    def set_pos(self, x, y):
        self.pos.x = x
        self.pos.y = y

    def add_to_pool(self, champion):
        self.champion_pool.append(champion)

    def get_keys(self):
        if(self.isPlaying):
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT]:
                if keys[pg.K_RIGHT]:
                    self.vel.x = 0
                    self.is_moving = False
                else:
                    self.looking_at = 'Left'
                    self.vel.x = -PLAYER_SPEED
                    self.is_moving = True
            elif keys[pg.K_RIGHT]:
                self.looking_at = 'Right'
                self.vel.x = PLAYER_SPEED
                self.is_moving = True
            elif self.vel.x != 0:
                self.vel.x *= 0.8
            if keys[pg.K_UP]:
                if keys[pg.K_DOWN]:
                    self.vel.y = 0
                    if keys[pg.K_LEFT] or keys[pg.K_RIGHT]:
                        self.is_moving = True
                    else:
                        self.is_moving = False
                else:
                    self.looking_at = 'Top'
                    self.vel.y = -PLAYER_SPEED
                    self.is_moving = True
            elif keys[pg.K_DOWN]:
                self.looking_at = 'Bot'
                self.vel.y = PLAYER_SPEED
                self.is_moving = True
            elif self.vel.y != 0:
                self.vel.y *= 0.8

            if(self.is_moving):
                if -10 < self.vel.x < 10:
                    self.vel.x = 0

                if -10 < self.vel.y < 10:
                    self.vel.y = 0

            if self.vel.x != 0 and self.vel.y != 0:
                self.vel *= 0.7071
            if keys[pg.K_0]:
                for quest in self.quest_list:
                    print(quest.goal)
            if keys[pg.K_8]:
                self.hp -= 1 if self.hp > 0 else 0
                print(self.hp)
            if keys[pg.K_9]:
                self.hp += 1 if self.hp < self.hp_max else 0
                print(self.hp)
            if keys[pg.K_6]:
                self.xp -= 1 if self.xp > 0 else 0
                print(self.xp)
            if keys[pg.K_7]:
                self.xp += 1 if self.xp < self.xp_max else 0
                print(self.xp)
                # for sprite in self.game.frontLayer:
                #     print(sprite)
                # print((self.pos[0], self.pos[1]))
                # print(self.game.camera.apply(self))
                # print(self.rect)
                # print(self.main_champ)
            elif keys[pg.K_1]:
                self.switch(0)
            elif keys[pg.K_2]:
                self.switch(1)
            elif keys[pg.K_3]:
                self.switch(2)
            elif keys[pg.K_a]:
                self.use_spell(0)

    def use_spell(self, spell):
        now = pg.time.get_ticks()
        if now - self.time_since_last_spell > 250:
            self.time_since_last_spell = now
            Fireball(self)
            print("FIRE")

    def switch(self, x):
        self.vel = vec(0, 0)
        self.isPlaying = False
        self.main_champ = self.champion_pool[x]
        self.main_champ.animation()
        self.image = self.main_champ.image
        pg.display.update()
        bg = self.game.screen.copy()
        for img in self.explode[:len(self.explode)//2]:
            self.game.screen.blit(bg, (0, 0))
            self.game.screen.blit(pg.transform.scale(
                img, (150, 150)), (WIDTH/2 - CHARACTER_SIZE+10, (HEIGHT)/2 - CHARACTER_SIZE-15, 90, 100))
            pg.display.flip()
            self.game.dt_update()
            time.sleep(.01)
        self.game.draw()
        bg = self.game.screen.copy()
        for img in self.explode[len(self.explode)-len(self.explode)//2:]:
            self.game.screen.blit(bg, (0, 0))
            self.game.screen.blit(pg.transform.scale(
                img, (150, 150)), (WIDTH/2 - CHARACTER_SIZE+10, (HEIGHT)/2 - CHARACTER_SIZE-15, 90, 100))
            pg.display.flip()
            self.game.dt_update()
            time.sleep(.01)
        self.isPlaying = True
        self.rect = self.image.get_rect()

    def collide_with_obstacle(self, dir):
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

    def collide_with_interactif(self):
        self.time = pg.time.get_ticks()
        if(self.time > self.pause + 250):
            self.pause = self.time
            hits = pg.sprite.spritecollide(self, self.game.interactif, False)

            if hits:
                self.game.interactif_dialogue(hits[0])
            else:
                self.game.interactif_dialogue(None)

    def collide_interaction(self, sprite):
        if sprite in self.game.doors:
            self.vel = vec(0, 0)
            self.isPlaying = False
            self.passing_door(sprite)
        elif sprite in self.game.stairs:
            self.vel = vec(0, 0)
            self.isPlaying = False
            self.go_upstair()

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
        if(self.isPlaying):
            self.get_keys()
            self.pos += self.vel * self.game.dt
            self.rect.x = self.pos.x
            self.collide_with_obstacle('x')
            self.rect.y = self.pos.y
            self.collide_with_obstacle('y')
            self.collide_with_interactif()
            self.playerpos = [floor(pos/TILESIZE) for pos in self.pos]
        if(self.vel == (0, 0)):
            self.is_moving = False
