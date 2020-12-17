from math import sqrt, pi, cos, sin


class Hex:
    """
    This class represents a tile of the hexagonal grid
    """
    def __init__(self, q=0, r=0, s=None):
        self.q = q
        self.r = r
        self.s = (s if s != None else int(-q - r))
        assert self.s + self.q + self.r == 0, "The sum of the 3 coordinates should be equal to 0!"  #condition so that all the hexagons are in the same plan

    def __repr__(self):
        return f"{self.q} {self.r} {self.s}"

    def __eq__(self, other):
        return self.q == other.q and self.r == other.r and self.s == other.s

    def __add__(self, other):
        return Hex(self.q + other.q, self.r + other.r, self.s + other.s)

    def __sub__(self, other):
        return Hex(self.q - other.q, self.r - other.r, self.s - other.s)

    def __mul__(self, x):
        return Hex(self.q * x, self.r * x, self.s * x)

    def __rmul__(self, x):
        return self * x

    def neighbor(self, direction):
        """
        Return the nearest tile in the selected direction. Direction 0 is on the right side, continuing clockwise
        """
        direction %= 6
        return self + axial_hex_directions[direction]

    def neighbors(self):
        """
        Return all the neighbors of a tile in a list, starting from the one on the right side
        """
        return [self.neighbor(i) for i in range(6)]


axial_hex_directions = [
    Hex(1, 0),
    Hex(0, 1),
    Hex(-1, 1),
    Hex(-1, 0),
    Hex(0, -1),
    Hex(1, -1)
]  #clockwise orientation, starting from the hexagon on the right


def length_hex(hex):
    """
    Returns the Manhattan distances between a tile and the 0 0 0 tile
    """
    return (abs(hex.q) + abs(hex.r) +
            abs(hex.s)) / 2  #(divided by 2 because we work with hexagons)


def distance_hex(hex1, hex2):
    """
    Returns the Manhattan distances between two tiles
    """
    return length_hex(hex1 - hex2)


def rounding_hex(q, r, s):
    rq, rr, rs = round(q), round(r), round(s)
    diff_q, diff_r, diff_s = abs(rq - q), abs(rr - r), abs(rs - s)
    if diff_q > diff_r and diff_q > diff_s:
        rq = -rr - rs
    elif diff_r > diff_s:
        rr = -rq - rs
    else:
        rs = -rq - rr
    return Hex(rq, rr, rs)

class Tile(Hex) :
    object=None

    def __repr__(self):
        return f"{self.q} {self.r} {self.s} ({self.object})"

    def set_object(self, object) :
        self.object = object
        return self

    def remove_object(self) :
        obj = self.object
        self.object= None
        return obj

def hex_circle(hex,r, fill=True) :
    res=[]
    for x in range(-r+1,r) :
        for y in range(max(-r,-x-r)+1,min(r,-x+r)):
            z=-x-y
            res.append(hex+Hex(x,y,z))
    if not fill:
        resp = hex_circle(hex,r-1, True)
        for h in resp :
            res.remove(h)
    return res

def lerp(a,b,t) :
    return a+(b-a)*t

def lerp_hex(hex1,hex2,t) :
    return Hex(lerp(hex1.x,hex2.x,t),lerp(hex1.y,hex2.y,t),lerp(hex1.z,hex2.z,t))

def hex_linedraw(hex1,hex2) :
    l = distance_hex(hex1,hex2)
    hex1+= Hex(1e-6,1e-6)#We "deviate" hex1 so we never have points on the limite between two hexs
    res=[]
    for i in range(0,l+1) :
        res.append(rounding_hex(hex1,hex2,1.0/l * i))
    return res

class Orientation:
    """
    This represent the orientations of the hexagons in the grid
    """
    def __init__(self, f0, f1, f2, f3, b0, b1, b2, b3, start_angle):
        self.f0, self.f1, self.f2, self.f3 = f0, f1, f2, f3  #Artificial matrix of forward direction (hex to pixels) : in cartesian coordinates, this would be : 0 , 1 , 1, 0 (the two vectors (0,1) and (1,0))
        self.b0, self.b1, self.b2, self.b3 = b0, b1, b2, b3  #Matrix for getting back from pixels to hex
        self.start_angle = start_angle  #The starting angle of the orientation, in multiple of 60° (i.e. should be 0 for flat topped (0°) and 0.5 for pointy topped (30°)) !!! THIS ANGLE IS FROM THE X AXIS (or whatever its equivalent is in hex coordinates)


orientation_pointy = Orientation(sqrt(3),
                                 sqrt(3) / 2.0, 0.0, 3.0 / 2.0,
                                 sqrt(3) / 3.0, -1.0 / 3.0, 0.0, 2.0 / 3.0,
                                 0.5)

orientation_flat = Orientation(3.0 / 2.0, 0.0,
                               sqrt(3) / 2.0, sqrt(3), 2.0 / 3.0, 0.0,
                               -1.0 / 3.0,
                               sqrt(3) / 3.0, 0.0)


class Layout:
    def __init__(self, orientation, tuplesize, tupleorigin):
        self.orientation = orientation
        if orientation == orientation_pointy:
            self.sizex = tuplesize[0] / cos(
                pi / 6
            )  #Size of the half hexagons along x axis in PIXELS => /!\ cos here because we draw hexagons within circles
            self.sizey = tuplesize[1]
        if orientation == orientation_flat:
            self.sizex = tuplesize[
                0]  #Size of the hexagons along x axis in PIXELS
            self.sizey = tuplesize[1] / sin(
                pi /
                3)  #=> /!\ sin here because we draw hexagons within circles
        self.originx = tupleorigin[0]  #Origin coordinates in PIXELS
        self.originy = tupleorigin[1]


def hex_to_pixel(layout, hex):#return center (in px) of hex
    orientation = layout.orientation
    x = (orientation.f0 * hex.q +
         orientation.f1 * hex.r) * layout.sizex + layout.originx
    y = (orientation.f2 * hex.q +
         orientation.f3 * hex.r) * layout.sizey + layout.originy
    return (x, y)


def pixel_to_hex(layout, coord):
    """
    Returns the hex to which belongs the pixel at the coordinates "coord"
    """
    x, y = coord[0], coord[1]
    orientation = layout.orientation
    hexX = (x - layout.originx) / layout.sizex
    hexY = (y - layout.originy) / layout.sizey
    q = orientation.b0 * hexX + orientation.b1 * hexY
    r = orientation.b2 * hexX + orientation.b3 * hexY
    return rounding_hex(q, r, -q - r)


def corner_offset(layout, corner):
    corner = corner % 6
    sizex, sizey = layout.sizex, layout.sizey
    angle = 2 * pi * (layout.orientation.start_angle + corner) / 6
    return (sizex * cos(angle), sizey * sin(angle))


def hex_corner(layout, hex):
    """
    Returns all the corners of an hexagons (in tuple of coordinates in pixel)
    """
    center = hex_to_pixel(layout, hex)
    return [(round(center[0] + offset[0]), round(center[1] + offset[1]))
            for offset in [corner_offset(layout, i) for i in range(6)]]


def initgrid(x, y):
    """
    draw a rectangular hex grid with x the number of lines and y the number of "columns"
    """
    Grid = []
    k = 1
    for i in range(x):
        k += (i) % 2 - 1
        for j in range(k, y + k):
            Grid.append(Tile(j, i))
    return Grid

def update_grid(Grid, Tile) :
    if Tile in Grid :
        e = Grid[Grid.index(Tile)]
        Grid[Grid.index(Tile)] = Tile
        return e

class cell:
    def __init__(self, hex):
        self.hex = hex
        self.g = 0
        self.camefrom = None
        self.f = 0

    def reconstruct_path(self, path):

        path.insert(0, self.hex)
        if self.camefrom != None:
            return self.camefrom.reconstruct_path(path)
        else:
            return path

    def __repr__(self):
        return self.hex.__repr__()


def pathfinding(tilestart, tilegoal, Grid):#TO BE FIXED problem of grid pointer
    if tilestart not in Grid or tilegoal not in Grid :
        print("Error : Tiles not in grid")
        exit(-1)
    start = cell(tilestart)
    goal = cell(tilegoal)

    discovered = [start]
    explored = []
    start.f = start.g + distance_hex(start.hex, goal.hex)

    for tiles in Grid :
        if tiles.object != None :
            Grid.remove(tiles)

    while (discovered != []):
        min = discovered[0].f
        for cells in discovered:
            if cells.f <= min:
                min = cells.f
                current = cells

        if current.hex == goal.hex:
            path = []
            return current.reconstruct_path(path)
            #explored.append(current)
            #return explored

        discovered.remove(current)
        explored.append(current)

        for neigh in [cell(hex) for hex in current.hex.neighbors()]:
            if (neigh in explored) or (neigh.hex not in Grid):
                continue
            gtest = current.g + distance_hex(current.hex, neigh.hex)
            if (gtest < neigh.g) or (neigh not in discovered):
                neigh.camefrom = current
                neigh.g = gtest
                neigh.f = neigh.g + distance_hex(neigh.hex, goal.hex)
                if neigh not in discovered:
                    discovered.append(neigh)
    return -1


if __name__ == "__main__":
    l = Layout(orientation_flat, (1, 1), (0, 0))
    a = Hex(0, 0)
    print(a)
    #print (hex_corner(l,a))
    layout = Layout(orientation_pointy, (758, 876),
                    (758 / 2, 876 / 2))  #layout bizarre
    print(hex_corner(layout, a))
    cellulle = cell(Tile(0, 0))
    print(cellulle.hex.neighbors())
    assert Tile().object == None
    assert Tile().set_object("Object properly initialised").object == "Object properly initialised"
    gr= initgrid(2,2)
    print(gr)
    update_grid(gr,Tile(0,0).set_object("Test"))
    print(gr)
    print(pathfinding(Tile(1,1),Tile(1,0),gr))
    print(hex_circle(Hex(1,1),2,True))
    print(Tile()==Tile().set_object("test"))
    print("test grid")
    grid = [Tile(), Tile(1, 1).set_object("Clément2"), Tile(1, 2)]
    print(grid)
    print(
        pathfinding(
            Tile(), Tile(1,2),
            grid))
    print(grid)