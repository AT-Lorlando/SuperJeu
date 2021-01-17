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
from screen_inv import *
from hud import *
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
        
        LIFE_HUD = Life_HUD(HEIGHT//15 + 10,15 ,self.player)
        EXP_HUD = Exp_HUD(HEIGHT//15 + 10,45 ,self.player)
        CHARACTER_HUD = Character_HUD(5,5, self.player)
        Life_DATA_HUD = Life_Data_HUD(300,12, self.player)
        Exp_DATA_HUD = Exp_Data_HUD(300,42, self.player)

        self.HUD.append(LIFE_HUD)
        self.HUD.append(EXP_HUD)
        self.HUD.append(CHARACTER_HUD)
        self.HUD.append(Life_DATA_HUD)
        self.HUD.append(Exp_DATA_HUD)


        self.resume = False
        self.screen_inv = Screen_inv(self.screen, self)

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
        self.doors = pg.sprite.Group()
        self.stairs = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.interactif = pg.sprite.Group()
        self.map_data = instance.data
        self.known_tiles = []

        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                # print(tile, get_id(tile))
                if get_id(tile) == FLOOR_ID:
                    Floor(self, col, row, get_header(self, tile))
                elif get_id(tile) == WALL_ID:
                    Floor(self, col, row, get_header(self, tile))
                    Wall(self, col, row, get_header(self, tile))
                elif get_id(tile) == SPAWN_ID:
                    Floor(self, col, row, tile if self.actual_stage else 0)
                    if not self.resume:
                        self.player.set_pos(col*TILESIZE, row*TILESIZE)
                    else:
                        pass

                elif get_id(tile) == DOOR_ID:
                    Floor(self, col, row, tile if self.actual_stage else 0)
                    Door(self, col, row, get_header(self, tile))
                elif get_id(tile) == STAIR_ID:
                    Floor(self, col, row, tile)
                    Stair(self, col, row)
                elif get_id(tile) == COLLECTABLE_ID:
                    Floor(self, col, row, tile if self.actual_stage else 0)
                    Collectable(self, col, row, tile)
                elif get_id(tile) == MOB_ID:
                    Floor(self, col, row, tile if self.actual_stage else 0)
                    Mob(self, col, row, tile)

                # HUB Features
                elif get_id(tile) == NPC_ID:
                    Floor(self, col, row, 0)
                    NPC(self, col, row, get_header(self, tile))
                    if tile % 1000 == SHOP_ID:
                        Floor(self, col, row, 0)
                        Shop_area(self, col, row, tile)
                    elif tile % 1000 == QUEST_ID:
                        Floor(self, col, row, 0)
                        Quest_area(self, col, row, tile)
                    elif tile % 1000 == CHEST_ID:
                        Floor(self, col, row, tile if self.actual_stage else 0)
                        Chest_area(self, col, row, tile)
                    elif tile % 1000 == SAVE_ID:
                        Floor(self, col, row, tile if self.actual_stage else 0)
                        Save_area(self, col, row, tile)
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

    def animation_add(self, image_tab, sprite=None, pos=(0,0),colorkey=None):
        if(sprite):
            self.animation_tab.append(
                Animation(self, self.camera.apply(sprite), image_tab, colorkey))
        else:
            self.animation_tab.append(
                Animation(self, pos, image_tab,colorkey))

    def run(self):
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
            font_size = [self.interactif_sentence.get_rect()[2], self.interactif_sentence.get_rect()[3]]
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
        for hud in self.HUD:
            hud.draw(self)
        pg.display.update()

    def save(self):
        inv = []
        for case in self.player.inv.inventory:
            if case.item != None:
                inv.append(case.item.name)
        print("inv = ", inv)
        save = Save_player(self.player.money, self.player.pos,
                           self.player.xp, self.player.quest_list)
        pickle.dump((save), open("save.p", "wb"))
        print(self.player.pos, "and money", self.player.money)
        pass

    def load(self):
        save = pickle.load(open("save.p", "rb"))
        # save.money += 100
        self.player.money = save.money
        self.player.pos = save.pos
        self.player.xp = save.xp
        self.player.quest_list = save.actual_quests

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
                if event.key == pg.K_i:
                    print("inv open")
                    self.screen_inv.run(self.screen.copy(), self.player)
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
    def __init__(self, game, pos, tab, colorkey = None):
        self.game = game
        self.frame_rate = 12
        self.time_since_anime = 0
        self.actual_frame = 0
        self.pos = pos
        self.colorkey = None
        if colorkey:
            self.colorkey = colorkey
        # self.rect = pg.Rect(0,0,pos)
        self.image_tab = tab
        self.to_kill = False

    def draw(self):
        this_image = self.image_tab[self.actual_frame]
        if self.colorkey:
            this_image.set_colorkey(self.colorkey)
        self.game.screen.blit(this_image, self.pos)

    def update(self):
        now = pg.time.get_ticks()
        if(now > self.time_since_anime + self.frame_rate):
            self.time_since_anime = now
            self.actual_frame += 1
            if self.actual_frame >= len(self.image_tab):
                self.game.animation_tab.remove(self)

class Save_player():
    def __init__(self, money, pos, xp, actual_quests):
        self.money = money
        self.pos = pos
        self.xp = xp
        self.actual_quests = actual_quests
