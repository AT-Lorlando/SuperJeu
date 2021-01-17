import Hex as hx
from CombatCharacter import *
class Spell :
    name=""
    owner = None
    championClasse = None
    castzone = [hx.Hex()] #relative
    dammagezone = [hx.Hex()]  #relative
    surtuile = None
    name=None
    offsetx=0
    offsety=0
    manacost=0
    """ countdown=0
    spell=[False,False] #Thunder #... """

    def cast(self,Grid, position):
        hex_touched = []
        for hexes in self.dammagezone:
            hex_touched.append(position+hexes)
        tuiles_touches=[]
        for hexes in hex_touched :
            if hexes in Grid:
                tuiles_touches.append(Grid[Grid.index(hexes)])
        for tuiles in tuiles_touches :
            self.surtuile(self.owner,tuiles)
            hx.update_grid(Grid,tuiles)
        self.owner.mana-=self.manacost
        return
    
    def computecastzone(self,Grid,caster):
        return [elmt for elmt in list(map((lambda x: caster + x), self.castzone)) 
        if elmt in Grid and (Grid[Grid.index(elmt)].object==None or isinstance(Grid[Grid.index(elmt)].object,player))]
        
    def computedamagezone(self,Grid,target):
        return [elmt for elmt in list(map((lambda x: target + x), self.dammagezone)) 
        if elmt in Grid and (Grid[Grid.index(elmt)].object==None or isinstance(Grid[Grid.index(elmt)].object,player)) ]


    def __init__(self, fc) :
        self.surtuile = fc

    """ def draw_spell(self,screen,spellnum,count,position):
        if self.countdown==count:
            self.spell[spellnum]=False
            self.countdown=0
        elif spell[spellnum] and self.countdown<count:
            screen.blit(self.name[self.countdown],position)
            self.countdown += 1 """


def fireball_dammage(owner, tuile) :
    if tuile.object in Characters :
        tuile.object.healthpoint-=50
    return 

def thunder_dammage(owner, tuile) :
    #if tuile.object in Characters :
    if isinstance(tuile.object,player):
        tuile.object.deal_damage(40)
    return 

def sunburn_dammage(owner, tuile) :
    #if tuile.object in Characters :
    if isinstance(tuile.object,player):
        tuile.object.deal_damage(25)
    return 

def attack_dammage(owner,tuile):
    if isinstance(tuile.object,player):
        tuile.object.deal_damage(10)
    return 

def bomb_dammage(owner,tuile):
    if isinstance(tuile.object,player):
        tuile.object.deal_damage(70)
    return 

def heal_dammage(owner,tuile):
    if isinstance(tuile.object,player):
        tuile.object.deal_damage(-20)
    return 


""" fireball = Spell(fireball_dammage)
fireball.dammagezone = hx.hex_circle(hx.Hex(),1)
fireball.castzone= hx.hex_circle((hx.Hex(), 3))
fireball.name=fireball """

fireball=""

sunburn = Spell(thunder_dammage)
sunburn.name="sunburn"
sunburn.dammagezone=hx.hex_circle(hx.Hex(), 1)
sunburn.castzone = hx.hex_circle(hx.Hex(),3)
sunburn.manacost=2


thunder = Spell(thunder_dammage)
thunder.dammagezone=hx.hex_circle(hx.Hex(), 2)
thunder.castzone = hx.hex_circle(hx.Hex(), 4)
thunder.offsetx=31
thunder.offsety=35
thunder.manacost=4
thunder.name="thunder"


bomb = Spell(bomb_dammage)
bomb.name="bomb"
bomb.dammagezone=hx.hex_circle(hx.Hex(), 2)
bomb.castzone = hx.hex_circle(hx.Hex(),3)
bomb.manacost=2

heal=Spell(heal_dammage)
heal.name="heal"
heal.dammagezone=hx.hex_circle(hx.Hex(),1)
heal.castzone = hx.hex_circle(hx.Hex(),3)
heal.manacost=2

attack = Spell(attack_dammage)
attack.dammagezone=hx.hex_circle(hx.Hex(),1)
attack.castzone= hx.hex_circle(hx.Hex(),2)
attack.manacost=1
attack.offsetx=Gobelincombathorizontalshift
attack.offsety=Gobelincombatverticalshift
attack.name="attack"