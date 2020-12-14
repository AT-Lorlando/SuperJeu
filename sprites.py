from pygame.constants import K_y
from Dungeon import New_Stage
import pygame as pg
from settings import *
from os import path
from Dungeon import *
from inventory_clem import *
from shop import *
from screen_shop import *
vec = pg.math.Vector2


def resize(img, size, y=0):
    return pg.transform.scale(img, (size, y)) if y else pg.transform.scale(img, (size, size))

class Floor(pg.sprite.Sprite):
    def __init__(self, game, x, y, tile):
        self.groups = game.backLayer
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = resize(pg.image.load(
            path.join(floor_folder, f'{tile}.png')), TILESIZE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, tile):
        self.groups = game.backLayer, game.obstacle, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        if(tile):
            self.image = resize(pg.image.load(
                path.join(wall_folder, f'{tile}.png')), TILESIZE)
        else:
            self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y, door_type, instance_behind):
        self.groups = game.backLayer, game.obstacle, game.doors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.door_type = door_type
        self.instance_behind = (floor(instance_behind %
                                      10000/1000), floor(instance_behind % 1000/100))
        self.image = resize(pg.image.load(path.join(portal_folder, 'portal.png')), TILESIZE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = (x) * TILESIZE
        self.rect.y = (y) * TILESIZE
        self.actual_frame = 1
        self.time_since_anime = 0
        

    def turn(self):
        self.time = pg.time.get_ticks()
        if(self.time > self.time_since_anime + 150):
            self.time_since_anime = self.time
            self.image = pg.transform.rotate(self.image,90)
            

    def update(self):
        self.turn()


class Stair(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.backLayer, game.obstacle, game.stairs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = resize(pg.image.load(path.join(portal_folder, 'portal.png')), TILESIZE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = (x) * TILESIZE
        self.rect.y = (y) * TILESIZE
        self.actual_frame = 1
        self.time_since_anime = 0
        self.portal = [(pg.image.load(
            path.join(portal_folder, f'{i}.png'))) for i in range(1, 4)]

    def turn(self):
            self.time = pg.time.get_ticks()
            if(self.time > self.time_since_anime + 150):
                self.time_since_anime = self.time
                self.image = pg.transform.rotate(self.image,90)

    def update(self):
        self.turn()


class Interactif(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.interactif
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect((x) * TILESIZE, (y) * TILESIZE, TILESIZE*4, TILESIZE)
        self.x = x
        self.y = y
class Shop_area(Interactif):
    def __init__(self, game, x, y):
        super(Shop_area,self).__init__(game, x, y)
        self.key = pg.K_e
        self.shop = Screen_shop(game.screen)

    def interaction(self, player):
        self.shop.run(self.game.screen.copy(), player.inv)

class Quest_area(Interactif):
    def __init__(self, game, x, y):
        super(Quest_area,self).__init__(game, x, y)
        self.key = pg.K_e

    def interaction(self, player):
        print('Interact')


class NPC(pg.sprite.Sprite):
    def __init__(self, game, x, y, tile):
        self.groups = game.midLayer, game.obstacle
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.img = tile//10
        self.image = resize(pg.image.load(
            path.join(npc_folder, f'{self.img}.png')),CHARACTER_SIZE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = (x) * TILESIZE
        self.rect.y = (y) * TILESIZE

class House(pg.sprite.Sprite):
    def __init__(self, game, x, y, tile):
        self.groups = game.midLayer, game.obstacle
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = resize(pg.image.load(
            path.join(house_folder, f'{tile}.png')),4*TILESIZE,3*TILESIZE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = (x) * TILESIZE
        self.rect.y = (y) * TILESIZE

class Decoration(pg.sprite.Sprite):
    def __init__(self, game, x, y, tile):
        self.groups = game.backLayer
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = resize(pg.image.load(
            path.join(deco_folder, f'{tile}.png')), TILESIZE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE