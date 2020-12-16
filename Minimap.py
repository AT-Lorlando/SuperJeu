from pygame.constants import K_RIGHT
from settings import *
from Game import *
import pygame as pg
from math import floor

class Square(pg.sprite.Sprite):
    def __init__(self, minimap, x, y, color, size):
        self.groups = minimap.sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.minimap = minimap
        self.x = minimap.x + x*size
        self.y = minimap.y + y*size
        self.image = pg.Surface((size, size))
        self.image.fill(color)
        self.surface = pg.Rect(self.x, self.y, size, size)

class Minimap():
    def __init__(self, game):
        self.game = game
        self.zoom = 3
        self.square_size = floor(TILESIZE/40)
        self.range = 20
        self.data = []
        self.x = 0
        self.y = 0
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.surface = pg.Rect(self.x, self.y, TILESIZE, TILESIZE)
        self.sprites = pg.sprite.Group()

    def event_zoom(self, y):
        self.zoom = (self.zoom + y)%len(ZOOM_VALUE)
        zoom = ZOOM_VALUE[self.zoom]
        self.square_size = floor(TILESIZE/40 * zoom)
        self.range = floor(20/zoom)
        self.x = WIDTH - (self.range+10)*self.square_size - TILESIZE
        self.y = 10
    
    def data_update(self, data):
        self.data = data
        self.sprites = pg.sprite.Group()
        self.x = (self.range+10)*self.square_size + TILESIZE
        self.y = 10
        self.surface = pg.Rect(self.x, self.y, self.square_size, self.square_size)
        for row, tiles in enumerate(self.data):
            for col, tile in enumerate(tiles):
                if tile%10 == FLOOR_ID:
                    Square(self, col, row, YELLOW, self.square_size)
                elif tile%10 == WALL_ID:
                    Square(self, col, row, BLACK, self.square_size)
                elif tile%10 == STAIR_ID or tile%10 == DOOR_ID:
                    Square(self, col, row, GREEN, self.square_size)
                elif tile%10 == SPAWN_ID:
                    Square(self, col, row, GREEN, self.square_size)
                    
    def draw(self):
        self.data_update(self.data)
        # self.game.screen.blit(self.image, self.surface)
        Square(self, self.Playerpos[0], self.Playerpos[1], RED, self.square_size)
        for sprite in self.sprites:
            self.game.screen.blit(sprite.image, sprite.surface)

    def update(self):
        self.Playerpos = [floor(pos/TILESIZE) for pos in self.game.player.pos]
        # Square(self, Playerpos[0], Playerpos[1], RED, self.square_size)
        # pg.draw.rect(self.game.screen, RED, pg.Rect(self.x + Playerpos[0], self.y + Playerpos[1], self.square_size, self.square_size))
        # self.left = self.Playerpos[0]-self.range if self.Playerpos[0]-self.range>0 else 0
        # self.right = self.Playerpos[0]+self.range if self.Playerpos[0]+self.range<len(self.data[0]) else len(self.data[0])
        # self.top = self.Playerpos[1]-self.range if self.Playerpos[1]-self.range>0 else 0
        # self.bot = self.Playerpos[1]+self.range if self.Playerpos[1]+self.range<len(self.data) else len(self.data)
        # self.sprites.update()