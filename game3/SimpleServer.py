# server.py 
import socket
import os
import threading
from threading import Thread
import _thread
import pygame, sys, random
from pygame.locals import *
import pickle
from Maps import *


#import time

clients = set()
clients_lock = threading.Lock()
th = []

#useful game dimensions
TILESIZE  = 20
MAPWIDTH  = 11
MAPHEIGHT = 8
BOTTOM_HALF_START = 15

#constants representing colours
BLACK = (0,   0,   0  )
BROWN = (153, 76,  0  )
GREEN = (0,   255, 0  )
BLUE  = (0,   0,   255)
WHITE = (255, 255, 255)

#constants representing the different resources
DIRT  = 0
GRASS = 1
WATER = 2
COAL  = 3
DIAMOND = 4
LAVA = 5
SKY = 6
CLOUD = 7
PLANE = 8
WOOD = 9
LEAVES = 10

#add a font for our inventory
SEED_SPACE_ROW = MAPHEIGHT - 13
SEED_SPACE_COL = MAPWIDTH - 8
TOP_HALF = MAPHEIGHT - 5

#a list of resources
resources = [DIRT,GRASS,WATER,COAL,DIAMOND,LAVA]
#use list comprehension to create our tilemap
tilemap = [ [DIRT for w in range(MAPWIDTH)] for h in range(MAPHEIGHT) ]

def listener(client, address):
   print("Accepted connection from: ", address)
   with clients_lock:
      clients.add(client)#Array of clients
   try:
      while True:
         data = client.recv(1024).decode() #block waiting for data from a client
         if not data:
            break
         else:
            print(repr(data))
            #with clients_lock:
               #for c in clients:
						#do something for every client
                        #c.sendall(data.encode('ascii'))
   finally:
      with clients_lock:
         clients.remove(client)
         client.close()
'''
#fill all with water
for row in range (MAPHEIGHT):
   for col in range (MAPWIDTH):
      tilemap[row][col] = WATER
     
for row2 in range (2, 5):
   for col2 in range (2, 5):
      if random.randint(0,1) == True:
         tilemap[row2][col2] = GRASS

tilemap[SEED_SPACE_ROW][SEED_SPACE_COL] = GRASS

#LEFT OF TILE
if tilemap[SEED_SPACE_ROW][SEED_SPACE_COL-1] == WATER:
   if random.randint(0,1) > 0:
      tilemap[SEED_SPACE_ROW][SEED_SPACE_COL-1] = LEAVES
       
#ABOVE TILE
if tilemap[SEED_SPACE_ROW-1][SEED_SPACE_COL] == WATER:
   if random.randint(0,3) > 0:
      tilemap[SEED_SPACE_ROW-1][SEED_SPACE_COL] = LAVA
       
#TOP LEFT OF TILE
if tilemap[SEED_SPACE_ROW-1][SEED_SPACE_COL-1] == WATER:
   if random.randint(0,2) > 0:
      tilemap[SEED_SPACE_ROW-1][SEED_SPACE_COL-1] = COAL
       
#RIGHT OF TILE
if tilemap[SEED_SPACE_ROW][SEED_SPACE_COL+1] == WATER:
   if random.randint(0,4) > 0:
      tilemap[SEED_SPACE_ROW][SEED_SPACE_COL+1] = DIRT
       
#BELOW TILE
if tilemap[SEED_SPACE_ROW+1][SEED_SPACE_COL] == WATER:
   if random.randint(0,5) > 0:
      tilemap[SEED_SPACE_ROW+1][SEED_SPACE_COL] = DIAMOND
       
#BOTTOM RIGHT OF TILE
if tilemap[SEED_SPACE_ROW+1][SEED_SPACE_COL+1] == WATER:
   if random.randint(0,7) > 0:
      tilemap[SEED_SPACE_ROW+1][SEED_SPACE_COL+1] = WOOD
'''
#assemble the map
player_count = int(input("Just for sake of argument, enter the number of players: "))
map = Map(player_count)

# create a socket object

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

port = 9999                                           

addr = (host, port)

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

while True:
   print("Server is listening for connections...")
   client, address = serversocket.accept()
   packet = pickle.dumps(map)
   client.sendto(packet, addr)
   th.append(Thread(target=listener, args = (client,address)).start()) #spin another thread for the new client
   
serversocket.close()