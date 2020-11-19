from math import sqrt, pi, cos, sin

class Hex:
    """
    This class represents a tile of the hexagonal grid
    """
    def __init__(self, q=0,r=0, s=None) :
        self.q=q
        self.r=r
        self.s= (s if s!=None else int(-q-r))
        assert self.s+self.q+self.r==0 , "The sum of the 3 coordinates should be equal to 0!"#condition so that all the hexagons are in the same plan

    def __repr__(self):
        return f"{self.q} {self.r} {self.s}"

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
        """
        Return the nearest tile in the selected direction. Direction 0 is on the right side, continuing clockwise
        """
        direction %=5
        return self+axial_hex_directions[direction]

    def neighbors(self) :
        """
        Return all the neighbors of a tile in a list, starting from the one on the right side
        """
        return [self.neighbor(i) for i in range(6)]

axial_hex_directions = [Hex(1,0),Hex(0,1),Hex(-1,1),Hex(-1,0),Hex(0,1),Hex(1,-1)] #clockwise orientation, starting from the hexagon on the right

def length_hex(hex) :
    """
    Returns the Manhattan distances between a tile and the 0 0 0 tile
    """
    return (abs(hex.q)+abs(hex.r)+abs(hex.s))/2 #(divided by 2 because we work with hexagons)

def distance_hex(hex1, hex2) :
    """
    Returns the Manhattan distances between two tiles
    """
    return length_hex(hex1-hex2)

def rounding_hex(q,r,s):
    rq, rr, rs = round(q), round(r), round(s)
    diff_q, diff_r, diff_s = abs(rq - q), abs(rr - r), abs(rs - s)
    if diff_q>diff_r and diff_q>diff_s :
        rq = -rr-rs
    elif diff_r>diff_s :
        rr = -rq -rs
    else :
        rs = -rq -rr
    return Hex(rq,rr,rs)


class Orientation:
    """
    This represent the orientations of the hexagons in the grid
    """
    def __init__(self,
    f0,f1,f2,f3,
    b0,b1,b2,b3,
    start_angle):
        self.f0,self.f1,self.f2,self.f3=f0,f1,f2,f3 #Artificial matrix of forward direction (hex to pixels) : in cartesian coordinates, this would be : 0 , 1 , 1, 0 (the two vectors (0,1) and (1,0))
        self.b0,self.b1,self.b2,self.b3=b0,b1,b2,b3 #Matrix for getting back from pixels to hex
        self.start_angle = start_angle #The starting angle of the orientation, in multiple of 60° (i.e. should be 0 for flat topped (0°) and 0.5 for pointy topped (30°)) !!! THIS ANGLE IS FROM THE X AXIS (or whatever its equivalent is in hex coordinates)


orientation_pointy = Orientation(
                            sqrt(3), sqrt(3)/2.0, 0.0, 3.0/2.0,
                            sqrt(3)/3.0,  -1.0/3.0, 0.0, 2.0/3.0,
                            0.5)

orientation_flat = Orientation(
                            3.0 / 2.0, 0.0, sqrt(3) / 2.0, sqrt(3),
                            2.0 / 3.0, 0.0,  -1.0 / 3.0, sqrt(3) / 3.0,
                            0.0)

class Layout :
    def  __init__(self, orientation,tuplesize, tupleorigin) :
        self.orientation=orientation
        if orientation==orientation_pointy :
            self.sizex = tuplesize[0]/cos(pi/6) #Size of the hexagons along x axis in PIXELS => /!\ cos here because we draw hexagons within circles
            self.sizey=tuplesize[1]
        if orientation==orientation_flat :
            self.sizex = tuplesize[0] #Size of the hexagons along x axis in PIXELS
            self.sizey=tuplesize[1]/sin(pi/3)#=> /!\ sin here because we draw hexagons within circles
        self.originx=tupleorigin[0] #Origin coordinates in PIXELS
        self.originy=tupleorigin[1]

def hex_to_pixel(layout, hex) :
    orientation = layout.orientation
    x = (orientation.f0 * hex.q + orientation.f1 * hex.r) * layout.sizex +layout.originx
    y = (orientation.f2 * hex.q + orientation.f3 * hex.r) * layout.sizey +layout.originy
    return (x, y)

def pixel_to_hex(layout,coord):
    x,y = coord[0], coord[1]
    orientation = layout.orientation
    hexX = (x - layout.originx) / layout.sizex
    hexY = (y - layout.originy) / layout.sizey
    q = orientation.b0 * hexX + orientation.b1 * hexY
    r = orientation.b2 * hexX + orientation.b3 * hexY
    return rounding_hex(q,r,-q-r)

def corner_offset(layout, corner) :
    corner=corner%6
    sizex,sizey=layout.sizex,layout.sizey
    angle = 2*pi* (layout.orientation.start_angle+corner)/6
    return (sizex*cos(angle), sizey*sin(angle))

def hex_corner(layout, hex) :
    center=hex_to_pixel(layout, hex)
    return [(round(center[0]+offset[0]),round(center[1]+offset[1])) for offset in [corner_offset(layout,i) for i in range(6)]]

if __name__ == "__main__":
    l = Layout(orientation_flat,(1,1),(0,0))
    a=Hex(0,0)
    print(a)
    #print (hex_corner(l,a))
    layout=Layout(orientation_pointy,(758,876),(758/2,876/2)) #layout bizarre
    print (hex_corner(layout,a))
    #grille rectangle
    x=1
    for y in range(7) :
        x+=(y)%2 -1
        for z in range(x,7+x):
            8
            #print(z,y)