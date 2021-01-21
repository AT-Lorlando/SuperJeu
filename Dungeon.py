import random
import numpy as np
from numpy.lib.function_base import diff
import pandas as pd
from math import floor, ceil
from settings import *

import csv

ROOM_SIZE = 50
SPACE_BETWEEN_END = floor(0.10 * ROOM_SIZE)
global_header = 11000    

def random_lenght(Room_size):
    return random.randint(floor(0.35 * Room_size), ceil(0.75*Room_size))

def get_header():
    global global_header
    global_header += 1000
    if global_header > 99000:
        global_header = 11000
    return global_header

class Instance:
    def __init__(self, name):
        self.name = name
        self.data = []
        self.data = np.full( (70, 80), FLOOR_ID)
        self.door_type = 1

    def open(self, filename):
        file = open(f'{filename}', "rt")
        tab = []
        tile = 0
        k = 0
        for i,line in enumerate(file):
            for j,c in enumerate(line):
                if(c != ';' and c != '\n'):
                    tab.append(int(c))
                # elif(j//2 >= 80):
                #     break
                else:
                    for index, y in enumerate(tab):
                        tile += y*pow(10,len(tab)-index-1)
                    self.data[i, k] = tile
                    # if(tile != 1):
                    #     print('add', tile, i, j//2, k)
                    tile = 0
                    tab = []
                    k +=1
            k = 0
            
    def save(self):
        file = open(f'Instance_{self.name}.txt', "w")
        for line in self.data:
            file.write(str(line).replace('[', '').replace('\n', '').replace(']','\n').replace('  ', ' ').replace('  ', ' ').replace(' ', ','))

class Tile:
    def __init__(self, ID):
        self.ID = ID
        self.header = get_header()
        self.x = 0
        self.y = 0
        self.X = 0
        self.Y = 0

    def make_size(self, Room_size):
        self.Width = random_lenght(Room_size)
        self.Height = random_lenght(Room_size)
        self.data = np.full( (self.Height, self.Width), self.header + FLOOR_ID)
        self.data[:,0] = np.full_like(1, self.header + WALL_ID)
        self.data[:,-1] = np.full_like(1, self.header + WALL_ID)
        self.data[0] = np.full_like(1, self.header + WALL_ID)
        self.data[-1] = np.full_like(1, self.header + WALL_ID)

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.X = x + self.Width - 1
        self.Y = y + self.Height - 1

class Corridor:
    def __init__(self, ID, x, y, side, l):
        self.ID = ID
        self.header = get_header()
        self.x = x
        self.y = y
        self.side = side
        self.lenght = l

class Room:
    def __init__(self, ID, Room_size):
        self.ID = ID
        self.header = get_header()
        self.size = Room_size
        self.data = np.full( (self.size, self.size), VOID_ID)
        self.tile = 0
        self.tile_Xpos = 0
        self.tile_Ypos = 0
        self.pos = 0
        self.corridor_tab = []
        self.connected = False
    
    def connect(self):
        self.connected = True

    def add_corridor(self, side):
        assert(self.tile) #Can't create corridor without tile in the room
        thisCorridorX = 0
        thisCorridorY = 0
        thisCorridorLenght = 0
        if(side == 'LEFT'):
            thisCorridorX = 0
            thisCorridorY = random.randint(self.tile.y+SPACE_BETWEEN_END, self.tile.Y-SPACE_BETWEEN_END)
            thisCorridorLenght = self.tile.x+1
        elif(side == 'RIGHT'):
            thisCorridorX = self.size - 1
            thisCorridorY = random.randint(self.tile.y+SPACE_BETWEEN_END, self.tile.Y-SPACE_BETWEEN_END)
            thisCorridorLenght = self.size-self.tile.X
        elif(side == 'TOP'):
            thisCorridorX = random.randint(self.tile.x+SPACE_BETWEEN_END, self.tile.X-SPACE_BETWEEN_END)
            thisCorridorY = 0
            thisCorridorLenght = self.tile.y+1
        elif(side == 'BOT'):
            thisCorridorX = random.randint(self.tile.x+SPACE_BETWEEN_END, self.tile.X-SPACE_BETWEEN_END)
            thisCorridorY = self.size - 1
            thisCorridorLenght = self.size-self.tile.Y
        self.corridor_tab.append(Corridor( 10*self.ID+len(self.corridor_tab), thisCorridorX, thisCorridorY,side, thisCorridorLenght))

    def add_tile(self, tile):
        tile.make_size(self.size)
        thisX = random.randint(SPACE_BETWEEN_END, self.size-SPACE_BETWEEN_END)
        thisY = random.randint(SPACE_BETWEEN_END, self.size-SPACE_BETWEEN_END)
        while(thisX+tile.Width > self.size-SPACE_BETWEEN_END or 
            thisY+tile.Height > self.size-SPACE_BETWEEN_END or 
            thisX+tile.Width < SPACE_BETWEEN_END or 
            thisY+tile.Height < SPACE_BETWEEN_END):

            thisX = random.randint(SPACE_BETWEEN_END, self.size-SPACE_BETWEEN_END)
            thisY = random.randint(SPACE_BETWEEN_END, self.size-SPACE_BETWEEN_END)
            tile.make_size(self.size)
        self.tile_Xpos = thisX
        self.tile_Ypos = thisY
        for x in range(0,tile.Width):
            for y in range(0,tile.Height):
                X = thisX+x
                Y = thisY+y
                self.data[Y][X]= tile.data[y][x]
        if(1 > 0):
            if(1 > 0):
                tile.set_pos(thisX, thisY)
            else:
                tile.set_pos(thisX, thisY-tile.Height+1) 
        else:
            if(1 > 0):
                tile.set_pos(thisX-tile.Width+1, thisY)
            else:
                tile.set_pos(thisX-tile.Width+1, thisY-tile.Height+1) 
        self.tile = tile

    def add_ID(self, ID):
        assert(self.tile != 0)
        thisX = random.randint(2, self.tile.Width-2)
        thisY = random.randint(2, self.tile.Height-2)
        while(self.data[thisY+self.tile_Ypos][thisX+self.tile_Xpos] != self.tile.header + FLOOR_ID):
            thisX = random.randint(2, self.tile.Width-2)
            thisY = random.randint(2, self.tile.Height-2)
        self.data[thisY+self.tile_Ypos][thisX+self.tile_Xpos] = self.tile.header + ID
        

class Stage:
    def __init__(self, ID, Final_size, Room_size):
        self.ID = ID
        self.factor = Final_size
        self.size = Final_size*ROOM_SIZE-Final_size
        self.room_size = Room_size
        self.data = np.full( (self.size, self.size), VOID_ID)
        self.corridor_tab = []
        self.room_tab = []
        self.door_type = 2

    def add_room(self, room):
        for roomT in self.room_tab:
            assert(roomT.ID != room.ID) # Room already in the final room
        thisX = room.ID%self.factor
        thisY = floor(room.ID/self.factor)
        for x in range(room.size-1):
            for y in range(room.size-1):
                self.data[thisY*(self.room_size-1)+y][thisX*(self.room_size-1)+x] += room.data[y][x]
        if(len(self.room_tab)) == 0:
            room.connect()
        self.room_tab.append(room)
        
        for corridor in room.corridor_tab:
            self.corridor_tab.append(Corridor(corridor.ID, thisX*(self.room_size-1)+corridor.x, thisY*(self.room_size-1)+corridor.y, corridor.side, corridor.lenght))

    def are_connected(self, tile_number):
        count = 0
        for room in self.room_tab:
            if room.connected == True:
                count += 1
        return count >= tile_number

    def write_corridor(self, corridor):
        x = corridor.x
        y = corridor.y
        for i in range(1,corridor.lenght):
            for j in [-1,1]:
                if(corridor.side == 'LEFT'):
                    self.data[y+j][x+i] = corridor.header + WALL_ID
                    self.data[y][x+i] = corridor.header + FLOOR_ID
                elif(corridor.side == 'RIGHT'):
                    self.data[y+j][x-i] = corridor.header + WALL_ID
                    self.data[y][x-i] = corridor.header + FLOOR_ID
                elif(corridor.side == 'TOP'):
                    self.data[y+i][x+j] = corridor.header + WALL_ID
                    self.data[y+i][x] = corridor.header + FLOOR_ID
                elif(corridor.side == 'BOT'):  
                    self.data[y-i][x+j] = corridor.header + WALL_ID
                    self.data[y-i][x] = corridor.header + FLOOR_ID

    def connect_corridor(self, room1, room2):
        #Ordering the rooms to connect
        if(room1.ID >= room2.ID): #Always this order
            return
        ID1 = room1.ID
        ID2 = room2.ID
        #Looking for the direction
        thisX = ID1%self.factor
        thisY = floor(ID1/self.factor)
        firstCorridor = 0
        secondCorridor = 0
        if(ID1 == ID2-1 and floor(ID1/self.factor) == floor(ID2/self.factor)): #Right and on the same row
            #Searching for the corridor
            for cor in room1.corridor_tab:
                if(cor.side == 'RIGHT'):
                    firstCorridor = cor
            for cor in room2.corridor_tab:
                if(cor.side == 'LEFT'):
                    secondCorridor = cor
            assert(firstCorridor != 0 and secondCorridor != 0) #Cannot find the corridor
            #Looking wich corridor is above
            if(firstCorridor.y > secondCorridor.y):
                #From de first corridor y to the second, writing in 
                #ID*(space-1) + interate / (ID+1)*(space-1) + wall & floor
                for y in range(secondCorridor.y-1, firstCorridor.y+2):
                    for x in [-1, 1]:
                        self.data[thisY*(self.room_size-1)+y][(thisX+1)*(self.room_size-1)+x] = firstCorridor.header +WALL_ID
                        self.data[thisY*(self.room_size-1)+y][(thisX+1)*(self.room_size-1)] = firstCorridor.header +FLOOR_ID
                self.data[thisY*(self.room_size-1)+firstCorridor.y+1][(thisX+1)*(self.room_size-1)] = firstCorridor.header +WALL_ID
                self.data[thisY*(self.room_size-1)+secondCorridor.y-1][(thisX+1)*(self.room_size-1)] = firstCorridor.header +WALL_ID
            elif(firstCorridor.y < secondCorridor.y):
                for y in range(firstCorridor.y-1, secondCorridor.y+2):
                    for x in [-1, 1]:
                        self.data[thisY*(self.room_size-1)+y][(thisX+1)*(self.room_size-1)+x] = firstCorridor.header +WALL_ID
                        self.data[thisY*(self.room_size-1)+y][(thisX+1)*(self.room_size-1)] = firstCorridor.header +FLOOR_ID
                self.data[thisY*(self.room_size-1)+firstCorridor.y-1][(thisX+1)*(self.room_size-1)] = firstCorridor.header +WALL_ID
                self.data[thisY*(self.room_size-1)+secondCorridor.y+1][(thisX+1)*(self.room_size-1)] = firstCorridor.header +WALL_ID
            elif(firstCorridor.y == secondCorridor.y):
                self.data[thisY*(self.room_size-1)+firstCorridor.y+1][(thisX+1)*(self.room_size-1)] = firstCorridor.header +WALL_ID
                self.data[thisY*(self.room_size-1)+firstCorridor.y][(thisX+1)*(self.room_size-1)] = firstCorridor.header +FLOOR_ID
                self.data[thisY*(self.room_size-1)+firstCorridor.y-1][(thisX+1)*(self.room_size-1)] = firstCorridor.header +WALL_ID
            #Picking the corridor in the Final room tab
            for cor in self.corridor_tab:
                if(firstCorridor.ID == cor.ID):
                    firstCorridor = cor
                if(secondCorridor.ID == cor.ID):
                    secondCorridor = cor
            self.write_corridor(firstCorridor)
            self.write_corridor(secondCorridor)
            if(room1.connected or room2.connected):
                room1.connect()
                room2.connect()
        elif(ID1 == ID2-self.factor and ID1%self.factor == ID2%self.factor): #Bot and on the same col
            #Searching for the corridor
            for cor in room1.corridor_tab:
                if(cor.side == 'BOT'):
                    firstCorridor = cor
            for cor in room2.corridor_tab:
                if(cor.side == 'TOP'):
                    secondCorridor = cor
            assert(firstCorridor != 0 and secondCorridor != 0) #Cannot find the corridor
            #Looking wich corridor is aside
            if(firstCorridor.x > secondCorridor.x):
                #From de first corridor y to the second, writing in 
                #ID*(space-1) + interate / (ID+1)*(space-1) + wall & floor
                for x in range(secondCorridor.x-1, firstCorridor.x+2):
                    for y in [-1, 1]:
                        self.data[(thisY+1)*(self.room_size-1)+y][thisX*(self.room_size-1)+x] = firstCorridor.header +WALL_ID
                        self.data[(thisY+1)*(self.room_size-1)][thisX*(self.room_size-1)+x] = firstCorridor.header +FLOOR_ID
                self.data[(thisY+1)*(self.room_size-1)][thisX*(self.room_size-1)+firstCorridor.x+1] = firstCorridor.header +WALL_ID
                self.data[(thisY+1)*(self.room_size-1)][thisX*(self.room_size-1)+secondCorridor.x-1] = firstCorridor.header +WALL_ID
            elif(firstCorridor.x < secondCorridor.x):
                for x in range(firstCorridor.x-1, secondCorridor.x+2):
                    for y in [-1, 1]:
                        self.data[(thisY+1)*(self.room_size-1)+y][thisX*(self.room_size-1)+x] = firstCorridor.header +WALL_ID
                        self.data[(thisY+1)*(self.room_size-1)][thisX*(self.room_size-1)+x] = firstCorridor.header +FLOOR_ID
                self.data[(thisY+1)*(self.room_size-1)][thisX*(self.room_size-1)+firstCorridor.x-1] = firstCorridor.header +WALL_ID
                self.data[(thisY+1)*(self.room_size-1)][thisX*(self.room_size-1)+secondCorridor.x+1] = firstCorridor.header +WALL_ID
            elif(firstCorridor.x == secondCorridor.x):
                self.data[(thisY+1)*(self.room_size-1)][thisX*(self.room_size-1)+firstCorridor.x+1] = firstCorridor.header +WALL_ID
                self.data[(thisY+1)*(self.room_size-1)][thisX*(self.room_size-1)+firstCorridor.x] = firstCorridor.header +FLOOR_ID
                self.data[(thisY+1)*(self.room_size-1)][thisX*(self.room_size-1)+firstCorridor.x-1] = firstCorridor.header +WALL_ID
            #Picking the corridor in the Final room tab
            for cor in self.corridor_tab:
                if(firstCorridor.ID == cor.ID):
                    firstCorridor = cor
                if(secondCorridor.ID == cor.ID):
                    secondCorridor = cor
            self.write_corridor(firstCorridor)
            self.write_corridor(secondCorridor)
            if(room1.connected or room2.connected):
                room1.connect()
                room2.connect()

    def add_type(self, x):
        for i, line in enumerate(self.data):
            for j, tile in enumerate(line):
                if tile%100 == FLOOR_ID or tile%100 == WALL_ID:
                    self.data[i][j] += 100 * x

    def save(self):
        np.savetxt(f"Stage{self.ID}.txt", self.data, fmt="%.5i")


class Dungeon:
    def __init__(self, instance_type, difficulty):
        assert(difficulty > 0, difficulty)
        self.stage_tab = []
        self.type = instance_type
        self.difficulty = difficulty
        self.stage_numbers = random.randint(self.difficulty+2, self.difficulty+3)
        for i in range(1,self.stage_numbers+1):
            if(i>8):
                i = 8
            self.stage_tab.append(New_Stage(i, i, self.type))
        self.stage_tab.append(New_Stage(0, 0, self.type))



def New_Stage(ID, difficulty, dungeon_type):
    stage_size = STAGE_SIZE_TAB[difficulty]
    tile_number = random.randint(difficulty*2,floor(difficulty*2.5))
    if tile_number > stage_size*stage_size:
        tile_number = stage_size*stage_size
        
    chest_weight = [8,6,4,2]
    mob_weight = [5,7,6,3,2,1]

    stage = Stage(ID, stage_size, ROOM_SIZE)
    Room_size = ROOM_SIZE

    if(difficulty):
        while(not stage.are_connected(tile_number)):
            stage = Stage(ID, stage_size, ROOM_SIZE)
            #Chosing tile position:
            Tile_pos_tab = np.sort(random.sample([i for i in range(stage_size*stage_size)], k = tile_number))
            #Chosing stair and spawn position
            special_room = random.sample(sorted(Tile_pos_tab), k = 2 if tile_number > 1 else 1) #Spawn and Stair pos
            for pos in Tile_pos_tab:
                new_room = Room(pos, Room_size)
                new_room.add_tile(Tile(pos))
                #Adding spawn and stairs
                if pos == special_room[0]:
                    new_room.add_ID(SPAWN_ID)
                elif pos == special_room[1]:
                    new_room.add_ID(STAIR_ID)

                #Adding corridor with the position of the tile
                if(pos%stage_size == 0): #RIGHT
                    new_room.add_corridor('RIGHT')
                elif(pos%stage_size == stage_size): #RIGHT
                    new_room.add_corridor('LEFT')
                elif(0<pos%stage_size<stage_size): #MID
                    new_room.add_corridor('RIGHT')
                    new_room.add_corridor('LEFT')
                if(floor(pos/stage_size) == 0): #TOP
                    new_room.add_corridor('BOT')
                elif(floor(pos/stage_size) == stage_size): #BOT
                    new_room.add_corridor('TOP')
                elif(0<floor(pos/stage_size)<stage_size): #MID
                    new_room.add_corridor('TOP')
                    new_room.add_corridor('BOT')
                

                #chest and Mob parts
                for _ in range(random.choices([0,1,2,3], weights=chest_weight, k=1)[0]):
                    new_room.add_ID(CHEST_ID)
                for _ in range(random.choices([0,1,2,3,4,5], weights=mob_weight, k=1)[0]):
                    new_room.add_ID(MOB_ID)  

                stage.add_room(new_room)
            for room1 in stage.room_tab:
                for room2 in stage.room_tab:
                    stage.connect_corridor(room1, room2)
    else:
        stage = Stage(ID, stage_size, ROOM_SIZE)
        new_room = Room(0, Room_size)
        new_room.add_tile(Tile(0))
        new_room.add_ID(SPAWN_ID)
        new_room.add_ID(STAIR_ID)
        new_room.add_ID(CHEST_ID)
        stage.add_room(new_room)

    stage.add_type(dungeon_type)
    stage.save()
    return stage