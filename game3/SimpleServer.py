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
import copy

clients_lock = threading.Lock()
th = []
l_playerNames = []
d_playerCountries = {}

def receivePlacements(l_players, l_dead_players, serversocket, map, address):
   l_placements = []
   
   d_players = {}
   for player in l_players:
      d_players[player.user_name] = player
   
   tempPlayers = copy.copy(l_players)
   for player in tempPlayers:
      try:
         response = player.connection.recv(16384)
         placement = pickle.loads(response)
         l_placements.append(placement)
      except:
         l_players.remove(player)
         l_playerNames.remove(player.user_name)
         d_playerCountries[player.user_name] = 0
         for continent in map.l_continent_names:
            for country in range(len(map.d_continents[continent])):
               if map.d_continents[continent][country].owner == player.user_name:
                  map.d_continents[continent][country].owner = "Unoccupied"
   
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
      
   tempPlayers = copy.copy(l_players)
   sortPlayers(map.l_player_names, d_playerCountries)
   for player in tempPlayers:
      curr_connection = player.connection
      player.connection = None
      packet = pickle.dumps((Map(map_to_copy=map, copy_player_name=player.user_name), l_playerNames, d_playerCountries))
      try:
         curr_connection.sendto(packet, address)
      except:
         l_players.remove(player)
         sortPlayers(map.l_player_names, d_playerCountries)
         l_playerNames.remove(player.user_name)
         d_playerCountries[player.user_name] = 0
         for continent in map.l_continent_names:
            for country in range(len(map.d_continents[continent])):
               if map.d_continents[continent][country].owner == player.user_name:
                  map.d_continents[continent][country].owner = "Unoccupied"
      player.connection = curr_connection
      print("Sent placements to: " + player.user_name)
      
   tempPlayers = copy.copy(l_dead_players)
   
   for i in range(len(tempPlayers)):
      curr_connection = l_dead_players[i].connection
      l_dead_players[i].connection = None
      packet = pickle.dumps((map, l_playerNames, d_playerCountries))
      try:
         curr_connection.sendto(packet, address)
         l_dead_players[i].connection = curr_connection
         print("Sent placements to spectator: " + l_dead_players[i].user_name)
      except:
         l_dead_players.remove(l_dead_players[i])
      
def resolveAttacks(defender_coords, l_attacks, map, l_players, d_attackResults):
   numOfAttackers = 2
   while numOfAttackers > 0:
      print("Number of attackers: " + str(numOfAttackers))
      defending_country = map.ll_map[defender_coords[1]][defender_coords[0]]
      d_attackers = {}
      d_attacker_counts = {}
      
      for player in l_players:
         d_attackers[player.user_name] = [UnitCounts(0,0,0,0), 0] #UnitCounts, country attack bonus
         d_attacker_counts[player.user_name] = 0
         for attacker in l_attacks:
            for attack in attacker[0]:
               attacking_country = map.ll_map[attack[1]][attack[0]]
               if attacker[2][attacking_country] != None:
                  attacking_user = attacker[2][attacking_country][3]
                  if attacker[2][attacking_country][0] == defending_country and attacking_user == player.user_name:
                     #print("Player " + attacking_user + " is attacking " + str(map.d_continents[defending_country[0]][defending_country[1]]))
                     d_attackers[player.user_name][0].infantry += attacker[2][map.ll_map[attack[1]][attack[0]]][1].infantry
                     d_attackers[player.user_name][0].archers += attacker[2][map.ll_map[attack[1]][attack[0]]][1].archers
                     d_attackers[player.user_name][0].cannons += attacker[2][map.ll_map[attack[1]][attack[0]]][1].cannons
                     d_attackers[player.user_name][0].champions += attacker[2][map.ll_map[attack[1]][attack[0]]][1].champions
                     
                     d_attackers[player.user_name][1] += map.d_continents[attacking_country[0]][attacking_country[1]].attack_bonus
                     d_attacker_counts[player.user_name] += 1 # Number of countries to divide losses into
      
      d_damage_sum = {}
      for player in l_players:
         d_damage_sum[player.user_name] = 0
         #print("damage sum for " + player.user_name + ": " + str(d_damage_sum[player.user_name]))
         for attacker in l_players:
            if attacker.user_name != player.user_name:
               d_damage_sum[player.user_name] += int((d_attackers[attacker.user_name][0].infantry + \
                                                 d_attackers[attacker.user_name][0].archers * 2 + \
                                                 d_attackers[attacker.user_name][0].cannons + \
                                                 d_attackers[attacker.user_name][0].champions * 3) \
                                                 * (d_attackers[attacker.user_name][1] / 100 + 1))
               #print("damage sum for " + player.user_name + ": " + str(d_damage_sum[player.user_name]))
         defending_country_data = map.d_continents[defending_country[0]][defending_country[1]]
         d_damage_sum[player.user_name] += int((defending_country_data.unit_counts.infantry + \
                                           defending_country_data.unit_counts.archers * 2 + \
                                           defending_country_data.unit_counts.cannons + \
                                           defending_country_data.unit_counts.champions * 3) \
                                           * (defending_country_data.defense_bonus / 100 + 1))
         print("damage sum for " + player.user_name + ": " + str(d_damage_sum[player.user_name]))
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
                         
      curr_unit_counts.infantry -= int(random.randrange(int(defender_damage_sum  * .5), int(defender_damage_sum) + 1) * curr_unit_counts.infantry / max(total_unit_count, 1))
      curr_unit_counts.archers -= int(random.randrange(int(defender_damage_sum   * .4), int(defender_damage_sum) + 1) * curr_unit_counts.archers / max(total_unit_count, 1))
      curr_unit_counts.cannons -= int(random.randrange(int(defender_damage_sum   * .2), int(defender_damage_sum  * .4) + 1) * curr_unit_counts.cannons / max(total_unit_count, 1))
      curr_unit_counts.champions -= int(random.randrange(int(defender_damage_sum * .2), int(defender_damage_sum  * .35) + 1) * curr_unit_counts.champions / max(total_unit_count, 1))
      
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
            if player[2][attacking_country][0] == defending_country:
               total_unit_count = (player[2][attacking_country][1].infantry + \
                            player[2][attacking_country][1].archers + \
                            player[2][attacking_country][1].cannons + \
                            player[2][attacking_country][1].champions)
               
               attacker_name = player[2][attacking_country][3]
               print("Troops were murdered: " + str(player[2][attacking_country][3]))
               print("total_unit_count: " + str(total_unit_count))
               print("d_damage_sum: " + str(d_damage_sum[attacker_name]))
               player[2][attacking_country][1].infantry -= int(random.randrange(int(d_damage_sum[attacker_name]  * .5), int(d_damage_sum[attacker_name]) + 1) * player[2][attacking_country][1].infantry / max(total_unit_count, 1) / max(d_attacker_counts[player[2][attacking_country][3]], 1))
               player[2][attacking_country][1].archers -= int(random.randrange(int(d_damage_sum[attacker_name]   * .4), int(d_damage_sum[attacker_name]) + 1) * player[2][attacking_country][1].archers / max(total_unit_count, 1) / max(d_attacker_counts[player[2][attacking_country][3]], 1))
               player[2][attacking_country][1].cannons -= int(random.randrange(int(d_damage_sum[attacker_name]   * .2), int(d_damage_sum[attacker_name] * .35) + 2) * player[2][attacking_country][1].cannons / max(total_unit_count, 1) / max(d_attacker_counts[player[2][attacking_country][3]], 1))
               player[2][attacking_country][1].champions -= int(random.randrange(int(d_damage_sum[attacker_name] * .2), int(d_damage_sum[attacker_name] * .35) + 1) * player[2][attacking_country][1].champions / max(total_unit_count, 1) / max(d_attacker_counts[player[2][attacking_country][3]], 1))
               
              
               if player[2][attacking_country][1].infantry < 0:
                  player[2][attacking_country][1].infantry = 0
               if player[2][attacking_country][1].archers < 0:
                  player[2][attacking_country][1].archers = 0
               if player[2][attacking_country][1].cannons < 0:
                  player[2][attacking_country][1].cannons = 0
               if player[2][attacking_country][1].champions < 0:
                  player[2][attacking_country][1].champions = 0
               
      l_tempAttacks = copy.deepcopy(l_attacks)
      for player in range(len(l_tempAttacks)):
         for attack in range(len(l_tempAttacks[player][0])):
            country = map.ll_map[l_tempAttacks[player][0][attack][1]][l_tempAttacks[player][0][attack][0]]
            units = l_tempAttacks[player][2][country][1]
            if units.infantry == 0 and units.archers == 0 and units.cannons == 0 and units.champions == 0:
               if l_attacks[player][2][country][3] != map.d_continents[defending_country[0]][defending_country[1]].owner and \
                  map.d_continents[defending_country[0]][defending_country[1]].name not in d_attackResults[l_attacks[player][2][country][3]][2]:
                  defenderCount = 0
                  for defender in l_attacks[player][1]:
                     if defender == defender_coords:
                        defenderCount += 1
                  print("Defender count: " + str(defenderCount))
                  if defenderCount == 1:
                     d_attackResults[l_attacks[player][2][country][3]][2].append(map.d_continents[defending_country[0]][defending_country[1]].name) 
                     print("added fail to player: " + l_attacks[player][2][country][3])
               l_attacks[player][0].remove(l_tempAttacks[player][0][attack])
               l_attacks[player][1].remove(l_tempAttacks[player][1][attack])
               l_attacks[player][2][country] = None
               print("Removed an attacker from the list")
               
      attacking_player = None
      numOfAttackers = 0
      for player in l_players:
         attacking = False
         for attack_packet in l_attacks:
            d_attacks = attack_packet[2]
            for attacking_country in d_attacks.keys():
               if d_attacks[attacking_country] != None:
                  attacking = attacking or (d_attacks[attacking_country][3] == player.user_name \
                              and d_attacks[attacking_country][0] == defending_country)
                  if d_attacks[attacking_country][0] == defending_country:
                     attacking_player = d_attacks[attacking_country][3]
         if attacking:
            numOfAttackers += 1

      if curr_unit_counts.infantry == 0 \
      and curr_unit_counts.archers == 0 \
      and curr_unit_counts.cannons == 0 \
      and curr_unit_counts.champions == 0 \
      and numOfAttackers == 1:
         d_attackResults[map.d_continents[defending_country[0]][defending_country[1]].owner][1].append(map.d_continents[defending_country[0]][defending_country[1]].name)
         print("Set owner of " + map.d_continents[defending_country[0]][defending_country[1]].name + " to " + attacking_player)
         d_attackResults[attacking_player][0].append(map.d_continents[defending_country[0]][defending_country[1]].name)
         map.d_continents[defending_country[0]][defending_country[1]].owner = attacking_player
         map.d_continents[defending_country[0]][defending_country[1]].unit_production = 1
         for attack_packet in l_attacks:
            d_attacks = attack_packet[2]
            for attacking_country in d_attacks.keys():
               if d_attacks[attacking_country] != None and d_attacks[attacking_country][3] == attacking_player \
               and d_attacks[attacking_country][0] == defending_country:
                  attacking_army = d_attacks[attacking_country][1]
                  curr_unit_counts.infantry += attacking_army.infantry
                  curr_unit_counts.archers += attacking_army.archers
                  curr_unit_counts.cannons += attacking_army.cannons
                  curr_unit_counts.champions += attacking_army.champions
                  attacking_army.infantry = 0
                  attacking_army.archers = 0
                  attacking_army.cannons = 0
                  attacking_army.champions = 0
                  numOfAttackers = 0

      l_tempAttacks = copy.deepcopy(l_attacks)
      for player in range(len(l_tempAttacks)):
         for attack in range(len(l_tempAttacks[player][0])):
            country = map.ll_map[l_tempAttacks[player][0][attack][1]][l_tempAttacks[player][0][attack][0]]
            units = l_tempAttacks[player][2][country][1]
            if units.infantry == 0 and units.archers == 0 and units.cannons == 0 and units.champions == 0:
               l_attacks[player][0].remove(l_tempAttacks[player][0][attack])
               l_attacks[player][1].remove(l_tempAttacks[player][1][attack])
               l_attacks[player][2][country] = None
               print("Removed an attacker from the list")
            
def receiveAttacks(l_players, l_dead_players, serversocket, map, address):
   l_attacks = []   # list of tuples (l_attackers, l_defenders, d_attacks), each belonging to a different player
   l_defenders = [] # list of defender_coords
   d_attackResults = {} # dictionary of the results of the attacks in the form (countries conquered, countries lost, failed attacks)
   
   d_attackResults["Unoccupied"] = [[],[],[]]
   for player in l_players:
      d_attackResults[player.user_name] = [[],[],[]]
   d_players = {}
   for player in l_players:
      d_players[player.user_name] = player
   
   tempPlayers = copy.copy(l_players)
   for player in tempPlayers:
      try:
         response = player.connection.recv(16384)
         packet = pickle.loads(response)
         l_attacks.append(packet)
      except:
         l_playerNames.remove(player.user_name)
         l_players.remove(player)
         d_playerCountries[player.user_name] = 0
         for continent in map.l_continent_names:
            for country in range(len(map.d_continents[continent])):
               if map.d_continents[continent][country].owner == player.user_name:
                  map.d_continents[continent][country].owner = "Unoccupied"
   
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
      
   # Handle retreating armies
   l_tempAttacks = copy.deepcopy(l_attacks)
               
   del l_defenders[:]
   for player in l_attacks:
      for defender in player[1]:
         if defender not in l_defenders:
            l_defenders.append(defender)
            print(defender)
   
   for defender in l_defenders: # defender is a set of coords
      resolveAttacks(defender, l_attacks, map, l_players, d_attackResults)
   
   l_temp_players = []
   for player in l_players:
      d_playerCountries[player.user_name] = 0
      
   d_playerCountries["Unoccupied"] = 0
   
   for name, continent in map.d_continents.items():
      for country in continent:
         d_playerCountries[country.owner] += 1
         
   for player in l_players:
      for name, continent in map.d_continents.items():
         for country in continent:
            if country.owner == player.user_name and player not in l_temp_players:
               l_temp_players.append(player)
               
   for player in l_players:
      if player not in l_temp_players:
         l_dead_players.append(player)
   
   l_players = copy.copy(l_temp_players)
   del l_playerNames[:]
   for player in l_players:
      l_playerNames.append(player.user_name)
	
   sortPlayers(map.l_player_names, d_playerCountries)
   
   tempPlayers = copy.copy(l_players)
   
   for i in range(len(tempPlayers)):
      curr_connection = l_players[i].connection
      l_players[i].connection = None
      playerMap = Map(map_to_copy=map, copy_player_name=l_players[i].user_name)
      packet = pickle.dumps((playerMap, l_playerNames, d_attackResults[l_players[i].user_name], d_playerCountries))
      try:
         curr_connection.sendto(packet, address)
         l_players[i].connection = curr_connection
         print("Sent final map to: " + l_players[i].user_name)
      except:
         d_playerCountries[player.user_name] = 0
         l_playerNames.remove(player.user_name)
         l_players.remove(l_players[i])
         sortPlayers(map.l_player_names, d_playerCountries)
         for continent in map.l_continent_names:
            for country in range(len(map.d_continents[continent])):
               if map.d_continents[continent][country].owner == player.user_name:
                  map.d_continents[continent][country].owner = "Unoccupied"
      
   tempPlayers = copy.copy(l_dead_players)
   
   for i in range(len(tempPlayers)):
      curr_connection = l_dead_players[i].connection
      l_dead_players[i].connection = None
      packet = pickle.dumps((map, l_playerNames, d_playerCountries))
      try:
         curr_connection.sendto(packet, address)
         l_dead_players[i].connection = curr_connection
         print("Sent final map to spectator: " + l_dead_players[i].user_name)
      except:
         l_dead_players.remove(l_dead_players[i])
      
   return l_players
      
def receiveMoves(l_players, l_dead_players, serversocket, map, address):
   l_moves = [] # list of tuples (l_senders, l_receivers, d_moves)
   
   tempPlayers = copy.copy(l_players)
   for player in tempPlayers:
      try:
         response = player.connection.recv(16384)
         packet = pickle.loads(response)
         l_moves.append(packet)
      except:
         d_playerCountries[player.user_name] = 0
         l_playerNames.remove(player.user_name)
         l_players.remove(player)
         for continent in map.l_continent_names:
            for country in range(len(map.d_continents[continent])):
               if map.d_continents[continent][country].owner == player.user_name:
                  map.d_continents[continent][country].owner = "Unoccupied"
      
   for player in l_moves:
      for send in range(len(player[0])):
         sending_country = map.ll_map[player[0][send][1]][player[0][send][0]]
         sending_units = map.d_continents[sending_country[0]][sending_country[1]].unit_counts
         receiving_country = map.ll_map[player[1][send][1]][player[1][send][0]] # Continent and country name (tuple) of the receiving country: courtesy of Caleb
         receiving_units = map.d_continents[receiving_country[0]][receiving_country[1]].unit_counts
         sent_units = player[2][sending_country][1]
         # Take the units sent out of the sending country
         sending_units.infantry -= sent_units.infantry
         sending_units.archers -= sent_units.archers
         sending_units.cannons -= sent_units.cannons
         sending_units.champions -= sent_units.champions
         # Put the units sent into the receiving country
         receiving_units.infantry += sent_units.infantry
         receiving_units.archers += sent_units.archers
         receiving_units.cannons += sent_units.cannons
         receiving_units.champions += sent_units.champions
   
   for player in l_players:
      player.unit_counts = 0
      for continent in map.l_continent_names:
         for country_i in range(len(map.d_continents[continent])):
            if map.d_continents[continent][country_i].owner == player.user_name:
               player.unit_counts += 3
               map.d_continents[continent][country_i].unit_production += 1
               if map.d_continents[continent][country_i].unit_production == 1 and bool(random.getrandbits(1)): #50-50 chance boolean coin toss
                  map.d_continents[continent][country_i].unit_counts.infantry += 1
                  map.d_continents[continent][country_i].unit_production = 0
               elif map.d_continents[continent][country_i].unit_production == 2 and bool(random.getrandbits(1)):
                  if bool(random.getrandbits(1)):
                     map.d_continents[continent][country_i].unit_counts.archers += 1
                  else:
                     map.d_continents[continent][country_i].unit_counts.cannons += 1
                  map.d_continents[continent][country_i].unit_production = 0
               elif map.d_continents[continent][country_i].unit_production == 5:
                  map.d_continents[continent][country_i].unit_counts.champions += 1
                  map.d_continents[continent][country_i].unit_production = 0
               else:
                  map.d_continents[continent][country_i].unit_production += 1
   
   
   applyContinentBonuses(l_players, map)
   sortPlayers(map.l_player_names, d_playerCountries)
   tempPlayers = copy.copy(l_players)
   for player in tempPlayers:
      curr_connection = player.connection
      player.connection = None
      packet = pickle.dumps((Map(map_to_copy=map, copy_player_name=player.user_name), player, l_playerNames, d_playerCountries))
      try:
         curr_connection.sendto(packet, address)
         player.connection = curr_connection
         print("Sent moves to: " + player.user_name)
      except:
         l_players.remove(player)
         sortPlayers(map.l_player_names, d_playerCountries)
         l_playerNames.remove(player.user_name)
         for continent in map.l_continent_names:
            for country in range(len(map.d_continents[continent])):
               if map.d_continents[continent][country].owner == player.user_name:
                  map.d_continents[continent][country].owner = "Unoccupied"
         
      
   tempPlayers = copy.copy(l_dead_players)
   
   for i in range(len(tempPlayers)):
      curr_connection = tempPlayers[i].connection
      tempPlayers[i].connection = None
      packet = pickle.dumps((map, l_playerNames, d_playerCountries))
      try:
         curr_connection.sendto(packet, address)
         tempPlayers[i].connection = curr_connection
         print("Sent final map to spectator: " + tempPlayers[i].user_name)
      except:
         l_dead_players.remove(tempPlayers[i])

def applyContinentBonuses(l_players, map):
   for player in l_players:
      for continent_name, continent in map.d_continents.items():
         owns_continent = True
         i = 0
         while i < len(continent) and owns_continent:
            owns_continent = owns_continent and continent[i].owner == player.user_name
            i += 1
         
         if owns_continent:
            player.unit_counts += map.d_bonuses[continent_name]
            print("Awarding bonus for " + continent_name + " to " + player.user_name + ".")
            print(str(player.user_name) + ": " + str(player.unit_counts))
            
def getKey(item):
   return item[1]
   
def sortPlayers(l_playerNames, d_playerCountries):
   tempObject = []
   for name in l_playerNames:
      tempObject.append((name, d_playerCountries[name]))
   tempObject = sorted(tempObject, key=getKey, reverse=True)
   del l_playerNames[:]
   for name in tempObject:
      l_playerNames.append(name[0])
      print(name)

def serve(player_count, addr):   
   l_players = []
   l_dead_players = []
   
   print("Entering server")

   # create a socket object

   serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   # bind to the port
   serversocket.bind(addr)

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
      
   for player in l_players:
      l_playerNames.append(player.user_name)
      d_playerCountries[player.user_name] = 1
      
   #assemble the map
   print("got map")
   print("# of players: " + str(len(l_players)))
   map = Map(l_players)
   for player in l_players:
      curr_connection = player.connection
      player.connection = None
      packet = pickle.dumps((Map(map_to_copy=map, copy_player_name=player.user_name), player, l_playerNames, d_playerCountries))
      curr_connection.sendto(packet, addr)
      player.connection = curr_connection
      print("Sent to: " + player.user_name)
   
   while True:
      receivePlacements(l_players, l_dead_players, serversocket, map, addr)
      l_players = receiveAttacks(l_players, l_dead_players, serversocket, map, addr)
      if len(l_players) <= 0:
         print("Exiting server")
         break
      receiveMoves(l_players, l_dead_players, serversocket, map, addr)
      #temp = input("pausing the server")
   
   serversocket.close()