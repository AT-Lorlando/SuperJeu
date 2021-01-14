import Hex as hx
from CombatCharacter import *
class Spell :
    owner = None
    championClasse = None
    castzone = [hx.Hex()] #relative
    dammagezone = [hx.Hex()]  #relative
    surtuile = None
    name=None
    offsetx=0
    offsety=0
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
        return
    
    def computecastzone(self,Grid,caster):
        return [elmt for elmt in list(map((lambda x: caster + x), self.castzone)) if elmt in Grid and (Grid[Grid.index(elmt)].object==None or isinstance(Grid[Grid.index(elmt)].object,player))]
        
    def computedamagezone(self,Grid,target):
        return [elmt for elmt in list(map((lambda x: target + x), self.dammagezone)) if elmt in Grid and (Grid[Grid.index(elmt)].object==None or isinstance(Grid[Grid.index(elmt)].object,player)) ]


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
        tuile.object.healthpoint-=1
    return 

def thunder_dammage(owner, tuile) :
    #if tuile.object in Characters :
    if isinstance(tuile.object,player):
        tuile.object.deal_damage(1)
    return 

""" fireball = Spell(fireball_dammage)
fireball.dammagezone = hx.hex_circle(hx.Hex(),1)
fireball.castzone= hx.hex_circle((hx.Hex(), 3))
fireball.name=fireball """

fireball=""

thunder = Spell(thunder_dammage)
thunder.dammagezone= hx.hex_circle(hx.Hex(), 2)
thunder.castzone = hx.hex_circle(hx.Hex(), 3)
thunder.offsetx=30
thunder.offsety=35