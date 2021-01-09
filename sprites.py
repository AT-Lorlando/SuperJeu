from pygame.constants import K_y
import pygame as pg
from settings import *
from os import path
from Dungeon import *
from inventory_clem import *
from shop import *
from screen_shop import *
from dialogue import *
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
        self.image = resize(pg.image.load(
            path.join(floor_folder, f'{tile}.png')), TILESIZE)
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
        self.image = resize(pg.image.load(
            path.join(wall_folder, f'{tile}.png')), TILESIZE)
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
        print("Door tile:", tile)
        self.image = resize(pg.image.load(
            path.join(portal_folder, 'portal.png')), TILESIZE)
        self.rect = self.image.get_rect()
        super(Door,self).__init__(game, x, y, tile)
        self.groups = game.Layers[4], game.obstacle, game.doors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.door_type = 1
        self.instance_behind = (tile//10, tile%10) #Type,dif
        self.actual_frame = 1
        self.time_since_anime = 0

    def turn(self):
        self.time = pg.time.get_ticks()
        if(self.time > self.time_since_anime + 150):
            self.time_since_anime = self.time
            self.image = pg.transform.rotate(self.image, 90)

    def update(self):
        self.turn()


class Stair(MySprite):
    def __init__(self, game, x, y):
        self.image = resize(pg.image.load(
            path.join(portal_folder, 'portal.png')), TILESIZE)
        self.rect = self.image.get_rect()
        super(Stair,self).__init__(game, x, y)
        self.groups = game.Layers[4], game.obstacle, game.stairs
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.actual_frame = 1
        self.time_since_anime = 0
        self.portal = [(pg.image.load(
            path.join(portal_folder, f'{i}.png'))) for i in range(1, 4)]


    def turn(self):
        self.time = pg.time.get_ticks()
        if(self.time > self.time_since_anime + 150):
            self.time_since_anime = self.time
            self.image = pg.transform.rotate(self.image, 90)

    def update(self):
        self.turn()

class NPC(MySprite):
    def __init__(self, game, x, y, tile):
        img = tile//10
        self.image = resize(pg.image.load(
            path.join(npc_folder, f'{img}.png')), CHARACTER_SIZE)
        self.rect = self.image.get_rect()
        super(NPC,self).__init__(game, x, y, tile)

        self.groups = game.Layers[5], game.obstacle
        pg.sprite.Sprite.__init__(self, self.groups)

class Interactif(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # super(Interactif,self).__init__(game, x, y)
        self.groups = game.interactif
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect((x) * TILESIZE, (y) *
                            TILESIZE, TILESIZE*4, TILESIZE)
        self.x = x
        self.y = y

class Shop_area(Interactif):
    def __init__(self, game, x, y):
        super(Shop_area, self).__init__(game, x, y)

        self.key = pg.K_e
        self.shop = Screen_shop(game.screen, game)

    def interaction(self, player):
        self.shop.run(self.game.screen.copy(), player)


class Quest_area(Interactif):
    def __init__(self, game, x, y):
        super(Quest_area, self).__init__(game, x, y)
        self.key = pg.K_e
        self.quest = Gime_apple
        self.dialogue = Dialogue(game, self,"Bonjour M.Hugo", "Désolé, je ne peux pas trop vous parler", "Je dois absolument faire la récolte de mon champ !", "Malheureusement, je viens de casser ma pelle...","Pouvez vous allez m'en acheter une ?", "Le marchand se trouve juste à gauche !",  "Je vous recompenserais !")

    def interaction(self, player):
        self.dialogue.linkwith(player)
        self.dialogue.run(self.game.screen.copy())

    def accept(self, player):
        if self.quest and not self.quest in player.quest_list:
            player.quest_list.append(self.quest)
        elif self.quest and self.quest.is_complete(player):
            self.quest.congrats(player)
            self.quest = None

class Quest():
    def __init__(self, ID,rewards_tab):
        self.ID = ID
        self.rewards = rewards_tab    
        self.xp = 500
        self.money = 500

    def give_rewards(self, player):
        for reward in self.rewards:
            player.inv.add_without_case(reward)
        player.gain_money(self.money)
        player.gain_xp(self.xp)

    def give_up(self, player):
        if self in player.quest_list:
            player.quest_list.remove(self)
        
    def is_complete(self, player):
        pass

class Lost_Item_Quest(Quest):
    def __init__(self, ID, rewards_tab, needed_tab):
        super(Lost_Item_Quest,
        self).__init__(ID,rewards_tab)
        self.needed = needed_tab
        self.goal = "You have to find the Losted ring in the first dungeon."

    def is_complete(self, player):
        return any([player.inv.is_in(item) for item in self.needed])

    def congrats(self, player):
        self.give_rewards(player)
        for item in self.needed:
            player.inv.remove(item)
            print("removed", item)
        player.quest_list.remove(self)

Gime_apple = Lost_Item_Quest(1, [Empowered_Sword],[Apple])
Losted_ring_Quest = Lost_Item_Quest(2, [Empowered_Staff],[Lost_ring])






