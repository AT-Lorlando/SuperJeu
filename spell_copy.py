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
            tuiles_touches.append(Grid[Grid.index(hexes)])
        for tuiles in tuiles_touches :
            self.surtuile(self.owner,tuiles)
            hx.update_grid(Grid,tuiles)
        return


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