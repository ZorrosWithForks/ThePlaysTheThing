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
MAPWIDTH  = 10
MAPHEIGHT = 7
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