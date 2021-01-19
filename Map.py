from pygame.constants import MOUSEWHEEL
from settings import *
from Game import *
import pygame as pg
from math import floor
from Mother_screen import *

class Square(pg.sprite.Sprite):
    def __init__(self, mother_map, x, y, color):
        self.groups = mother_map.sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.mother_map = mother_map
        self.x = mother_map.x + x*mother_map.square_size
        self.y = mother_map.y + y*mother_map.square_size
        self.image = pg.Surface((mother_map.square_size+1, mother_map.square_size+1))
        self.image.fill(color)
        self.rect = pg.Rect(self.x, self.y, mother_map.square_size, mother_map.square_size)
        # print(self.rect)

class Map(Mother_screen):
    def __init__(self, game):
        super(Map, self).__init__(game)
        self.zoom = 1.4
        self.zoom_index = 2
        self.square_size = floor(TILESIZE/40)
        self.range = 20
        self.map_data = []
        self.x = floor(WIDTH*0.3)
        self.y = floor(HEIGHT*0.3)
        self.rect = pg.Rect(self.x, self.y, TILESIZE, TILESIZE)
        self.fond.fill((0, 0, 0, 100))
        self.image_pos = (floor(WIDTH*0.1), floor(HEIGHT*0.1))
        self.animation = [pg.transform.scale(pg.image.load(path.join(map_folder, f'{x}.png')), (floor(WIDTH*0.8), floor(HEIGHT*0.8))) for x in range(1,9)]
        self.image = pg.transform.scale(pg.image.load(path.join(map_folder, '8.png')), (floor(WIDTH*0.8), floor(HEIGHT*0.8)))
        self.sprites = pg.sprite.Group()
        self.move = None
        self.old_offset = (0,0)
        self.offset_x = 0
        self.offset_y = 0

    def update(self):
        self.mouse = pg.mouse.get_pressed()
        self.pos_mouse = pg.mouse.get_pos()
        if self.mouse[0]:
            if not self.move: 
                self.move = self.pos_mouse
            self.offset_x = self.pos_mouse[0] - self.move[0] + self.old_offset[0]
            self.offset_y = self.pos_mouse[1] - self.move[1] + self.old_offset[1]
        if not self.mouse[0]:
            self.old_offset = (self.offset_x, self.offset_y)
            self.move = None
            

    def event_zoom(self, y):
        self.zoom_index = (self.zoom_index + y) if 0 < (self.zoom_index + y) < len(ZOOM_VALUE) else len(ZOOM_VALUE)-1 if (self.zoom_index + y) >= len(ZOOM_VALUE) else 0
        self.pos_mouse = pg.mouse.get_pos()
        self.zoom = ZOOM_VALUE[self.zoom_index]
    
    def data_update(self, data):
        self.map_data = data
        self.sprites = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile//100 in self.game.known_tiles or self.game.player.divinesight:
                    if tile%100 == WALL_ID:
                        Square(self, col, row, BLACK)
                    elif tile%100 == STAIR_ID or tile%100 == DOOR_ID:
                        Square(self, col, row, RED)
                    elif tile%100 == SPAWN_ID:
                        Square(self, col, row, GREEN)

    def events(self):       
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_m or pg.K_ESCAPE:
                    self.running = False
            elif event.type == MOUSEWHEEL:
                self.event_zoom(event.y)
    
    def display(self, screen):
        self.Playerpos = [floor(pos/TILESIZE) for pos in self.game.player.pos]
        self.data_update(self.map_data)
        self.screen = screen
        self.run(self.screen.copy())

    def draw(self):        
        for sprite in self.sprites:
            if(floor(WIDTH*0.25)<(self.offset_x+sprite.x*self.zoom)<floor(WIDTH*0.65) and 
            floor(HEIGHT*0.25)<(self.offset_y+sprite.y*self.zoom)<floor(HEIGHT*0.7)):
                self.screen.blit(pg.transform.scale(sprite.image,(
                    floor(sprite.image.get_width()*self.zoom),
                    floor(sprite.image.get_height()*self.zoom)
                )),(
                    floor(self.offset_x+sprite.x*self.zoom), 
                    floor(self.offset_y+sprite.y*self.zoom)
                ))