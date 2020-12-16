class Spell ():
    def __init__(self,zone,key,cooldown):
        self.zone = zone # zone is a table of the affected hex in relatif point of view (ex : (0,0) if the spell affects only one case) 
        self.key = key #the key on the keyboard
        self.cooldown = cooldown # base stat of the spell
        self.countdown # remaining rounds
    
    def hexTouched(self,pos_x,pos_y,x_map,y_map):
        tab=[]
        for case in self.zone :
            if (0 <= pos_x + case(0) < x_map) and  (0 <= pos_x + case(1) < y_map) : # check if the case is in the map
                tab.append((pos_x+case(0), pos_y+case(1)))
        return tab # return a table with the hex which exists

    def isPressed(self,key_pressed):
        if self.key == key_pressed :
            return True

    def isUsed(self):
        self.countdown = self.cooldown
    
    def turnPassed(self):
        self.countdown -=1 #need to make a loop to apply this method to all the spell



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