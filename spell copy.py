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
        tuiles_touches=[]
        for hexes in hex_touched :
            tuiles_touches.append(Grid[Grid.index(hexes)])
        for tuiles in tuiles_touches :
            self.surtuile(self.owner,tuiles)
        return


    def __init__(self, fc) :
        self.surtuile = fc


def fireball_dammage(owner, tuile) :
    if tuile.object in Characters :
        tuile.object.healthpoint-=1
    return 

fireball = Spell(fireball_dammage)
fireball.dammagezone = hx.hex_circle(hx.Hex(),1)
fireball.castzone= hx.hex_circle(hx.hex_circle(Hex(), 3))
