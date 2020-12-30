import Hex as hx
class Spell :
    owner = None
    championClasse = None
    castzone = [hx.Hex()] #relative
    dammagezone = [hx.Hex()]  #relative
    surtuile = None

    def cast(self,Grid, position):
        hex_touched = []
        for hexes in self.dammagezone:
            hex_touched.append(position+hexes)
        for hexes in hex_touched :
            #To-do : hex to tiles
            tuiles_touches = []
            pass
        for tuiles in tuiles_touches :
            self.surtuile(self.owner,tuiles)
        return


    def __init__(self, fc) :
        self.surtuile = fc
        self.surtuile("","")


def boule_de_feu(owner, tuile) :
    # dmg = owner.int * 5
    # tuile.object.hp -= dmg
    print("cc")
    return 

bdf = Spell(boule_de_feu)