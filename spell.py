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
        self.pos = vec(player.pos)
        
        #All images
        self.image = pg.Surface((CHARACTER_SIZE, CHARACTER_SIZE))
        self.rect = self.image.get_rect()

        self.rect.center = self.pos

        self.time_since_anime = 0
        self.actual_frame = 0
        self.angle = 0
        self.traveling = False

        self.explodes_images = None
        self.traveling_images = None

    def launch(self):
        if self.range:
            if(self.player.looking_at == "Right"):
                self.pos += vec(TILESIZE//2,0)
                self.vel = vec(300,0)
                self.angle = 0
            elif(self.player.looking_at == "Left"):
                self.pos += vec(-TILESIZE//2,0)
                self.vel = vec(-300,0)
                self.angle = 180
            elif(self.player.looking_at == "Top"):
                self.pos += vec(0,-TILESIZE//2)
                self.vel = vec(0,-300)
                self.angle = 90
            elif(self.player.looking_at == "Bot"):
                self.pos += vec(0,TILESIZE//2)
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

    def make_effect(self, sprite):
        if sprite.hp:
            sprite.hp -= 1

    def explode(self):
        self.game.animation_add(self.explodes_images, self, colorkey=(223,222,223))

    def update(self):
        now = pg.time.get_ticks()
        if(now> self.time_since_anime + 50):
            self.time_since_anime = now
            self.actual_frame = (self.actual_frame + 1) % len(self.traveling_images)
        if self.traveling:
            self.image = pg.transform.rotate(self.traveling_images[self.actual_frame],self.angle)
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