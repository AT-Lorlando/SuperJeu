from Dungeon import New_Stage
import pygame as pg
import sys
from os import path
from math import floor

from settings import *
from sprites import *
from tilemap import *
from Minimap import *
#from Dungeon import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.game_folder = path.dirname('.')
        self.clock = pg.time.Clock()
        self.map_data = []
        self.minimap = Minimap(self)
        self.actual_stage = 0
        self.actual_dungeon = 0
        self.hub = Instance('Hub')
        self.frontLayer = pg.sprite.Group()
        self.frontLayer.all_sprites = pg.sprite.Group()
        self.backLayer = pg.sprite.Group()
        self.backLayer.all_sprites = pg.sprite.Group()
        self.player = Player(self, 0, 0)
        self.known_tiles = []

    def add_to_known_tiles(self):
        PlayerX = floor(self.player.pos[0]/TILESIZE)
        PlayerY = floor(self.player.pos[1]/TILESIZE)
        PlayerRange = 2
        for tiles in (self.map_data[PlayerY-PlayerRange:PlayerY+PlayerRange]):
            for tile in (tiles[PlayerX-PlayerRange:PlayerX+PlayerRange]):
                tileID = floor(tile%100/10)
                if(tileID not in self.known_tiles):
                    self.known_tiles.append(tileID)

    def draw_instance(self, instance):
        self.obstacle = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.map_data = instance.data
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile%10 == FLOOR_ID:
                    Floor(self, col, row)
                elif tile%10 == WALL_ID:
                    Wall(self, col, row)
                elif tile%10 == SPAWN_ID:
                    Floor(self, col, row)
                    self.player.set_pos(col*TILESIZE, row*TILESIZE)
                elif tile%10 == DOOR_ID:
                    Door(self, col, row, instance.door_type, floor(tile%100/10), floor(tile%1000/100))
        self.camera = Camera(WIDTH , HEIGHT)
        self.frontLayer.all_sprites.update()
        self.minimap.data = self.map_data
        print('Stage:', self.actual_stage)
        self.player.isPlaying = True 

    def load_dungeon(self, dungeon_type, dungeon_difficulty):
        self.actual_dungeon = Dungeon(dungeon_type, dungeon_difficulty)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.backLayer.all_sprites.update()
        self.frontLayer.all_sprites.update()
        self.add_to_known_tiles()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        for sprite in self.backLayer.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.frontLayer.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.minimap.draw(self.map_data, self.known_tiles)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass


