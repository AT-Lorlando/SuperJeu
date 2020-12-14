from pygame.constants import MOUSEWHEEL
from settings import *
from Game import *
import pygame as pg
from math import floor
from Mother_screen import *

class Square(pg.sprite.Sprite):
    def __init__(self, map_hud, x, y, color, size):
        self.groups = map_hud.sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.map_hud = map_hud
        self.x = map_hud.x + x*size
        self.y = map_hud.y + y*size
        self.image = pg.Surface((size, size))
        self.image.fill(color)
        self.surface = pg.Rect(self.x, self.y, size, size)

class Map(Mother_screen):
    def __init__(self, game):
        super(Map, self).__init__()
        self.game = game   
        self.zoom = 3
        self.square_size = floor(TILESIZE/40)
        self.range = 20
        self.map_data = []
        self.x = 0
        self.y = 0
        self.surface = pg.Rect(self.x, self.y, TILESIZE, TILESIZE)
        self.fond.fill((0, 0, 0, 100))
        self.image_pos = (floor(WIDTH*0.1), floor(HEIGHT*0.1))
        self.image = [pg.transform.scale(pg.image.load(path.join(map_folder, f'{x}.png')), (floor(WIDTH*0.8), floor(HEIGHT*0.8))) for x in range(1,9)]
        self.sprites = pg.sprite.Group()

    def event_zoom(self, y):
        self.zoom = (self.zoom + y)%len(ZOOM_VALUE)
        zoom = ZOOM_VALUE[self.zoom]
        self.square_size = floor(TILESIZE/40 * zoom)
        self.range = floor(20/zoom)
        self.x = WIDTH - (self.range+10)*self.square_size - TILESIZE
        self.y = 10
    
    def data_update(self, data):
        self.map_data = data
        self.sprites = pg.sprite.Group()
        self.x = (self.range+10)*self.square_size + TILESIZE
        self.y = 10
        self.surface = pg.Rect(self.x, self.y, self.square_size, self.square_size)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile%100 == FLOOR_ID:
                    Square(self, col, row, YELLOW, self.square_size)
                elif tile%100 == WALL_ID:
                    Square(self, col, row, BLACK, self.square_size)
                elif tile%100 == STAIR_ID or tile%100 == DOOR_ID:
                    Square(self, col, row, GREEN, self.square_size)
                elif tile%100 == SPAWN_ID:
                    Square(self, col, row, GREEN, self.square_size)

    def events(self):       
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
            elif event.type == MOUSEWHEEL:
                self.event_zoom(event.y)
    
    def display(self, screen, known_data):
        self.Playerpos = [floor(pos/TILESIZE) for pos in self.game.player.pos]
        self.screen = screen
        self.run(self.screen.copy())
        # self.game.screen.blit(self.image, self.surface)
        # Square(self, self.Playerpos[0], self.Playerpos[1], RED, self.square_size)
        # for sprite in self.sprites:
        #     self.game.screen.blit(sprite.image, sprite.surface)

    # def update(self):
    #     self.Playerpos = [floor(pos/TILESIZE) for pos in self.game.player.pos]
    #     # Square(self, Playerpos[0], Playerpos[1], RED, self.square_size)
    #     # pg.draw.rect(self.game.screen, RED, pg.Rect(self.x + Playerpos[0], self.y + Playerpos[1], self.square_size, self.square_size))
    #     # self.left = self.Playerpos[0]-self.range if self.Playerpos[0]-self.range>0 else 0
    #     # self.right = self.Playerpos[0]+self.range if self.Playerpos[0]+self.range<len(self.data[0]) else len(self.data[0])
    #     # self.top = self.Playerpos[1]-self.range if self.Playerpos[1]-self.range>0 else 0
    #     # self.bot = self.Playerpos[1]+self.range if self.Playerpos[1]+self.range<len(self.data) else len(self.data)
    #     # self.sprites.update()