import numpy
import random

#find the rooms which exist in the map
def find_room(map):
    tab = []
    for x in range(0, len(map)):
        for y in range(0, len(map)):
            if map[x][y]!='.' :
                tab.append((x, y))

    return tab


# chip_select is INITIALIZED or AVAILABLE
def rooms_type(chip_select, map, xRoom, yRoom):
    tab = []  # list of the rooms availables

    # right
    if 0 <= xRoom+1 < len(map):
        right = (xRoom+1, yRoom)
        if map[right[0]][right[1]] in chip_select:
            tab.append(right)

    # left
    if 0 <= xRoom-1 < len(map):
        left = (xRoom-1, yRoom)
        if map[left[0]][left[1]] in chip_select:
            tab.append(left)

    # top
    if 0 <= yRoom+1 < len(map):
        top = (xRoom, yRoom+1)
        if map[top[0]][top[1]] in chip_select:
            tab.append(top)

    # bottom
    if 0 <= yRoom-1 < len(map):
        bottom = (xRoom, yRoom-1)
        if map[bottom[0]][bottom[1]] in chip_select:
            tab.append(bottom)

    return tab


def pick_a_room(map, choose):
    filled = rooms_type(INITIALIZED, map, choose[0], choose[1])
    empty = rooms_type(AVAILABLE, map, choose[0], choose[1])
    tab = []  # slot with the different weighting
    tab.append(empty) # add the rooms which exists one the right/left/top/bottom
    coef = 50 # weighting

    for i in range(len(empty)):
        for y in range(len(filled)):
            if abs(empty[i][0]-choose[0]) == abs(filled[y][0]-choose[0]):  # find in the x axis
                for _ in range(coef):
                    tab.append(empty[i])

            if abs(empty[i][1]-choose[1]) == abs(filled[y][1]-choose[1]):  # find in the y axis
                for _ in range(coef):
                    tab.append(empty[i])

    choosen = random.choice(tab[0])

    return choosen


file_room = open("room_generator.txt", "w")
file_map = open("map_generator.txt", "w")
map_size = 7
nb_room = 10
# initialize the alphabet for INITIALIZED
alphabet = []
for x in range(ord('a'),ord('z')+1):
     alphabet.append(chr(x))
INITIALIZED = alphabet
# initialize the dot for AVAILABLE
dot_tab =[]
dot_tab.append('.')
AVAILABLE = dot_tab

# initialize with '.'
map = numpy.zeros((map_size, map_size),dtype=str)
for x in range(0,map_size) :
    for y in range(0,map_size) :
        map[x][y] = '.'

# initialize the start in the center of the map
start_x = len(map)//2
start_y = len(map)//2
map[start_x][start_y] = 'a'  # start = 2 or 'a'                                                  /!\
nb_room -= 1

def room_letter(count) :
    # print count
    return chr(ord('a')+count)
count = 1
while nb_room > 0:
    nb_available = 0
    existing_rooms = find_room(map)  # find the rooms which exist
    

    # find rooms available to be initialized
    while nb_available == 0:
        # choose a room
        choose = random.choice(existing_rooms)
        # find the neighbouring rooms not initialized
        availables_rooms = rooms_type(AVAILABLE, map, choose[0], choose[1])
        nb_available = len(availables_rooms)

    # choose a random number of rooms to initialize
    for i in range(random.randrange(nb_available)):
        # choose a room to initialize it
        init = pick_a_room(map, choose)
        map[init[0]][init[1]] = room_letter(count)           # initialize the room                               /!\
        count += 1
        # remove the room from the availables one
        availables_rooms.remove(init)
        nb_room -= 1
        if nb_room <= 0:  # check if we have enought rooms
            break

# file_map.write(str(map))  # write the matrix in the file
print(map)
# print(str(str(map).split('[')))
for a in map:
    if str(a) != '[' or str(a) != ']':
        for b in a:
            file_room.write(str(b))
            # file_room.write(",")
    # file_room.write("-")
    file_room.write("\n")


file_map.close()
