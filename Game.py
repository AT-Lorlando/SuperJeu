from pygame.constants import MOUSEWHEEL
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
        self.HUD = [1, 1, 1, 1, 1, 1, 1, 1]  # HUD list: Minimap, Life, etc
        self.actual_stage = 0
        self.actual_dungeon = 0
        self.hub = Instance('Hub')
        self.frontLayer = pg.sprite.Group()
        self.frontLayer.all_sprites = pg.sprite.Group()
        self.backLayer = pg.sprite.Group()
        self.backLayer.all_sprites = pg.sprite.Group()
        self.interactif = pg.sprite.Group()
        self.player = Player(self, 0, 0)
        self.known_tiles = []
        self.interactif_sentence = None

    def add_to_known_tiles(self):
        PlayerX = floor(self.player.pos[0]/TILESIZE)
        PlayerY = floor(self.player.pos[1]/TILESIZE)
        PlayerRange = 2
        for tiles in (self.map_data[PlayerY-PlayerRange:PlayerY+PlayerRange]):
            for tile in (tiles[PlayerX-PlayerRange:PlayerX+PlayerRange]):
                tileID = floor(tile/10)
                if(tileID not in self.known_tiles):
                    self.known_tiles.append(tileID)

    def draw_instance(self, instance):
        self.obstacle = pg.sprite.Group()
        self.obstacle.interactif = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.stairs = pg.sprite.Group()
        self.backLayer = pg.sprite.Group()
        self.backLayer.all_sprites = pg.sprite.Group()
        self.map_data = instance.data
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile % 10 == FLOOR_ID:
                    Floor(self, col, row)
                elif tile % 10 == WALL_ID:
                    Wall(self, col, row)
                elif tile % 10 == SPAWN_ID:
                    Floor(self, col, row)
                    self.player.set_pos(col*TILESIZE, row*TILESIZE)
                    print('Set player to', col, row)
                elif tile % 10 == DOOR_ID:
                    Floor(self, col, row)
                    Door(self, col, row, instance.door_type, tile)
                elif tile % 10 == SHOP_ID:
                    Floor(self, col, row)
                    Shoper(self, col, row)
                elif tile % 10 == STAIR_ID:
                    Floor(self, col, row)
                    Stair(self, col, row)
        self.camera = Camera(WIDTH, HEIGHT)
        self.backLayer.all_sprites.update()
        self.frontLayer.all_sprites.update()
        self.minimap.data_update(self.map_data)
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
        self.minimap.update()

    def interactif_dialogue(self, sprite):
        if(sprite):
            # print('2')
            self.interactif_sentence = f'Press sprite.key to interact with {sprite}'
        else:
            self.interactif_sentence = None
            # print('3')

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(DARKGREY)
        for sprite in self.backLayer.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        for sprite in self.frontLayer.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        if(self.interactif_sentence):
            font_surface = pg.font.SysFont("Blue Eyes.otf", 30).render(
                self.interactif_sentence, True, (255, 255, 255))
            font_size = [font_surface.get_rect(
            )[2], font_surface.get_rect()[3]]
            dialogue = pg.transform.scale(pg.image.load(path.join(
                assets_folder, "dialogue.png")).convert_alpha(), (font_size[0]+15, font_size[1]+20))
            self.screen.blit(dialogue, (WIDTH/2-60, HEIGHT/1.3))
            self.screen.blit(font_surface, (WIDTH/2-60, HEIGHT/1.3+20))
            screen_shop.running = True
        pg.display.flip()

    def print_minimap(self):
        while self.HUD[0]:
            self.minimap.draw()
            pg.display.flip()
            self.events()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                elif event.key == pg.K_m:
                    self.HUD[0] = (self.HUD[0]+1) % 2
                    if(self.HUD[0]):
                        self.print_minimap()

            elif event.type == MOUSEWHEEL:
                self.minimap.event_zoom(event.y)

    def show_start_screen(self):
        pass
