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


def resize(img, size):
    return pg.transform.scale(img, (size, size))

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
        self.image = pg.Surface((TILESIZE, TILESIZE))
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
            self.actual_frame = (self.actual_frame + 1) % 3
            self.image = resize(self.portal[self.actual_frame], TILESIZE)

    def update(self):
        self.turn()


class Stair(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.backLayer, game.obstacle, game.stairs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
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
            self.actual_frame = (self.actual_frame + 1) % 3
            self.image = resize(self.portal[self.actual_frame], TILESIZE)

    def update(self):
        self.turn()


class Shoper(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.interactif
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE*2, TILESIZE*3))
        # self.image.fill(ORANGE)
        self.rect = pg.Rect((x) * TILESIZE, (y) * TILESIZE, TILESIZE*2, TILESIZE*3)
        self.key = pg.K_e
        self.x = x
        self.y = y
        self.shop = Screen_shop(game.screen)

    def interaction(self, player):
        self.shop.run(self.game.screen.copy(), player.inv)


class NPC(pg.sprite.Sprite):
    def __init__(self, game, x, y, ID):
        self.groups = game.midLayer
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((CHARACTER_SIZE, CHARACTER_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = (x) * TILESIZE
        self.rect.y = (y) * TILESIZE

class House(pg.sprite.Sprite):
    def __init__(self, game, x, y, ID):
        self.groups = game.midLayer
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((CHARACTER_SIZE, CHARACTER_SIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = (x) * TILESIZE
        self.rect.y = (y) * TILESIZE
        self.shop = Screen_shop(game.screen)

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