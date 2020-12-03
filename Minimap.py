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
        self.x = WIDTH - (self.range+10)*self.square_size - TILESIZE
        self.y = 10
        self.surface = pg.Rect(self.x, self.y, self.square_size, self.square_size)

    def draw(self):
        self.game.screen.blit(self.image, self.surface)
        for sprite in self.sprites:
            self.game.screen.blit(sprite.image, sprite.surface)
            #print('Draw', sprite.x)

    def update(self, known_data):
        thisPlayerpos = [floor(pos/TILESIZE) for pos in self.game.player.pos]
        left = thisPlayerpos[0]-self.range if thisPlayerpos[0]-self.range>0 else 0
        right = thisPlayerpos[0]+self.range if thisPlayerpos[0]+self.range<len(self.data[0]) else len(self.data[0])
        top = thisPlayerpos[1]-self.range if thisPlayerpos[1]-self.range>0 else 0
        bot = thisPlayerpos[1]+self.range if thisPlayerpos[1]+self.range<len(self.data) else len(self.data)
        # for row, tiles in enumerate(self.data[top:bot]):
        #     for col, tile in enumerate(tiles[left:right]):
        for row, tiles in enumerate(self.data[top:bot]):
            for col, tile in enumerate(tiles[left:right]):
                if(floor(tile/10) in known_data):
                    if tile%10 == FLOOR_ID:
                        Square(self, col+left, row+top, YELLOW, self.square_size)
                        #pg.draw.rect(self.game.screen, YELLOW, self.square_size, pg.Rect(
                        #    self.x+((self.square_size)*col), self.y+((self.square_size)*row), self.square_size, self.square_size))
                    elif tile%10 == WALL_ID:
                        Square(self, col+left, row+top, BLACK, self.square_size)
                        #pg.draw.rect(self.game.screen, BLACK, pg.Rect(
                        #    self.x+((self.square_size)*col), self.y+((self.square_size)*row), self.square_size, self.square_size))
                    elif tile%10 == STAIR_ID or tile%10 == DOOR_ID:
                        Square(self, col+left, row+top, GREEN, self.square_size)
                        #pg.draw.rect(self.game.screen, GREEN, pg.Rect(
                        #    self.x+((self.square_size)*col), self.y+((self.square_size)*row), self.square_size, self.square_size))
                    elif tile%10 == SPAWN_ID:
                        Square(self, col+left, row+top, GREEN, self.square_size)
                        #pg.draw.rect(self.game.screen, ORANGE, pg.Rect(
                        #    self.x+((self.square_size)*col), self.y+((self.square_size)*row), self.square_size, self.square_size))
                pg.draw.rect(self.game.screen, RED, pg.Rect(
                    self.x+(self.square_size*(thisPlayerpos[0]-left)), self.y+(self.square_size*(thisPlayerpos[1]-top)), self.square_size, self.square_size))
        self.sprites.update()