import Hex as hx
class Spell :
    owner = None
    castzone = [hx.Hex()]
    dammagezone = [hx.Hex()]  #relative
    def dammage_compute(self,Grid, position):
        hex_touched = []
        for hexes in self.dammagezone:
            tile_touched.append(position+hexes)
        for hexes in hex_touched :