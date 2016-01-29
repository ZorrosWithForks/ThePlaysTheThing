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

clients_lock = threading.Lock()
th = []

def listener(client, address, l_players):
   print("Accepted connection from: ", address)
   with clients_lock:      
      print("Added player")
    
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
         #l_players.remove(client)
         client.close()
         
def serve(player_count):   
   l_players = []
   
   print("Entering server")

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
   i = 0
   while i < player_count:
      print("Server is listening for connections...")
      client, address = serversocket.accept()
      th.append(Thread(target=listener, args = (client, address, l_players)).start()) #spin another thread for the new client
      l_players.append(Player.Player(user_name=client.recv(1024).decode()))#Array of clients
      l_players[i].connection = client
      i += 1
      
   #assemble the map
   print("got map")
   print("# of players: " + str(len(l_players)))
   map = Map(l_players)
   for player in l_players:
      curr_connection = player.connection
      player.connection = None
      packet = pickle.dumps((Map(map_to_copy=map, copy_player_name=player.user_name), player))
      curr_connection.sendto(packet, addr)
      print("Sent to: " + player.user_name)
   
   serversocket.close()