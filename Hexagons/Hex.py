

class Hex:
    def __init__(self, q=0,r=0, s=None) :
        self.q=q
        self.r=r
        self.s= (s if s!=None else int(-q-r))
        assert self.s+self.q+self.r==0 , "The sum of the 3 coordinates should be equal to 0!"#condition so that all the hexagons are in the same plan

    def __eq__(self, other) :
        return self.q==other.q and self.r==other.r and self.s==other.s

    def __add__(self, other) :
        return Hex(self.q+other.q,self.r+other.r,self.s+other.s)

    def __sub__(self, other) :
        return Hex(self.q-other.q,self.r-other.r,self.s-other.s)

    def __mul__(self, x) :
        return Hex(self.q*x,self.r*x,self.s*x)
    
    def __rmul__(self, x) :
        return self * x

    def neighbor(self, direction) :
        assert 0<=direction<6
        return self+axial_hex_directions[direction]
    
    def neighbors(self) :
        return [self.neighbor(i) for i in range(6)]

axial_hex_directions = [Hex(1,0),Hex(0,1),Hex(-1,1),Hex(-1,0),Hex(0,1),Hex(1,-1)] #clockwise orientation, starting from the hexagon on the right

def length(hex) :
        return (abs(hex.q)+abs(hex.r)+abs(hex.s))/2 #Manhattan distance between two cubes (divided by 2 because we work with hexagons)
    
def distance(hex1, hex2) :
        return length(hex1-hex2)



a=Hex(1,2)
print(f"{a.q} {a.r} {a.s}")
a=2*a
print(f"{a.q} {a.r} {a.s}")