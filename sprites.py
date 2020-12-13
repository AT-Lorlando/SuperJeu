from Dungeon import New_Stage
import pygame as pg
from settings import *
from os import path
from Dungeon import *
from inventory_clem import *
from shop import *
vec = pg.math.Vector2


def resize(img, size):
    return pg.transform.scale(img, (size+2, size+2))


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.frontLayer.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((100, 100))
        self.rect = self.image.get_rect()
        self.looking_at = 'Bot'
        self.actual_frame = 1
        self.time_since_anime = 0
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.playerpos = [floor(pos/TILESIZE) for pos in self.pos]
        self.isPlaying = False
        self.walk_right = [(pg.image.load(
            path.join(champ_folder, f'R{x}.png')).convert_alpha()) for x in range(1, 4)]
        self.walk_top = [(pg.image.load(
            path.join(champ_folder, f'T{x}.png')).convert_alpha()) for x in range(1, 4)]
        self.walk_bot = [(pg.image.load(
            path.join(champ_folder, f'B{x}.png')).convert_alpha()) for x in range(1, 4)]

    def set_pos(self, x, y):
        self.pos.x = x
        self.pos.y = y

    def walking(self):
        self.time = pg.time.get_ticks()
        if(self.time > self.time_since_anime + 150):
            self.time_since_anime = self.time
            self.actual_frame = (self.actual_frame + 1) % 3
            if(self.looking_at == 'Right'):
                self.image = self.walk_right[self.actual_frame]
            elif(self.looking_at == 'Left'):
                self.image = pg.transform.flip(
                    self.walk_right[self.actual_frame], True, False)
            elif(self.looking_at == 'Top'):
                self.image = self.walk_top[self.actual_frame]
            elif(self.looking_at == 'Bot'):
                self.image = self.walk_bot[self.actual_frame]

            self.image.set_colorkey(GREEN)

    def chilling(self):
        self.time = pg.time.get_ticks()
        if(self.time > self.time_since_anime + 180):
            self.time_since_anime = self.time
            self.actual_frame = (self.actual_frame + 1) % 3
            if(self.looking_at == 'Right'):
                self.image = self.walk_right[0]
            elif(self.looking_at == 'Left'):
                self.image = pg.transform.flip(self.walk_right[0], True, False)
            elif(self.looking_at == 'Top'):
                self.image = self.walk_top[0]
            elif(self.looking_at == 'Bot'):
                self.image = self.walk_bot[0]
            self.image.set_colorkey(WHITE)

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.chilling
            else:
                self.looking_at = 'Left'
                self.vel.x = -PLAYER_SPEED
                self.walking()
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.looking_at = 'Right'
            self.vel.x = PLAYER_SPEED
            self.walking()
        if keys[pg.K_UP] or keys[pg.K_w]:
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.chilling()
            else:
                self.looking_at = 'Top'
                self.vel.y = -PLAYER_SPEED
                self.walking()
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.looking_at = 'Bot'
            self.vel.y = PLAYER_SPEED
            self.walking()
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        if keys[pg.K_0]:
            print(self.pos[0])

    def collide_with_obstacle(self, dir):
        # self.game.interactif_dialogue(0)

        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.obstacle, False)
            if hits:
                self.collide_interaction(hits[0])
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        elif dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.obstacle, False)
            if hits:
                self.collide_interaction(hits[0])
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def collide_interaction(self, sprite):
        if sprite in self.game.doors:
            self.isPlaying = False
            self.passing_door(sprite)
        elif sprite in self.game.stairs:
            self.isPlaying = False
            self.go_upstair()
        elif isinstance(sprite, Shoper):
            self.game.interactif_dialogue(sprite)
        else:
            self.game.interactif_dialogue(0)

    def passing_door(self, door):
        self.game.known_tiles = []
        if(door.door_type > 0):  # Door linked to a dungeon
            self.game.load_dungeon(
                door.instance_behind[0], door.instance_behind[1])
            self.game.actual_stage += 1
            self.game.draw_instance(
                self.game.actual_dungeon.stage_tab[self.game.actual_stage-1])
        else:  # Door linked to menu
            self.game.actual_stage = 0
            self.game.draw_instance(self.game.hub)

    def go_upstair(self):
        assert(self.game.actual_dungeon)
        self.game.known_tiles = []
        self.game.actual_stage += 1
        self.game.draw_instance(
            self.game.actual_dungeon.stage_tab[self.game.actual_stage-1])

    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.obstacle, False)
        self.collide_interaction(hits)
        if(self.isPlaying):
            self.get_keys()
            self.pos += 2*self.vel * self.game.clock.tick(FPS) / 1000
            self.rect.x = self.pos.x
            self.collide_with_obstacle('x')
            self.rect.y = self.pos.y
            self.collide_with_obstacle('y')
            self.playerpos = [floor(pos/TILESIZE) for pos in self.pos]
        if(self.vel == (0, 0)):
            self.chilling()


class Floor(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.backLayer.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = resize(pg.image.load(
            path.join(room_folder, "room-floor.png")).convert_alpha(), TILESIZE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.backLayer.all_sprites, game.obstacle, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.image = resize(pg.image.load(
            path.join(wall_folder, "w (7).png")).convert_alpha(), TILESIZE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y, door_type, instance_behind):
        self.groups = game.backLayer.all_sprites, game.obstacle, game.doors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.door_type = door_type
        self.instance_behind = (floor(instance_behind %
                                      1000/100), floor(instance_behind % 100/10))
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = (x) * TILESIZE
        self.rect.y = (y) * TILESIZE
        self.actual_frame = 1
        self.time_since_anime = 0
        self.portal = [(pg.image.load(
            path.join(portal_folder, f'{x}.png')).convert_alpha()) for x in range(1, 4)]

    def turn(self):
        self.time = pg.time.get_ticks()
        if(self.time > self.time_since_anime + 150):
            self.time_since_anime = self.time
            self.actual_frame = (self.actual_frame + 1) % 3
            self.image = resize(self.portal[self.actual_frame], TILESIZE)

    def update(self):
        self.turn()


class Stair(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.backLayer.all_sprites, game.obstacle, game.stairs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = (x) * TILESIZE
        self.rect.y = (y) * TILESIZE
        self.actual_frame = 1
        self.time_since_anime = 0
        self.portal = [(pg.image.load(
            path.join(portal_folder, f'{x}.png')).convert_alpha()) for x in range(1, 4)]

    def turn(self):
        self.time = pg.time.get_ticks()
        if(self.time > self.time_since_anime + 150):
            self.time_since_anime = self.time
            self.actual_frame = (self.actual_frame + 1) % 3
            self.image = resize(self.portal[self.actual_frame], TILESIZE)

    def update(self):
        self.turn()


class Shoper(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.frontLayer.all_sprites, game.obstacle
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE*2, TILESIZE*2))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = (x) * TILESIZE
        self.rect.y = (y) * TILESIZE
        self.shop = create_screen_shop(create_shop())
