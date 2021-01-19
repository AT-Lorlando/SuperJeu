import Hex as hx
from CombatCharacter import *
class Spell :
    name=""
    owner = None
    championClasse = None
    castzone = [hx.Hex()] #relative
    castrange = 0
    dammagezone = [hx.Hex()]  #relative
    surtuile = None
    name=None
    offsetx=31
    offsety=35
    manacost=0
    dammage=0
    cooldown=0
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
            self.surtuile(self.owner,tuiles,self.dammage)
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


def dammage(owner, tuile,dammage) :
    #if tuile.object in Characters :
    if isinstance(tuile.object,player):
        tuile.object.deal_damage(dammage)
    return 


""" fireball = Spell(fireball_dammage)
fireball.dammagezone = hx.hex_circle(hx.Hex(),1)
fireball.castzone= hx.hex_circle((hx.Hex(), 3))
fireball.name=fireball """

def initspell(spell,name,dammage,dammagerange,castrange,manacost,cooldown):
    spell.cooldown=cooldown
    spell.dammage=dammage
    spell.name=name
    spell.dammagerange=dammagerange
    spell.dammagezone=hx.hex_circle(hx.Hex(), spell.dammagerange)
    spell.castrange=castrange
    spell.castzone = hx.hex_circle(hx.Hex(),spell.castrange)
    spell.manacost=manacost
    return spell

sunburn = Spell(dammage)
sunburn = initspell(sunburn,"Sunburn",20,1,3,2,1)

thunder = Spell(dammage)
thunder = initspell(thunder,"Thunder",40,2,4,4,3)


bomb = Spell(dammage)
bomb = initspell(bomb,"Bomb",70,2,3,2,2)

heal=Spell(dammage)
heal = initspell(heal,"Heal",-20,1,2,2,1)

attack = Spell(dammage)
attack= initspell(attack,"Attack",10,1,2,1,1)