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
         None
         #data = client.recv(1024).decode() #block waiting for data from a client
         #if not data:
            #break
         #else:
            #print(repr(data))
            #with clients_lock:
               #for c in clients:
						#do something for every client
                      #c.sendall(data.encode('ascii'))
   finally:
      with clients_lock:
         #l_players.remove(client)
         client.close()
         
def receivePlacements(l_players, serversocket, map, address):
   l_placements = []
   
   d_players = {}
   for player in l_players:
      d_players[player.user_name] = player
   
   for player in l_players:
      response = player.connection.recv(8192)
      placement = pickle.loads(response)
      l_placements.append(placement)
   
   #print("I got it! Yay!")

   
   for placement in l_placements:
      grand_total = 0
      for continent in map.l_continent_names:
         for country_i in range(len(map.d_continents[continent])):
            if placement[0].d_continents[continent][country_i].unit_counts != None and placement[0].d_continents[continent][country_i].owner == placement[1].user_name:
               grand_total += (placement[0].d_continents[continent][country_i].unit_counts.infantry - map.d_continents[continent][country_i].unit_counts.infantry)
               grand_total += (placement[0].d_continents[continent][country_i].unit_counts.archers - map.d_continents[continent][country_i].unit_counts.archers) * 2
               grand_total += (placement[0].d_continents[continent][country_i].unit_counts.cannons - map.d_continents[continent][country_i].unit_counts.cannons) * 2
               grand_total += (placement[0].d_continents[continent][country_i].unit_counts.champions - map.d_continents[continent][country_i].unit_counts.champions) * 5
               
      if grand_total <= d_players[placement[1].user_name].unit_counts:
         for continent in map.l_continent_names:
            for country_i in range(len(map.d_continents[continent])):
               if placement[0].d_continents[continent][country_i].unit_counts != None and placement[0].d_continents[continent][country_i].owner == placement[1].user_name:
                  map.d_continents[continent][country_i].unit_counts = placement[0].d_continents[continent][country_i].unit_counts
      else: print("Cheaters never prosper!")

   for player in l_players:
      curr_connection = player.connection
      player.connection = None
      packet = pickle.dumps(Map(map_to_copy=map, copy_player_name=player.user_name))
      curr_connection.sendto(packet, address)
      player.connection = curr_connection
      print("Sent to: " + player.user_name)
               
def serve(player_count):   
   l_players = []
   
   print("Entering server")

   # create a socket object

   serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

   # get local machine name
   temp = socket.gethostbyname_ex(socket.gethostname())[-1]
   host = temp[-1]                           

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
      #th.append(Thread(target=listener, args = (client, address, l_players)).start()) #spin another thread for the new client
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
      player.connection = curr_connection
      print("Sent to: " + player.user_name)
   
   while True:
      receivePlacements(l_players, serversocket, map, addr)
   
   serversocket.close()