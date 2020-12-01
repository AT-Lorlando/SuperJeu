from pygame.constants import K_RIGHT
from settings import *
from Game import *
import pygame as pg
from math import floor

class Minimap():
    def __init__(self, game):
        self.game = game
        self.zoom = 3
        self.size = floor(TILESIZE/40)
        self.range = 20
        self.data = []
        self.x = 0
        self.y = 0    

    def event_zoom(self, y):
        self.zoom = (self.zoom + y)%len(ZOOM_VALUE)
        zoom = ZOOM_VALUE[self.zoom]
        self.size = floor(TILESIZE/40 * zoom)
        self.x = WIDTH - len(self.data)*self.size - 2 * TILESIZE
        self.y = 10
    
    def data_update(self, data):
        self.data = data
        self.x = WIDTH - len(self.data)*self.size - 2 * TILESIZE
        self.y = 10

    def draw(self, data, known_data):
        thisPlayerpos = [floor(pos/TILESIZE) for pos in self.game.player.pos]
        left = thisPlayerpos[0]-self.range if thisPlayerpos[0]-self.range>0 else 0
        right = thisPlayerpos[0]+self.range if thisPlayerpos[0]+self.range<len(data[0]) else len(data[0])
        top = thisPlayerpos[1]-self.range if thisPlayerpos[1]-self.range>0 else 0
        bot = thisPlayerpos[1]+self.range if thisPlayerpos[1]+self.range<len(data) else len(data)
        for row, tiles in enumerate(data[top:bot]):
            for col, tile in enumerate(tiles[left:right]):
                if(floor(tile/10) in known_data):
                    if tile%10 == FLOOR_ID:
                        pg.draw.rect(self.game.screen, YELLOW, pg.Rect(
                            self.x+((self.size)*col), self.y+((self.size)*row), self.size, self.size))
                    elif tile%10 == WALL_ID:
                        pg.draw.rect(self.game.screen, BLACK, pg.Rect(
                            self.x+((self.size)*col), self.y+((self.size)*row), self.size, self.size))
                    elif tile%10 == STAIR_ID or tile%10 == DOOR_ID:
                        pg.draw.rect(self.game.screen, GREEN, pg.Rect(
                            self.x+((self.size)*col), self.y+((self.size)*row), self.size, self.size))
                    elif tile%10 == SPAWN_ID:
                        pg.draw.rect(self.game.screen, ORANGE, pg.Rect(
                            self.x+((self.size)*col), self.y+((self.size)*row), self.size, self.size))
                pg.draw.rect(self.game.screen, RED, pg.Rect(
                    self.x+(self.size*(thisPlayerpos[0]-left)), self.y+(self.size*(thisPlayerpos[1]-top)), self.size, self.size))