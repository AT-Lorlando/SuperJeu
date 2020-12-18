from pygame.constants import K_y
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

class MySprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, tile=0):
        self.game = game
        self.x = x
        self.y = y
        self.image = pg.Surface((TILESIZE,TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        self.hp = None

class Floor(MySprite):
    def __init__(self, game, x, y, tile):
        super(Floor,self).__init__(game, x, y, tile)
        self.groups = game.Layers[0]
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = resize(pg.image.load(
            path.join(floor_folder, f'{tile}.png')), TILESIZE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        self.hp = None

class Decoration(MySprite):
    def __init__(self, game, x, y, tile):
        super(Decoration,self).__init__(game, x, y, tile)
        self.groups = game.Layers[1]
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = resize(pg.image.load(
            path.join(deco_folder, f'{tile}.png')), TILESIZE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        self.hp = None


class Wall(MySprite):
    def __init__(self, game, x, y, tile):
        super(Wall,self).__init__(game, x, y, tile)
        self.groups = game.Layers[2], game.obstacle
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

        self.hp = None

class House(MySprite):
    def __init__(self, game, x, y, tile):
        super(House,self).__init__(game, x, y, tile)
        self.groups = game.Layers[3], game.obstacle
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = resize(pg.image.load(
            path.join(house_folder, f'{tile}.png')), 4*TILESIZE, 3*TILESIZE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = (x) * TILESIZE
        self.rect.y = (y) * TILESIZE

        self.hp = 10

class Door(MySprite):
    def __init__(self, game, x, y, tile):
        super(Door,self).__init__(game, x, y, tile)
        self.groups = game.Layers[4], game.obstacle, game.doors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.door_type = 1
        self.instance_behind = (floor(tile %
                                      10000/1000), floor(tile % 1000/100))
        self.image = resize(pg.image.load(
            path.join(portal_folder, 'portal.png')), TILESIZE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = (x) * TILESIZE
        self.rect.y = (y) * TILESIZE
        self.actual_frame = 1
        self.time_since_anime = 0

        self.hp = None

    def turn(self):
        self.time = pg.time.get_ticks()
        if(self.time > self.time_since_anime + 150):
            self.time_since_anime = self.time
            self.image = pg.transform.rotate(self.image, 90)

    def update(self):
        self.turn()


class Stair(MySprite):
    def __init__(self, game, x, y, tile):
        super(Stair,self).__init__(game, x, y, tile)
        self.groups = game.Layers[4], game.obstacle, game.stairs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = resize(pg.image.load(
            path.join(portal_folder, 'portal.png')), TILESIZE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = (x) * TILESIZE
        self.rect.y = (y) * TILESIZE
        self.actual_frame = 1
        self.time_since_anime = 0
        self.portal = [(pg.image.load(
            path.join(portal_folder, f'{i}.png'))) for i in range(1, 4)]

        self.hp = None

    def turn(self):
        self.time = pg.time.get_ticks()
        if(self.time > self.time_since_anime + 150):
            self.time_since_anime = self.time
            self.image = pg.transform.rotate(self.image, 90)

    def update(self):
        self.turn()

class NPC(MySprite):
    def __init__(self, game, x, y, tile):
        super(NPC,self).__init__(game, x, y, tile)
        self.groups = game.Layers[5], game.obstacle
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.img = tile//10
        self.image = resize(pg.image.load(
            path.join(npc_folder, f'{self.img}.png')), CHARACTER_SIZE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = (x) * TILESIZE
        self.rect.y = (y) * TILESIZE

        self.hp = None


class Interactif(MySprite):
    def __init__(self, game, x, y):
        super(Interactif,self).__init__(game, x, y)
        self.groups = game.interactif
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect((x) * TILESIZE, (y) *
                            TILESIZE, TILESIZE*4, TILESIZE)
        self.x = x
        self.y = y

        self.hp = None


class Shop_area(Interactif):
    def __init__(self, game, x, y):
        super(Shop_area, self).__init__(game, x, y)
        self.key = pg.K_e
        self.shop = Screen_shop(game.screen, game)

    def interaction(self, player):
        self.shop.run(self.game.screen.copy(), player)


class Quest_area(Interactif):
    def __init__(self, game, x, y):
        super(Quest_area, self).__init__(game, x, y)
        self.key = pg.K_e

    def interaction(self, player):
        print('Interact')







