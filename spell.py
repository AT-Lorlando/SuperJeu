class Spell ():
    def __init__(self,zone,key,cooldown):
        self.zone = zone # zone is a table of the affected hex in relatif point of view (ex : (0,0) if the spell affects only one case) 
        self.key = key
        self.cooldown = cooldown 
        self.countdown
    
    def hexTouched(self,pos_x,pos_y):
        return [(pos_x+self.zone.x,pos_y+self.zone.y) for each_case in self.zone]

    def isPressed(self,key_pressed):
        if self.key == key_pressed :
            return True

    def isUsed(self):
        self.countdown = self.cooldown
    
    def turnPassed(self):
        self.countdown -=1



class Spell_wizard(Spell):
    def __init__(self,dmg,STR,DEX,CON,INT,WIS,CHA) :
        super(Spell_wizard,self).__init__()
        self.base_dmg = dmg
        self.true_dmg = self.base_dmg * WIS
        self.heal = False

    def isHeal(self):
        self.heal= True


class Spell_warrior(Spell):
    def __init__(self,dmg,STR,DEX,CON,INT,WIS,CHA) :
        super(Spell_wizard,self).__init__()
        self.base_dmg = dmg

class Spell_rogue(Spell):
    def __init__(self,dmg,STR,DEX,CON,INT,WIS,CHA) :
        super(Spell_wizard,self).__init__()
        self.base_dmg = dmg