from numpy.lib.twodim_base import tril_indices
from pygame.constants import MOUSEWHEEL
from Dungeon import New_Stage
import pygame as pg
import sys
from os import path
from math import floor

from settings import *
from player import *
from sprites import *
from tilemap import *
from Map import *
import time

#from Dungeon import *


def get_id(tile):
    return (tile % 100)


def get_header(game, tile):
    return tile//100 if game.actual_stage == 0 else 1


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.game_folder = path.dirname('.')
        self.clock = pg.time.Clock()

        self.hub = Instance('Hub')
        self.hub.open("Instance_Hub.csv")

        self.map_data = []
        self.known_tiles = []
        self.actual_stage = 0
        self.actual_dungeon = 0

        self.map = Map(self)
        self.HUD = []  # HUD list: Map, Life, etc
        self.interactif_sentence = None
        self.interactif_sprite = None

        self.frontLayer = pg.sprite.Group()
        self.midLayer = pg.sprite.Group()
        self.backLayer = pg.sprite.Group()
        self.interactif = pg.sprite.Group()

        self.player = Player(self, 0, 0)

    def add_to_known_tiles(self):
        PlayerX = floor(self.player.pos[0]/TILESIZE)
        PlayerY = floor(self.player.pos[1]/TILESIZE)
        PlayerRange = 2
        for tiles in (self.map_data[PlayerY-PlayerRange:PlayerY+PlayerRange]):
            for tile in (tiles[PlayerX-PlayerRange:PlayerX+PlayerRange]):
                if(tile//100 not in self.known_tiles):
                    self.known_tiles.append(tile//100)

    def draw_instance(self, instance):
        self.obstacle = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.stairs = pg.sprite.Group()
        self.backLayer = pg.sprite.Group()
        self.midLayer = pg.sprite.Group()
        self.interactif = pg.sprite.Group()
        self.map_data = instance.data
        self.known_tiles = []

        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                # print(tile, get_id(tile))
                if get_id(tile) == FLOOR_ID:
                    Floor(self, col, row, get_header(self, tile))
                elif get_id(tile) == WALL_ID:
                    Wall(self, col, row, get_header(self, tile))
                elif get_id(tile) == SPAWN_ID:
                    Floor(self, col, row, 0)
                    self.player.set_pos(col*TILESIZE, row*TILESIZE)
                elif get_id(tile) == DOOR_ID:
                    Floor(self, col, row, 0)
                    Door(self, col, row, instance.door_type, tile)
                elif get_id(tile) == STAIR_ID:
                    Floor(self, col, row, 0)
                    Stair(self, col, row)
                # HUB Features
                elif get_id(tile) == NPC_ID:
                    Floor(self, col, row, 0)
                    NPC(self, col, row, get_header(self, tile))
                    if tile % 1000 == SHOP_ID:
                        print('shop')
                        Floor(self, col, row, 0)
                        Shop_area(self, col-1, row)
                    elif tile % 1000 == QUEST_ID:
                        print("Quest")
                        Floor(self, col, row, 0)
                        Quest_area(self, col-1, row)
                elif get_id(tile) == HOUSE_ID:
                    Floor(self, col, row, 0)
                    House(self, col, row, get_header(self, tile))
                elif(tile > 0):
                    Floor(self, col, row, 0)
                    Decoration(self, col, row, tile)

        self.camera = Camera(WIDTH, HEIGHT)
        self.backLayer.update()
        self.midLayer.update()
        self.frontLayer.update()
        self.map.data_update(self.map_data)
        if(self.actual_stage == 0):
            for tiles in self.map_data:
                for tile in tiles:
                    if(tile//100 not in self.known_tiles):
                        self.known_tiles.append(tile//100)
        self.player.isPlaying = True

    def load_dungeon(self, dungeon_type, dungeon_difficulty):
        self.actual_dungeon = Dungeon(dungeon_type, dungeon_difficulty)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt_update()
            self.events()
            self.update()
            self.draw()

    def dt_update(self):
        self.dt = self.clock.tick(FPS) / 1000

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.backLayer.update()
        self.midLayer.update()
        self.frontLayer.update()
        if(self.actual_stage > 0):
            self.add_to_known_tiles()
        self.camera.update(self.player)

    def interactif_dialogue(self, sprite):
        if(sprite):
            self.interactif_sprite = sprite
            self.interactif_sentence = pg.font.SysFont("Blue Eyes.otf", 30).render(
                f'Press {sprite.key} to interact with {sprite}', True, (255, 255, 255))
            font_size = [self.interactif_sentence.get_rect(
            )[2], self.interactif_sentence.get_rect()[3]]
            self.dialogue = pg.transform.scale(pg.image.load(path.join(
                assets_folder, "dialogue.png")).convert_alpha(), (font_size[0]+15, font_size[1]+20))
        else:
            self.interactif_sprite = None
            self.interactif_sentence = None
            self.interactif_key = None

    def draw(self):
        for sprite in self.backLayer:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.midLayer:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.frontLayer:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        if(self.interactif_sentence):
            self.screen.blit(self.dialogue, (WIDTH/2-60, HEIGHT/1.3))
            self.screen.blit(self.interactif_sentence,
                             (WIDTH/2-60, HEIGHT/1.3+20))
        # for scr in self.HUD:
        #     self.screen.blit(scr.image, self.camera.apply(self))
        pg.display.update()

    def events(self):
        # print("Catch")
        # catch all events here
        for event in pg.event.get():
            # print(event.type)
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                elif not self.player.is_moving:
                    if event.key == pg.K_m:
                        self.map.display(self.screen)
                if(self.interactif_sprite):
                    if event.key == self.interactif_sprite.key and not self.player.is_moving:
                        self.interactif_sprite.interaction(self.player)

    def show_start_screen(self):
        pass
