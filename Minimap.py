from settings import *
from Game import *
import pygame as pg
from math import floor

class Minimap():
    def __init__(self, game):
        self.game = game
        self.size = floor(TILESIZE/40)
        self.data = []
        self.zoom = 0
        self.x = 0
        self.y = 0
        
    def draw(self, data, known_data):
        self.x = 10 * TILESIZE - len(self.data)*self.size
        self.y = 0
        thisPlayerXpos = floor(self.game.player.pos[0]/TILESIZE)
        thisPlayerYpos = floor(self.game.player.pos[1]/TILESIZE)
        thisXRange = 25
        thisYRange = 25
        if(thisPlayerXpos<thisXRange):
            thisXRange-=(thisXRange-thisPlayerXpos)
        if(thisPlayerYpos<thisYRange):
            thisYRange-=(thisYRange-thisPlayerYpos)
        for row, tiles in enumerate(data[thisPlayerYpos-thisYRange:thisPlayerYpos+thisYRange]):
            for col, tile in enumerate(tiles[thisPlayerXpos-thisXRange:thisPlayerXpos+thisXRange]):
                if(floor(tile/10) in known_data):
                    if tile%10 == SPAWN_ID:
                        pg.draw.rect(self.game.screen, ORANGE, pg.Rect(
                            self.y+((self.size+1)*col), self.x+((self.size+1)*row), self.size, self.size))
                    elif tile%10 == FLOOR_ID:
                        pg.draw.rect(self.game.screen, YELLOW, pg.Rect(
                            self.x+((self.size+1)*col), self.y+((self.size+1)*row), self.size, self.size))
                    elif tile%10 == WALL_ID:
                        pg.draw.rect(self.game.screen, BLACK, pg.Rect(
                            self.x+((self.size+1)*col), self.y+((self.size+1)*row), self.size, self.size))
                    if (row == thisYRange and col == thisXRange):
                        pg.draw.rect(self.game.screen, RED, pg.Rect(
                            self.x+((self.size+1)*col), self.y+((self.size+1)*row), self.size, self.size))