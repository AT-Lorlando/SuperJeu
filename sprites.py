import pygame as pg
from settings import *
from os import path
from Dungeon import *
from inventory_clem import *
from shop import *
from screen_shop import *
from dialogue import Dialogue
from quest import *
vec = pg.math.Vector2

class MySprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, tile=0):
        self.game = game
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        self.hp = None

class Floor(MySprite):
    def __init__(self, game, x, y, tile):
        img = random.randint(1,8) if tile else 0
        self.image = resize(pg.image.load(
            path.join(floor_folder, f'{img}.png')), TILESIZE)
        self.rect = self.image.get_rect()
        super(Floor,self).__init__(game, x, y, tile)
        self.groups = game.Layers[0]
        pg.sprite.Sprite.__init__(self, self.groups)
class Decoration(MySprite):
    def __init__(self, game, x, y, tile):
        self.image = resize(pg.image.load(
            path.join(deco_folder, f'{tile}.png')), TILESIZE)
        self.rect = self.image.get_rect()
        super(Decoration,self).__init__(game, x, y, tile)
        self.groups = game.Layers[1]
        pg.sprite.Sprite.__init__(self, self.groups)
class Wall(MySprite):
    def __init__(self, game, x, y, tile):
        img = random.randint(1,6) if tile else 0
        self.image = resize(pg.image.load(
            path.join(wall_folder, f'{img}.png')), TILESIZE)
        self.rect = self.image.get_rect()
        super(Wall,self).__init__(game, x, y, tile)
        self.groups = game.Layers[2], game.obstacle
        pg.sprite.Sprite.__init__(self, self.groups)
        
class House(MySprite):
    def __init__(self, game, x, y, tile):
        self.image = resize(pg.image.load(
            path.join(house_folder, f'{tile}.png')), 4*TILESIZE, 3*TILESIZE)
        self.rect = self.image.get_rect()
        super(House,self).__init__(game, x, y, tile)
        self.groups = game.Layers[3], game.obstacle
        pg.sprite.Sprite.__init__(self, self.groups)

        self.hp = 10

    def update(self):
        if self.hp < 1:
            self.kill()

class Door(MySprite):
    def __init__(self, game, x, y, tile):
        self.image_tab = [(resize(pg.image.load(path.join(portal_folder, f'p ({x}).gif')), TILESIZE)) for x in range(1, 21)]
        self.image = self.image_tab[0]
        self.rect = self.image.get_rect()
        super(Door,self).__init__(game, x, y, tile)
        self.groups = game.Layers[4], game.obstacle, game.doors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.door_type = 1
        self.instance_behind = (tile//10, tile%10) #Type,dif
        self.actual_frame = 0
        self.time_since_anime = 0

    def turn(self):
        self.time = pg.time.get_ticks()
        if(self.time > self.time_since_anime + 25):
            self.time_since_anime = self.time
            self.actual_frame = (self.actual_frame + 1) % 19
            self.image = self.image_tab[self.actual_frame]

    def update(self):
        self.turn()


class Stair(MySprite):
    def __init__(self, game, x, y):
        self.image_tab = [(resize(pg.image.load(path.join(portal_folder, f'p ({x}).gif')), TILESIZE)) for x in range(1, 21)]
        self.image = self.image_tab[0]
        self.rect = self.image.get_rect()
        super(Stair,self).__init__(game, x, y)
        self.groups = game.Layers[4], game.obstacle, game.stairs
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.actual_frame = 1
        self.time_since_anime = 0


    def turn(self):
        self.time = pg.time.get_ticks()
        if(self.time > self.time_since_anime + 25):
            self.time_since_anime = self.time
            self.actual_frame = (self.actual_frame + 1) % 19
            self.image = self.image_tab[self.actual_frame]

    def update(self):
        self.turn()

class Mob(MySprite):
    def __init__(self, game, x, y, tile):
        
        self.image = resize(pg.image.load(
            path.join(npc_folder, f'{1}.png')), CHARACTER_SIZE)
        self.rect = self.image.get_rect()
        super(Mob,self).__init__(game, x, y, tile)
        self.hp = 10
        # self.rect.center = (x, y)
        # self.hit_rect = MOB_HIT_RECT.copy()
        # self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.aim = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = 100
        self.speed = 250
        self.is_moving = False

        self.groups = game.Layers[6], game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)

        self.time_since_anime = 0
        self.actual_frame = 1
        self.looking_at = "Bot"
        self.walk_right = [(pg.image.load(path.join(mob1_folder, f'r{x}.png'))) for x in range(0, 3)] 
        self.walk_left = [(pg.image.load(path.join(mob1_folder, f'l{x}.png'))) for x in range(0, 3)]
        self.walk_top = [(pg.image.load(path.join(mob1_folder, f't{x}.png'))) for x in range(0, 3)]
        self.walk_bot = [(pg.image.load(path.join(mob1_folder, f'b{x}.png'))) for x in range(0, 3)]
    
    
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
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.obstacle, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def IA(self):
        if(abs(self.game.player.pos.x - self.pos.x) < 4 * TILESIZE and 
        abs(self.game.player.pos.y - self.pos.y) < 4 * TILESIZE):
            self.is_moving = True
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        else:
            self.is_moving = False

    def look_update(self):
        if self.vel.x >= 0:
            if self.vel.y >= 0 and self.vel.y > self.vel.x:
                self.looking_at = "Bot"
            elif self.vel.y < 0 and abs(self.vel.y) > self.vel.x:
                self.looking_at = "Top"
            else:
                self.looking_at = "Right"
        elif self.vel.x < 0:
            if self.vel.y >= 0 and self.vel.y > abs(self.vel.x):
                self.looking_at = "Bot"
            elif self.vel.y < 0 and abs(self.vel.y) > abs(self.vel.x):
                self.looking_at = "Top"
            else:
                self.looking_at = "Left"
        self.animation()

    def animation(self):
        now = pg.time.get_ticks()
        if(now> self.time_since_anime + 150):
            self.time_since_anime = now
            if(self.is_moving == True):
                self.actual_frame = (self.actual_frame + 1) % 3
            else:
                self.actual_frame = 1
            if(self.looking_at == 'Right'):
                self.image = self.walk_right[self.actual_frame]
            elif(self.looking_at == 'Left'):
                self.image = self.walk_left[self.actual_frame]
            elif(self.looking_at == 'Top'):
                self.image = self.walk_top[self.actual_frame]
            elif(self.looking_at == 'Bot'):
                self.image = self.walk_bot[self.actual_frame]
        self.image = resize(self.image, CHARACTER_SIZE)

    def update(self):
        self.IA()
        self.rect.center = self.pos
        if self.is_moving:
            self.aim = vec(1, 0).rotate(-self.rot)
            self.aim.scale_to_length(self.speed)
            self.aim += self.vel * -1
            self.vel += self.aim * self.game.dt
            self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.collide_with_obstacle('x')
        self.rect.y = self.pos.y
        self.collide_with_obstacle('y')
        self.look_update()
        if(self.vel == (0, 0)):
            self.is_moving = False

        if self.hp <= 0:
            self.kill()

class NPC(MySprite):
    def __init__(self, game, x, y, tile):
        img = tile//10 % 10
        self.image = resize(pg.image.load(
            path.join(npc_folder, f'{img}.png')), CHARACTER_SIZE)
        self.rect = self.image.get_rect()
        super(NPC,self).__init__(game, x, y, tile)

        self.groups = game.Layers[5], game.obstacle
        pg.sprite.Sprite.__init__(self, self.groups)

class Collectable(MySprite):
    def __init__(self, game, x, y, tile):
        self.ID = tile//100
        self.item = ITEM_DICT[self.ID]
        self.image = resize(pg.image.load(
            path.join(item_folder, f'i ({self.ID}).png')), CHARACTER_SIZE)
        self.rect = self.image.get_rect()
        super(Collectable,self).__init__(game, x, y, tile)
        Collectable_area(game, x, y, self)

        self.groups = game.Layers[6]
        pg.sprite.Sprite.__init__(self, self.groups)

class Interactif(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # super(Interactif,self).__init__(game, x, y)
        self.groups = game.interactif
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x-1
        self.y = y-1
        self.rect = pg.Rect((self.x) * TILESIZE, (self.y) *
                            TILESIZE, TILESIZE*2, TILESIZE*2)
        

class Collectable_area(Interactif):
    def __init__(self, game, x, y, sprite):
        super(Collectable_area, self).__init__(game, x, y)
        self.sprite = sprite
        self.key = pg.K_e

    def interaction(self, player):
        self.sprite.kill()
        player.inv.add_without_case(self.sprite.item)
        self.kill()

class Save_area(Interactif):
    def __init__(self, game, x, y, ID):
        super(Save_area, self).__init__(game, x, y)
        self.key = pg.K_e

    def interaction(self, player):
        self.game.save()
class Chest_area(Interactif):
    def __init__(self, game, x, y, ID, items=None):
        super(Chest_area, self).__init__(game, x, y)
        self.key = pg.K_e
        self.shop = Screen_shop(game.screen, game, 0)
        if items:
            self.shop.put_in_shop(items)

    def interaction(self, player):
        self.shop.run(self.game.screen.copy(), player)

class Shop_area(Interactif):
    def __init__(self, game, x, y, ID):
        super(Shop_area, self).__init__(game, x, y)
        self.key = pg.K_e
        self.shop = Screen_shop(game.screen, game, ID)

    def interaction(self, player):
        self.shop.run(self.game.screen.copy(), player)


class Quest_area(Interactif):
    def __init__(self, game, x, y, ID):
        super(Quest_area, self).__init__(game, x, y)
        self.key = pg.K_e
        self.quest = QUEST_DICT[ID]
        self.dialogue = Dialogue(game, self, self.quest)

    def interaction(self, player):
        self.dialogue.linkwith(player)
        self.dialogue.run(self.game.screen.copy())

    def accept(self, player):
        if self.quest and not self.quest in player.quest_list:
            player.quest_list.append(self.quest)
        elif self.quest and self.quest.is_complete(player):
            self.quest.congrats(player)
            self.quest = None






