from Dungeon import New_Stage
import pygame as pg
import sys
from os import path
from math import floor

from settings import *
from sprites import *
from tilemap import *
#from Dungeon import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.game_folder = path.dirname('.')
        self.clock = pg.time.Clock()
        self.map_data = []
        # self.actual_room = 0
        # self.actual_map = 0
        # self.load_map_data(0)
        # self.load_room_data(0, 0)
        # self.known_map = []
        # self.known_map.append('0')
        self.frontLayer = pg.sprite.Group()
        self.frontLayer.all_sprites = pg.sprite.Group()
        self.backLayer = pg.sprite.Group()
        self.backLayer.all_sprites = pg.sprite.Group()
        self.player = Player(self, 0, 0)

    # def map_folder(self, map_ID):
    #     return path.join(dungeon_folder, f'map{map_ID}')

    # def map_path(self, map_ID):
    #     return path.join(self.map_folder(map_ID),  f'map{map_ID}.txt')

    # def room_path(self, room_ID, map_ID):
    #     return path.join(self.map_folder(map_ID),  f'room{room_ID}.txt')

    # def load_map_data(self, ID):
    #     self.map = Map(self.map_path(ID))

    # def load_room_data(self, ID, map_ID):
    #     self.room = Room(self.room_path(ID, map_ID))

    # def new_map(self, ID):
    #     self.load_map_data(ID)

    def load_dungeon_data(self, difficulty):
        self.obstacle = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        thisStage = New_Stage(1, difficulty)
        self.map_data = thisStage.data
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == FLOOR_ID:
                    Floor(self, col, row)
                if tile == WALL_ID:
                    Wall(self, col, row)
                if tile == SPAWN_ID:
                    Floor(self, col, row)
                    self.player.set_pos(col*TILESIZE, row*TILESIZE)
                    print('Set player to', col, row)
        self.camera = Camera(20, 20)
        self.frontLayer.all_sprites.update()
        self.player.isPlaying = True

        
    # def new_room(self, ID, map_ID, side):
    #     self.load_room_data(ID, map_ID)
    #     self.obstacle = pg.sprite.Group()
    #     self.walls = pg.sprite.Group()
    #     self.doors = pg.sprite.Group()
    #     thisRow = 0
    #     thisCol = 0
    #     thisPlayerRow = 0
    #     thisPlayerCol = 0
    #     thisDoorCoord = []
    #     thisMapData = self.map.data
    #     thisRoomData = self.room.data
    #     while(f'{self.actual_room}' not in thisMapData[thisRow]):
    #         thisRow += 1
    #     while(f'{self.actual_room}' not in thisMapData[thisRow][thisCol]):
    #         thisCol += 1
    #     for row, tiles in enumerate(thisRoomData):
    #         for col, tile in enumerate(tiles):
    #             if tile == '.':
    #                 Floor(self, col, row)
    #             if tile == '1':
    #                 Wall(self, col, row)
    #             if tile == 'S':
    #                 Exit(self, col, row, self.actual_map + 1)
    #             if tile == 'P':
    #                 Floor(self, col, row)
    #                 if(side == 'start'):
    #                     thisPlayerRow = row
    #                     thisPlayerCol = col
    #             if tile == 'D':
    #                 #Wall(self, col, row)
    #                 thisDoorCoord.append((col,row))
                    
    #     for col, row in thisDoorCoord:
    #         if(col == 0 and thisMapData[thisRow][thisCol-1] != '.'):
    #                     Door(self, col, row,
    #                         thisMapData[thisRow][thisCol-1], 'LEFT')
    #                     if(side == 'RIGHT'):
    #                         thisPlayerRow = row
    #                         thisPlayerCol = col+2

    #         elif(col == len(thisRoomData[0])-1 and thisMapData[thisRow][thisCol+1] != '.'):
    #                     Door(self, col, row,
    #                          thisMapData[thisRow][thisCol+1], 'RIGHT')
    #                     if(side == 'LEFT'):
    #                         thisPlayerRow = row
    #                         thisPlayerCol = col-2

    #         elif(row == 0 and thisMapData[thisRow-1][thisCol] != '.'):
    #                     Door(self, col, row,
    #                          thisMapData[thisRow-1][thisCol], 'TOP')
    #                     if(side == 'BOT'):
    #                         thisPlayerRow = row+2
    #                         thisPlayerCol = col

    #         elif(row == len(thisRoomData)-1 and thisMapData[thisRow+1][thisCol] != '.'):
    #                     Door(self, col, row,
    #                          thisMapData[thisRow+1][thisCol], 'BOT')
    #                     if(side == 'TOP'):
    #                         thisPlayerRow = row-2
    #                         thisPlayerCol = col

    #     self.camera = Camera(self.room.width, self.room.height)
        
    #     self.player.set_pos(thisPlayerCol * TILESIZE, thisPlayerRow*TILESIZE)
    #     self.known_map.append(f'{ID}')
    #     self.frontLayer.all_sprites.update()
    #     self.player.isPlaying = True

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
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    # def draw_minimap(self):
    #     thisSize = 1 * TILESIZE
    #     thisCol = WIDTH - thisSize - TILESIZE
    #     thisRow = thisSize
    #     # thisCol = 0
    #     # thisRow = 0
    #     thisMapData = self.map.data
    #     thisMiniSize = floor(thisSize / len(thisMapData))
    #     pg.draw.rect(self.screen, BLACK, pg.Rect(
    #         thisCol, thisRow, thisSize, thisSize))
    #     for row, tiles in enumerate(thisMapData):
    #         for col, tile in enumerate(tiles):
    #             if tile == '.':
    #                 pg.draw.rect(self.screen, BLACK, pg.Rect(
    #                     thisCol+((thisMiniSize+1)*col), thisRow+((thisMiniSize+1)*row), thisMiniSize, thisMiniSize))
    #             elif tile in (self.known_map):
    #                 pg.draw.rect(self.screen, LIGHTGREY, pg.Rect(
    #                     thisCol+((thisMiniSize+1)*col), thisRow+((thisMiniSize+1)*row), thisMiniSize, thisMiniSize))
    #             else:
    #                 pg.draw.rect(self.screen, BLACK, pg.Rect(
    #                     thisCol+((thisMiniSize+1)*col), thisRow+((thisMiniSize+1)*row), thisMiniSize, thisMiniSize))
    #             if tile == str(self.actual_room):
    #                 pg.draw.rect(self.screen, YELLOW, pg.Rect(
    #                     thisCol+((thisMiniSize+1)*col), thisRow+((thisMiniSize+1)*row), thisMiniSize, thisMiniSize))

    def draw(self):
        self.screen.fill(BGCOLOR)
        for sprite in self.backLayer.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.frontLayer.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #self.draw_minimap()
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


