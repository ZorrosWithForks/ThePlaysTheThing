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
      print("Sent placements to: " + player.user_name)

      
def resolveAttacks(defender_coords, l_attacks, map, l_players):
   defending_country = map.ll_map[defender_coords[1]][defender_coords[0]]
   defense_force = map.d_continents[defending_country[0]][defending_country[1]].unit_counts
   for player in l_attacks:
      for attack in player[0]:
         if defender_coords == attack:
            attacking_country = map.ll_map[attack[1]][attack[0]]
            attack_force = map.d_continents[attack[0]][attack[1]].unit_counts
            defense_force.infantry -= attack_force.infantry
            defense_force.archers -= attack_force.archers
            defense_force.cannons -= attack_force.cannons
            defense_force.champions -= attack_force.champions
            
   d_attackers = {}
   d_attacker_counts = {}
   for player in l_players:
      d_attackers[player.user_name] = [UnitCounts(0,0,0,0), 0] #UnitCounts, country attack bonus
      d_attacker_counts[player.user_name] = 0
      for attacker in l_attacks:
         for attack in attacker[0]:
            if attacker[2][map.ll_map[attack[1]][attack[0]]][0] == defending_country:
               d_attackers[player.user_name][0].infantry += attacker[2][map.ll_map[attack[1]][attack[0]]][1].infantry
               d_attackers[player.user_name][0].archers += attacker[2][map.ll_map[attack[1]][attack[0]]][1].archers
               d_attackers[player.user_name][0].cannons += attacker[2][map.ll_map[attack[1]][attack[0]]][1].cannons
               d_attackers[player.user_name][0].champions += attacker[2][map.ll_map[attack[1]][attack[0]]][1].champions
               
               attacking_country = map.ll_map[attack[1]][attack[0]]
               d_attackers[player.user_name][1] += map.d_continents[attacking_country[0]][attacking_country[1]].attack_bonus
               d_attacker_counts[player.user_name] += 1 # Number of countries to divide losses into
   
   d_damage_sum = {}
   for player in l_players:
      d_damage_sum[player.user_name] = 0
      for attacker in l_players:
         if attacker.user_name != player.user_name:
            d_damage_sum[player.user_name] += int((d_attackers[attacker.user_name][0].infantry + \
                                              d_attackers[attacker.user_name][0].archers * 2 + \
                                              d_attackers[attacker.user_name][0].cannons + \
                                              d_attackers[attacker.user_name][0].champions * 3) \
                                              * (d_attackers[attacker.user_name][1] / 100 + 1))
      
      defending_country_data = map.d_continents[defending_country[0]][defending_country[1]]
      d_damage_sum[player.user_name] += int((defending_country_data.unit_counts.infantry + \
                                        defending_country_data.unit_counts.archers * 2 + \
                                        defending_country_data.unit_counts.cannons + \
                                        defending_country_data.unit_counts.champions * 3) \
                                        * (defending_country_data.defense_bonus / 100 + 1))

   defender_damage_sum = 0
   for attacker in l_players:
      defender_damage_sum += int((d_attackers[attacker.user_name][0].infantry + \
                               d_attackers[attacker.user_name][0].archers * 2 + \
                               d_attackers[attacker.user_name][0].cannons + \
                               d_attackers[attacker.user_name][0].champions * 3) \
                               * (d_attackers[attacker.user_name][1] / 100 + 1))
   
   curr_unit_counts = map.d_continents[defending_country[0]][defending_country[1]].unit_counts
   total_unit_count = curr_unit_counts.infantry + \
                      curr_unit_counts.archers + \
                      curr_unit_counts.cannons + \
                      curr_unit_counts.champions
   curr_unit_counts.infantry -= int(random.randrange(int(defender_damage_sum / 30), int(defender_damage_sum / 20) + 6) * curr_unit_counts.infantry / total_unit_count)
   curr_unit_counts.archers -= int(random.randrange(int(defender_damage_sum / 40), int(defender_damage_sum / 20) + 6) * curr_unit_counts.archers / total_unit_count)
   curr_unit_counts.cannons -= int(random.randrange(int(defender_damage_sum / 50), int(defender_damage_sum / 30) + 4) * curr_unit_counts.cannons / total_unit_count)
   curr_unit_counts.champions -= int(random.randrange(int(defender_damage_sum / 50), int(defender_damage_sum / 40) + 2) * curr_unit_counts.champions / total_unit_count)
   
   for player in l_attacks:
      for attack in player[0]:
         attacking_country = map.ll_map[attack[1]][attack[0]]
         attacker_name = map.d_continents[attacking_country[0]][attacking_country[1]].owner
         player[2][attacking_country][1].infantry -= int(random.randrange(int(d_damage_sum[attacker_name] / 30), int(d_damage_sum[attacker_name] / 20) + 6) / d_attacker_counts[attacker_name])
         player[2][attacking_country][1].archers -= int(random.randrange(int(d_damage_sum[attacker_name] / 40), int(d_damage_sum[attacker_name] / 20) + 6) / d_attacker_counts[attacker_name])
         player[2][attacking_country][1].cannons -= int(random.randrange(int(d_damage_sum[attacker_name] / 50), int(d_damage_sum[attacker_name] / 30) + 4) / d_attacker_counts[attacker_name])
         player[2][attacking_country][1].champions -= int(random.randrange(int(d_damage_sum[attacker_name] / 50), int(d_damage_sum[attacker_name] / 40) + 2) / d_attacker_counts[attacker_name])
   
def receiveAttacks(l_players, serversocket, map, address):
   l_attacks = []
   l_defenders = []
   
   d_players = {}
   for player in l_players:
      d_players[player.user_name] = player
   
   for player in l_players:
      response = player.connection.recv(8192)
      packet = pickle.loads(response)
      l_attacks.append(packet)
      
   # Take attacking units out of their countries
   for player in l_attacks:
      for attacker in player[0]:
         current_attacker = map.ll_map[attacker[1]][attacker[0]]
         attack_force = map.d_continents[current_attacker[0]][current_attacker[1]].unit_counts
         attack_force.infantry -= player[2][current_attacker][1].infantry
         attack_force.archers -= player[2][current_attacker][1].archers
         attack_force.cannons -= player[2][current_attacker][1].cannons
         attack_force.champions -= player[2][current_attacker][1].champions
      
   while True:
      for player in l_attacks:
         for attacker in player[0]:
            current_attacker = map.ll_map[attacker[1]][attacker[0]]
            if player[2][current_attacker][2] == True:
               attack_force = map.d_continents[current_attacker[0]][current_attacker[1]].unit_counts
               attack_force.infantry += player[2][current_attacker][1].infantry
               attack_force.archers += player[2][current_attacker][1].archers
               attack_force.cannons += player[2][current_attacker][1].cannons
               attack_force.champions += player[2][current_attacker][1].champions
      
      for player in l_attacks:
         for defender in player[1]:
            if defender not in l_defenders:
               l_defenders.append(defender)
      
      for defender in l_defenders: # defender is a set of coords
         resolveAttacks(defender, l_attacks, map, l_players)
      
      for i in range(len(l_players)):
         curr_connection = l_players[i].connection
         l_players[i].connection = None
         packet = pickle.dumps((Map(map_to_copy=map, copy_player_name=l_players[i].user_name), l_attacks[i]))
         curr_connection.sendto(packet, address)
         l_players[i].connection = curr_connection
         print("Sent attacks to: " + l_players[i].user_name)
         
      for player in l_players:
         response = player.connection.recv(8192)
         packet = pickle.loads(response)
         l_attacks.append(packet)
      
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
      receiveAttacks(l_players, serversocket, map, addr)
   
   serversocket.close()