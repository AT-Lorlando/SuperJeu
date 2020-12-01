from Dungeon import New_Stage
import pygame as pg
from settings import *
from os import path
from Dungeon import *

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.frontLayer.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((12, 17))
        self.rect = self.image.get_rect()
        self.looking_at = 'Bot'
        self.actual_frame = 1
        self.time_since_anime = 0
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.isPlaying = False
        self.walk_right = [(pg.image.load(path.join(champ_folder,f'R{x}.png')).convert_alpha()) for x in range(1,4)]
        self.walk_top = [(pg.image.load(path.join(champ_folder,f'T{x}.png')).convert_alpha()) for x in range(1,4)]
        self.walk_bot = [(pg.image.load(path.join(champ_folder,f'B{x}.png')).convert_alpha()) for x in range(1,4)]
    
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
                self.image = pg.transform.flip(self.walk_right[self.actual_frame], True, False)
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

    def collide_with_obstacle(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.obstacle, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
                if hits[0] in self.game.doors:
                    self.isPlaying = False
                    self.passing_door(hits[0])
                if hits[0] in self.game.walls:
                    pass
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.obstacle, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                if hits[0] in self.game.doors:
                    self.isPlaying = False
                    self.passing_door(hits[0])
                if hits[0] in self.game.walls:
                    pass

    def passing_door(self, door):
        if(door.door_type > 0): #Door linked to a dungeon
            self.game.load_dungeon(door.instance_behind[0], door.instance_behind[1])
            self.game.actual_stage+=1
            self.game.draw_instance(self.game.actual_dungeon.stage_tab[self.game.actual_stage])
        else: #Door linked to menu
            self.game.actual_stage=0
            self.game.draw_instance(self.game.hub)

    def update(self):
        self.get_keys()
        if(self.isPlaying):
            self.pos += 2*self.vel * self.game.clock.tick(FPS) / 1000
            self.rect.x = self.pos.x
            self.collide_with_obstacle('x')
            self.rect.y = self.pos.y
            self.collide_with_obstacle('y')
        if(self.vel == (0, 0)):
            self.chilling()

class Floor(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.backLayer.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(path.join(room_folder, "room-floor.png")).convert_alpha()
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
        self.image = pg.image.load(path.join(wall_folder, "w (7).png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y, door_type, instance_type, difficulty):
        self.groups = game.backLayer.all_sprites, game.obstacle, game.doors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.door_type = door_type
        self.instance_behind = (instance_type, difficulty)
        self.image = pg.image.load(path.join(portal_folder,'1.png'))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = (x) * TILESIZE
        self.rect.y = (y) * TILESIZE
        self.actual_frame = 1
        self.time_since_anime = 0
        self.portal = [(pg.image.load(path.join(portal_folder,f'{x}.png')).convert_alpha()) for x in range(1,4)]
        
    def turn(self):
        self.time = pg.time.get_ticks()
        if(self.time > self.time_since_anime + 150):
            self.time_since_anime = self.time
            self.actual_frame = (self.actual_frame + 1) % 3
            self.image = self.portal[self.actual_frame]

    def update(self):
        self.turn()

class Exit(pg.sprite.Sprite):
    def __init__(self, game, x, y, i):
        self.groups = game.backLayer.all_sprites, game.obstacle, game.doors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.map_number = i
        self.image = pg.Surface((1.25 * TILESIZE, 1.25 * TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = (x - 0.125) * TILESIZE
        self.rect.y = (y - 0.125) * TILESIZE
