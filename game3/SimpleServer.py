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
import Player

#import time

def listener(client, address, l_players):
   print("Accepted connection from: ", address)
   with clients_lock:
      l_players.append(Player.Player(user_name=client.recv(1024).decode(), connection_object=client)#Array of clients
   
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

def serve(player_count):   
   l_players = []
   clients_lock = threading.Lock()
   th = []
   
   print("Entering server")

   #assemble the map
   map = Map(player_count)
   
   print("Got the map")

   # create a socket object

   serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

   # get local machine name
   host = socket.gethostname()                           

   port = 9998                                          

   addr = (host, port)

   # bind to the port
   serversocket.bind((host, port))

   # queue up to 5 requests
   serversocket.listen(5)

   while len(l_players) < player_count:
      print("Server is listening for connections...")
      client, address = serversocket.accept()
      packet = pickle.dumps(map)
      client.sendto(packet, addr)
      th.append(Thread(target=listener, args = (client, address, l_players)).start()) #spin another thread for the new client
      
   serversocket.close()