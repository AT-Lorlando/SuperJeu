import pygame as pg
from settings import *

class Spell (pg.sprite.Sprite):
    def __init__(self, character):
        self.groups = character.spell
        pg.sprite.Sprite.__init__(self, self.groups)
        self.range = 0
        self.dmg = 0
        self.aoe = (0,0,0)
        self.radius_dmg = 0 #0->100
        self.cooldown = 0

        #All images
        self.traveling = None
        self.hiting = None
    
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


class Spell_wizard(Spell):
    def __init__(self) :
        super(Spell_wizard,self).__init__()

class Spell_warrior(Spell):
    def __init__(self) :
        super(Spell_wizard,self).__init__()

class Spell_rogue(Spell):
    def __init__(self) :
        super(Spell_wizard,self).__init__()