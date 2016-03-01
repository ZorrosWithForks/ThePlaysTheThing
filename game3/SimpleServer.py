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
   
   curr_unit_counts = map.d_continents[defending_country[0]][defending_country[1]].unit_counts # defending countries army
   total_unit_count = curr_unit_counts.infantry + \
                      curr_unit_counts.archers + \
                      curr_unit_counts.cannons + \
                      curr_unit_counts.champions
                      
   curr_unit_counts.infantry -= int(random.randrange(int(defender_damage_sum / 30), int(defender_damage_sum / 20) + 6) * curr_unit_counts.infantry / max(total_unit_count, 1))
   curr_unit_counts.archers -= int(random.randrange(int(defender_damage_sum / 40), int(defender_damage_sum / 20) + 6) * curr_unit_counts.archers / max(total_unit_count, 1))
   curr_unit_counts.cannons -= int(random.randrange(int(defender_damage_sum / 50), int(defender_damage_sum / 30) + 4) * curr_unit_counts.cannons / max(total_unit_count, 1))
   curr_unit_counts.champions -= int(random.randrange(int(defender_damage_sum / 50), int(defender_damage_sum / 40) + 2) * curr_unit_counts.champions / max(total_unit_count, 1))
   
   if curr_unit_counts.infantry < 0:
      curr_unit_counts.infantry = 0
   if curr_unit_counts.archers < 0:
      curr_unit_counts.archers = 0
   if curr_unit_counts.cannons < 0:
      curr_unit_counts.cannons = 0
   if curr_unit_counts.champions < 0:
      curr_unit_counts.champions = 0
   
   for player in l_attacks:
      for attack in player[0]:
         attacking_country = map.ll_map[attack[1]][attack[0]]
         total_unit_count = player[2][attacking_country][1].infantry + \
                      player[2][attacking_country][1].archers + \
                      player[2][attacking_country][1].cannons + \
                      player[2][attacking_country][1].champions
      
         attacker_name = map.d_continents[attacking_country[0]][attacking_country[1]].owner
         player[2][attacking_country][1].infantry -= int(random.randrange(int(d_damage_sum[attacker_name] / 30), int(d_damage_sum[attacker_name] / 20) + 6) * player[2][attacking_country][1].infantry / max(total_unit_count, 1))
         player[2][attacking_country][1].archers -= int(random.randrange(int(d_damage_sum[attacker_name] / 40), int(d_damage_sum[attacker_name] / 20) + 6) * player[2][attacking_country][1].archers / max(total_unit_count, 1))
         player[2][attacking_country][1].cannons -= int(random.randrange(int(d_damage_sum[attacker_name] / 50), int(d_damage_sum[attacker_name] / 30) + 4) * player[2][attacking_country][1].cannons / max(total_unit_count, 1))
         player[2][attacking_country][1].champions -= int(random.randrange(int(d_damage_sum[attacker_name] / 50), int(d_damage_sum[attacker_name] / 40) + 2) * player[2][attacking_country][1].champions / max(total_unit_count, 1))
        
         if player[2][attacking_country][1].infantry < 0:
            player[2][attacking_country][1].infantry = 0
         if player[2][attacking_country][1].archers < 0:
            player[2][attacking_country][1].archers = 0
         if player[2][attacking_country][1].cannons < 0:
            player[2][attacking_country][1].cannons = 0
         if player[2][attacking_country][1].champions < 0:
            player[2][attacking_country][1].champions = 0
            
   l_tempAttacks = l_attacks
   for player in range(len(l_tempAttacks)):
      for attack in range(len(l_tempAttacks[player][0])):
         country = map.ll_map[l_tempAttacks[player][0][attack][1]][l_tempAttacks[player][0][attack][0]]
         units = l_tempAttacks[player][2][country][1]
         if units.infantry == 0 and units.archers == 0 and units.cannons == 0 and units.champions == 0:
            l_attacks[player][0].remove(l_tempAttacks[player][0][attack])
            l_attacks[player][1].remove(l_tempAttacks[player][1][attack])
            l_attacks[player][2][country] = None
            print("Removed an attacker from the list")
   
   numOfAttackers = 0
   attacking_army = None
   attacking_player = None
   for player in l_attacks:
      for defender in range(len(player[1])):
         if player[1][defender] == defender_coords:
            print("got an attacker")
            numOfAttackers += 1
            attacker = map.ll_map[player[0][defender][1]][player[0][defender][0]]
            attacking_player = player[2][attacker][3]
            attacking_army = player[2][attacker][1]

   if curr_unit_counts.infantry == 0 and curr_unit_counts.archers == 0 and curr_unit_counts.cannons == 0 and curr_unit_counts.champions == 0 and numOfAttackers == 1:
      map.d_continents[defending_country[0]][defending_country[1]].owner = attacking_player
      newUnits = attacking_army
      curr_unit_counts.infantry = newUnits.infantry
      curr_unit_counts.archers = newUnits.archers
      curr_unit_counts.cannons = newUnits.cannons
      curr_unit_counts.champions = newUnits.champions
      newUnits.infantry = 0
      newUnits.archers = 0
      newUnits.cannons = 0
      newUnits.champions = 0
         
   l_tempAttacks = l_attacks
   for player in range(len(l_tempAttacks)):
      for attack in range(len(l_tempAttacks[player][0])):
         country = map.ll_map[l_tempAttacks[player][0][attack][1]][l_tempAttacks[player][0][attack][0]]
         units = l_tempAttacks[player][2][country][1]
         if units.infantry == 0 and units.archers == 0 and units.cannons == 0 and units.champions == 0:
            l_attacks[player][0].remove(l_tempAttacks[player][0][attack])
            l_attacks[player][1].remove(l_tempAttacks[player][1][attack])
            l_attacks[player][2][country] = None
            print("Removed an attacker from the list")
         
def receiveAttacks(l_players, serversocket, map, address):
   l_attacks = []   # list of tuples (l_attackers, l_defenders, d_attacks), each belonging to a different player
   l_defenders = [] # list of defender_coords
   
   d_players = {}
   for player in l_players:
      d_players[player.user_name] = player
   
   for player in l_players:
      response = player.connection.recv(8192)
      packet = pickle.loads(response)
      l_attacks.append(packet)
   
   attackCount = 0
   for player in l_attacks:
      for attack in player[0]:
         attackCount += 1
      
   # Take attacking units out of their countries
   for player in l_attacks:
      for attacker in player[0]:
         current_attacker = map.ll_map[attacker[1]][attacker[0]]
         attack_force = map.d_continents[current_attacker[0]][current_attacker[1]].unit_counts
         attack_force.infantry -= player[2][current_attacker][1].infantry
         attack_force.archers -= player[2][current_attacker][1].archers
         attack_force.cannons -= player[2][current_attacker][1].cannons
         attack_force.champions -= player[2][current_attacker][1].champions
      
   while attackCount > 0:
      # Handle retreating armies
      l_tempAttacks = l_attacks
      for player in range(len(l_tempAttacks)):
         for attack in range(len(l_tempAttacks[player][0])):
            current_attacker = map.ll_map[l_tempAttacks[player][0][attack][1]][l_tempAttacks[player][0][attack][0]]
            if l_tempAttacks[player][2][current_attacker][2] == True:
               attack_force = map.d_continents[current_attacker[0]][current_attacker[1]].unit_counts
               attack_force.infantry += l_tempAttacks[player][2][current_attacker][1].infantry
               attack_force.archers += l_tempAttacks[player][2][current_attacker][1].archers
               attack_force.cannons += l_tempAttacks[player][2][current_attacker][1].cannons
               attack_force.champions += l_tempAttacks[player][2][current_attacker][1].champions
               l_attacks[player][0].remove(l_tempAttacks[player][0][attack])
               l_attacks[player][1].remove(l_tempAttacks[player][1][attack])
               l_attacks[player][2][current_attacker] = None
      del l_defenders[:]
      for player in l_attacks:
         for defender in player[1]:
            if defender not in l_defenders:
               l_defenders.append(defender)
               print(defender)
      
      for defender in l_defenders: # defender is a set of coords
         resolveAttacks(defender, l_attacks, map, l_players)
      
      for i in range(len(l_players)):
         curr_connection = l_players[i].connection
         l_players[i].connection = None
         packet = pickle.dumps((Map(map_to_copy=map, copy_player_name=l_players[i].user_name), l_attacks[i], True))
         curr_connection.sendto(packet, address)
         l_players[i].connection = curr_connection
         print("Sent attacks to: " + l_players[i].user_name)
      
      attackCount = 0
      for player in l_attacks:
         for attack in player[0]:
            attackCount += 1
            
      del l_attacks[:]
      for player in l_players:
         response = player.connection.recv(8192)
         packet = pickle.loads(response)
         l_attacks.append(packet)
            
   for i in range(len(l_players)):
      curr_connection = l_players[i].connection
      l_players[i].connection = None
      packet = pickle.dumps((Map(map_to_copy=map, copy_player_name=l_players[i].user_name), l_attacks[i], False))
      curr_connection.sendto(packet, address)
      l_players[i].connection = curr_connection
      print("Sent final map to: " + l_players[i].user_name)
      
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
      print("Server: exited receiveAttacks")
      #temp = input("pausing the server")
   
   serversocket.close()