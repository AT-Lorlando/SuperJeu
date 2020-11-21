from types import CoroutineType
import numpy as np
import mapgenerator as mapgen
import random 
# from map_generator import * 
# map_generator as mapgen

def load_map(map) :
    with open('map_generator.txt') as f: 
        for row in f:
            abc=[]
            for x in row :
                abc.append(x)
            map.append(abc)
    return map
   

def find_room(map, letter):
    for x in range(0, len(map)):
        for y in range(0, len(map)):
            if map[x][y] == letter :
                return (x,y)

def nb_rooms(map) :
    count = 0
    for x in range(0, len(map)):
        for y in range(0, len(map)):
            if map[x][y] != '.' :
                count +=1
    return count

# file_room = open("room_generator.txt", "w")
map=[]
map=load_map(map)
room_to_init = 'a' # begin the init with the start
# ROOM_SIZE = 7

alphabet = [] # declare an alphabet
for x in range(ord('a'),ord('z')+1):
     alphabet.append(chr(x))

for i in range(0,nb_rooms(map)) :
    HEIGHT_ROOM = random.choice(range(7,12))
    WIDTH_ROOM = random.choice(range(7,12))
    room=[]
    coo_room = find_room(map, room_to_init) # find the rooms to init with the letter given -> give the coordonate in the map
    # init the room with zeros
    for x in range(0,HEIGHT_ROOM):
        col =[]
        for y in range(0,WIDTH_ROOM):
            col.append(0)
        room.append(col)

    # put 1 on the borders's slots and '.' in the other slots
    for x in range(0, HEIGHT_ROOM):
        for y in range(0, WIDTH_ROOM):
            if len(mapgen.rooms_type([0,1,'.','D'],room,x,y,False,HEIGHT_ROOM,WIDTH_ROOM)) == 4 :
                room[x][y] = '.' 
            else:
                room[x][y]= 1
    #find the doors
    need_doors=mapgen.rooms_type(alphabet,map,coo_room[0],coo_room[1],True,HEIGHT_ROOM,WIDTH_ROOM)
    print(need_doors)
    for direction in need_doors :
        if direction == 'r' :
            room[HEIGHT_ROOM//2][WIDTH_ROOM-1] = 'D'
        if direction == 'l' :
            room[HEIGHT_ROOM//2][0] = 'D'
        if direction == 't' :
            room[0][WIDTH_ROOM//2] = 'D'
        if direction == 'b' :
            room[HEIGHT_ROOM-1][WIDTH_ROOM//2] = 'D'

    with open("room_"+room_to_init+".txt", "w") as f :
        mapgen.write_map(room,f)

    room_to_init=chr(ord(room_to_init)+1)
    
    


# print("\n\nEND")
# print(room)

    