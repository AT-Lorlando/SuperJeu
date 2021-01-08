from numpy.lib.twodim_base import tril_indices
from pygame import image
from pygame.constants import MOUSEWHEEL
from Dungeon import New_Stage
import pygame as pg
import sys
from os import path
from math import floor
import pickle

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
    if game.actual_dungeon:
        return game.actual_dungeon.type
    else:
        return tile//100


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.game_folder = path.dirname('.')
        self.clock = pg.time.Clock()

        self.dt = self.clock.tick(FPS) / 1000

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

        # Layer:
        self.Layers = [pg.sprite.Group() for _ in range(LAYER_NUMBER)]
        # print(self.Layers)
        # self.frontLayer = pg.sprite.Group()
        # self.midLayer = pg.sprite.Group()
        # self.backLayer = pg.sprite.Group()
        # self.interactif = pg.sprite.Group()

        self.animation_tab = []

        self.player = Player(self, 0, 0)

        self.resume = False

    def add_to_known_tiles(self):
        PlayerX = floor(self.player.pos[0]/TILESIZE)
        PlayerY = floor(self.player.pos[1]/TILESIZE)
        PlayerRange = 2
        for tiles in (self.map_data[PlayerY-PlayerRange:PlayerY+PlayerRange]):
            for tile in (tiles[PlayerX-PlayerRange:PlayerX+PlayerRange]):
                if(tile//100 not in self.known_tiles):
                    self.known_tiles.append(tile//100)

    def clean_layers(self, i):
        for i in range(i):
            self.Layers[i] = pg.sprite.Group()

    def draw_instance(self, instance):
        # print("Drawing")
        self.clean_layers(LAYER_NUMBER-1)
        # print(self.Layers)
        self.obstacle = pg.sprite.Group()
        # self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.stairs = pg.sprite.Group()
        # self.backLayer = pg.sprite.Group()
        # self.midLayer = pg.sprite.Group()
        self.interactif = pg.sprite.Group()
        self.map_data = instance.data
        self.known_tiles = []

        print("before row tiles loop pos", self.player.pos)

        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                # print(tile, get_id(tile))
                if get_id(tile) == FLOOR_ID:
                    Floor(self, col, row, get_header(self, tile))
                elif get_id(tile) == WALL_ID:
                    Floor(self, col, row, get_header(self, 0))
                    Wall(self, col, row, get_header(self, tile))
                elif get_id(tile) == SPAWN_ID:
                    Floor(self, col, row, 0)
                    if not self.resume:
                        self.player.set_pos(col*TILESIZE, row*TILESIZE)
                    else:
                        pass

                elif get_id(tile) == DOOR_ID:
                    Floor(self, col, row, 0)
                    Door(self, col, row, get_header(self, tile))
                elif get_id(tile) == STAIR_ID:
                    Floor(self, col, row, 0)
                    Stair(self, col, row)
                # HUB Features
                elif get_id(tile) == NPC_ID:
                    Floor(self, col, row, 0)
                    NPC(self, col, row, get_header(self, tile))
                    if tile % 1000 == SHOP_ID:
                        # print('shop')
                        Floor(self, col, row, 0)
                        Shop_area(self, col-1, row)
                    elif tile % 1000 == QUEST_ID:
                        # print("Quest")
                        Floor(self, col, row, 0)
                        Quest_area(self, col-1, row)
                elif get_id(tile) == HOUSE_ID:
                    Floor(self, col, row, 0)
                    House(self, col, row, get_header(self, tile))
                elif(tile > 0):
                    Floor(self, col, row, 0)
                    Decoration(self, col, row, tile)
        # print("befor camera pos", self.player.pos)

        self.camera = Camera(WIDTH, HEIGHT)
        for layer in self.Layers:
            layer.update()
        # self.backLayer.update()
        # self.midLayer.update()
        # self.frontLayer.update()
        # print(self.Layers)
        self.map.data_update(self.map_data)
        if(self.actual_stage == 0):
            for tiles in self.map_data:
                for tile in tiles:
                    if(tile//100 not in self.known_tiles):
                        self.known_tiles.append(tile//100)
        self.player.isPlaying = True

    def load_dungeon(self, dungeon_type, dungeon_difficulty):
        self.actual_dungeon = Dungeon(dungeon_type, dungeon_difficulty)

    def animation_add(self, sprite, image_tab):
        self.animation_tab.append(
            Animation(self, self.camera.apply(sprite), image_tab))

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
        # self.backLayer.update()
        # self.midLayer.update()
        for layer in self.Layers:
            layer.update()
        for animation in self.animation_tab:
            animation.update()
        # self.frontLayer.update()
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
        self.screen.fill(DARKGREY)
        for layer in self.Layers:
            for sprite in layer:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
        for animation in self.animation_tab:
            animation.draw()
        if(self.interactif_sentence):
            self.screen.blit(self.dialogue, (WIDTH/2-60, HEIGHT/1.3))
            self.screen.blit(self.interactif_sentence,
                             (WIDTH/2-60, HEIGHT/1.3+20))
        # for scr in self.HUD:
        #     self.screen.blit(scr.image, self.camera.apply(self))
        pg.display.update()

    def save(self):
        save = Save_player(self.player.money, self.player.pos)
        pickle.dump((save), open("save.p", "wb"))
        print(self.player.pos, "and money", self.player.money)
        pass

    def load(self):
        save = pickle.load(open("save.p", "rb"))
        # save.money += 100
        self.player.money = save.money
        self.player.pos = save.pos
        # self.player.set_pos(save.pos[0], save.pos[1])
        print(save.money)
        print(self.player.pos)

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
                if event.key == pg.K_s:
                    print("s")
                    self.save()
                elif not self.player.is_moving:
                    if event.key == pg.K_m:
                        self.map.display(self.screen)
                if(self.interactif_sprite):
                    if event.key == self.interactif_sprite.key and not self.player.is_moving:
                        self.interactif_sentence = None
                        self.draw()
                        self.interactif_sprite.interaction(self.player)

    def show_start_screen(self):
        pass


class Animation():
    def __init__(self, game, pos, tab):
        self.game = game
        self.frame_rate = 12
        self.time_since_anime = 0
        self.actual_frame = 0
        self.pos = pos
        # self.rect = pg.Rect(0,0,pos)
        self.image_tab = tab
        self.to_kill = False

    def draw(self):
        this_image = self.image_tab[self.actual_frame]
        this_image.set_colorkey((223, 222, 223))
        self.game.screen.blit(this_image, self.pos)

    def update(self):
        now = pg.time.get_ticks()
        if(now > self.time_since_anime + self.frame_rate):
            self.time_since_anime = now
            self.actual_frame += 1
            if self.actual_frame >= len(self.image_tab):
                self.game.animation_tab.remove(self)
                print("removed", len(self.game.animation_tab))


class Save_player():
    def __init__(self, money, pos):
        self.money = money
        self.pos = pos
