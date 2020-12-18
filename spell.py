import pygame as pg
from settings import *
vec = pg.math.Vector2


class Spell (pg.sprite.Sprite):
    def __init__(self, player):
        self.game = player.game
        self.player = player
        self.groups = self.game.Layers[6]
        pg.sprite.Sprite.__init__(self, self.groups)
        self.range = 0
        self.dmg = 0
        self.aoe = (0,0,0)
        self.radius_dmg = 0 #0->100
        self.cooldown = 0
        self.vel = vec(0, 0)
        self.pos = player.pos
        
        #All images
        self.image = pg.Surface((CHARACTER_SIZE, CHARACTER_SIZE))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect

        self.pos = vec(self.pos)
        self.rect.center = self.pos

        self.time_since_anime = 0
        self.actual_frame = 0
        self.angle = 0
        self.traveling = False
        self.hiting = False

        self.explodes_images = None
        self.traveling_images = None

    def launch(self):
        if self.range:
            if(self.player.looking_at == "Right"):
                self.vel = vec(300,0)
                self.angle = 0
            elif(self.player.looking_at == "Left"):
                self.vel = vec(-300,0)
                self.angle = 180
            elif(self.player.looking_at == "Top"):
                self.vel = vec(0,-300)
                self.angle = 90
            elif(self.player.looking_at == "Bot"):
                self.vel = vec(0,300)
                self.angle = 270
        self.traveling = True
    
    def collide(self):
        return pg.sprite.spritecollide(self, self.game.obstacle, False)

    def hit(self, sprite_group = None):
        # print("hit")        
        if sprite_group:
            self.vel = vec(0,0)
            self.hiting = True
            self.actual_frame = 0
            self.explode()
            for sprite in sprite_group:
                self.make_effect(sprite)
            self.kill()
            print("Fireball killed")

    def make_effect(self, sprite):
        if sprite.hp:
            sprite.hp -= 1
        print(sprite, "Hited", sprite.hp)

    def explode(self):
        self.game.animation_add(self, self.explodes_images)
        print("Pfiou EXPLOSION")

    def update(self):
        now = pg.time.get_ticks()
        if(now> self.time_since_anime + 50):
            self.time_since_anime = now
            self.actual_frame = (self.actual_frame + 1) % 8
        if self.traveling:
            self.image = pg.transform.rotate(self.traveling_images[self.actual_frame],self.angle)
            self.rect = self.image.get_rect()
            self.hit_rect = self.rect
        if self.hiting:
            self.image = self.explodes_images[self.actual_frame]
            self.rect = self.image.get_rect()
            self.hit_rect = self.rect
        self.image.set_colorkey((223,222,223))
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.hit(self.collide())

class Fireball(Spell):
    def __init__(self, character):
        super(Fireball,self).__init__(character)
        print("Fire ball creating")
        self.range = 5
        self.dmg = 5
        self.hp = -1        

        self.image = pg.Surface((CHARACTER_SIZE, CHARACTER_SIZE))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect

        self.traveling_images = [pg.transform.scale(
            (pg.image.load(path.join(spell_folder, f's ({x}).gif'))),(48,48)) for x in range(37, 45)]
        self.explodes_images = [pg.transform.scale(
            (pg.image.load(path.join(spell_folder, f'1 ({x}).gif'))),(48,48)) for x in range(38, 48)]
        self.launch()

    # def hexTouched(self,pos_x,pos_y,x_map,y_map):
    #     tab=[]
    #     for case in self.zone :
    #         if (0 <= pos_x + case(0) < x_map) and  (0 <= pos_x + case(1) < y_map) : # check if the case is in the map
    #             tab.append((pos_x+case(0), pos_y+case(1)))
    #     return tab # return a table with the hex which exists

    # def isPressed(self,key_pressed):
    #     if self.key == key_pressed :
    #         return True

    # def isUsed(self):
    #     self.countdown = self.cooldown
    
    # def turnPassed(self):
    #     self.countdown -=1 #need to make a loop to apply this method to all the spell


# class Spell_wizard(Spell):
#     def __init__(self) :
#         super(Spell_wizard,self).__init__()

# class Spell_warrior(Spell):
#     def __init__(self) :
#         super(Spell_wizard,self).__init__()

# class Spell_rogue(Spell):
#     def __init__(self) :
#         super(Spell_wizard,self).__init__()