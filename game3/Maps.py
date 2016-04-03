import random

class Map:
   #######################################################
   # Note: In order to generate a new map object, call   #
   # this constructor without passing to map_to_copy or  #
   # copy_player_name. To create a copy of the map       #
   # with a limited view based on a particular player,   #
   # pass the map object to be copied to map_to_copy and #
   # the player name that the map data should be limited #
   # to.                                                 #
   #######################################################
   def __init__(self, l_players=None,  map_to_copy=None, copy_player_name=None):
      if map_to_copy == None and copy_player_name == None:
         #Generate new map
         self.l_player_names = []
         for player in l_players:
            self.l_player_names.append(player.user_name)
         
         self.PLAYER_COUNT = len(l_players)
         self.COUNTRY_COUNT = self.PLAYER_COUNT * 6 + 5
         self.WIDTH = 10
         self.HEIGHT = 7
         self.WATER = (0, 0) #Constant representing water in map, If a particular tile is not water, it's a country
         
         self.ll_map = [[self.WATER for x in range(self.WIDTH)] for y in range(self.HEIGHT)]
         self.ll_water_mask = [[int(random.getrandbits(2)) for x in range(self.WIDTH)] for y in range(self.HEIGHT)]
         print("In map: # of players: " + str(self.PLAYER_COUNT))
         # Generate list of countries
         l_countries = []
         for country in range(0, self.COUNTRY_COUNT):
            l_countries.append(Country())
         
         # Generate the name for, and put the minimum 3 countries in, each continent
         self.d_continents = {}
         self.l_continent_names = []
         continent_endings = ["sia", "rica", "rope", "tica", "lia", "ria", "gea", "ple"]
         random.shuffle(continent_endings)
         for continent in range(0, self.PLAYER_COUNT + 1):
            continent_name = random.choice("AEIOU")
            continent_name += random.choice("pbwtcmnds")
            continent_name += random.choice("aeiou")
            continent_name += continent_endings.pop()
            self.l_continent_names.append(continent_name)
            
            self.d_continents[continent_name] = l_countries[continent * 3:continent * 3 + 3]
         else:
            l_countries = l_countries[continent * 3 + 3:]
         
         # Randomly place the leftover countries
         for leftover in l_countries:
            self.d_continents[random.choice(self.l_continent_names)].append(leftover)
            
         # Generate unit bonus for each continent
         self.d_bonuses = {}
         for continent in self.l_continent_names:
            self.d_bonuses[continent] = len(self.d_continents[continent]) + random.randint(0, 2)
      
         start = True
         temp_valid_tiles = []
         # Populate the map next
         for continent in self.l_continent_names:
            for country in range(len(self.d_continents[continent])):
               valid_tiles_c2 = []
               valid_tiles_c1 = []
               valid_tiles_c0 = []
               #Search map for water tiles that neighbor 3 or more countries of the same continent
               for x in range(self.WIDTH):
                  for y in range(self.HEIGHT):
                     neighbor_count = 0
                     neighbor_count += 1 if str(self.ll_map[(y + 1) % self.HEIGHT][(x + 1) % self.WIDTH][0]) == continent else 0
                     neighbor_count += 1 if str(self.ll_map[(y + 1) % self.HEIGHT][(x - 1) % self.WIDTH][0]) == continent else 0
                     neighbor_count += 1 if str(self.ll_map[(y + 1) % self.HEIGHT][(x) % self.WIDTH][0]) == continent else 0
                     neighbor_count += 1 if str(self.ll_map[(y - 1) % self.HEIGHT][(x + 1) % self.WIDTH][0]) == continent else 0
                     neighbor_count += 1 if str(self.ll_map[(y - 1) % self.HEIGHT][(x - 1) % self.WIDTH][0]) == continent else 0
                     neighbor_count += 1 if str(self.ll_map[(y - 1) % self.HEIGHT][(x) % self.WIDTH][0]) == continent else 0
                     neighbor_count += 1 if str(self.ll_map[(y) % self.HEIGHT][(x + 1) % self.WIDTH][0]) == continent else 0
                     neighbor_count += 1 if str(self.ll_map[(y) % self.HEIGHT][(x - 1) % self.WIDTH][0]) == continent else 0
                     
                     if self.ll_map[y][x] == self.WATER and neighbor_count >= 2:
                        valid_tiles_c2.append((y, x))
                     elif self.ll_map[y][x] == self.WATER and neighbor_count == 1:
                        valid_tiles_c1.append((y, x))
                     elif self.ll_map[y][x] == self.WATER and neighbor_count == 0:
                        valid_tiles_c0.append((y, x))
               
               if len(valid_tiles_c2) > 0:
                  temp_tile = random.choice(valid_tiles_c2)
                  self.ll_map[temp_tile[0]][temp_tile[1]] = (continent, country)
               elif len(valid_tiles_c1) > 0:
                  temp_tile = random.choice(valid_tiles_c1)
                  self.ll_map[temp_tile[0]][temp_tile[1]] = (continent, country)
               elif start:
                  self.ll_map[int(self.HEIGHT / 2) + random.randint(-1, 1)][int(self.WIDTH / 2) + random.randint(-2, 2)] = (continent, country)
                  start = False
               else:
                  temp_tile = random.choice(temp_valid_tiles)
                  self.ll_map[temp_tile[0]][temp_tile[1]] = (continent, country)
               temp_valid_tiles = valid_tiles_c1
         
         l_start_locals1 = []
         l_start_locals2 = []
         for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
               if x % 3 == 1 and y % 3 == 1 and self.ll_map[y][x] != self.WATER:
                  l_start_locals1.append(self.ll_map[y][x])
               elif x % 3 == 2 and y % 3 == 2 and self.ll_map[y][x] != self.WATER:
                  l_start_locals2.append(self.ll_map[y][x])
         
         print("lengths for double space: " + str(len(l_start_locals1)) + str(len(l_start_locals2)))
         if len(l_start_locals1) >= len(self.l_player_names):
            l_locals = l_start_locals1
            print("True for 2 space")
         elif len(l_start_locals2) >= len(self.l_player_names):
            l_locals = l_start_locals2
            print("True for 2 space")
         else:
            l_locals = []
            l_start_locals1 = []
            for x in range(self.WIDTH):
               for y in range(self.HEIGHT):
                  if x % 2 == 1 and y % 2 == 1 and self.ll_map[y][x] != self.WATER:
                     l_start_locals1.append(self.ll_map[y][x])
            
            if len(l_start_locals1) >= len(self.l_player_names):
               l_locals = l_start_locals1
               print("True for 1 space")
         random.shuffle(l_locals)
         if len(l_locals) >= len(self.l_player_names):
            for player_index in range(0, len(self.l_player_names)):
               self.d_continents[l_locals[player_index][0]][l_locals[player_index][1]].owner = self.l_player_names[player_index]
               self.d_continents[l_locals[player_index][0]][l_locals[player_index][1]].unit_counts = UnitCounts(0, 0, 0, 0)
               self.d_continents[l_locals[player_index][0]][l_locals[player_index][1]].defense_bonus = 10
               self.d_continents[l_locals[player_index][0]][l_locals[player_index][1]].attack_bonus = 10
         else:
            for player_index in range(0, len(self.l_player_names)):
               self.d_continents[self.l_continent_names[player_index]][0].owner = self.l_player_names[player_index]
               self.d_continents[self.l_continent_names[player_index]][0].unit_counts = UnitCounts(0, 0, 0, 0)
               self.d_continents[self.l_continent_names[player_index]][0].defense_bonus = 10
               self.d_continents[self.l_continent_names[player_index]][0].attack_bonus = 10
      else:
         #Make copy of the map limited by player
         self.PLAYER_COUNT = map_to_copy.PLAYER_COUNT
         self.COUNTRY_COUNT = map_to_copy.COUNTRY_COUNT
         self.WIDTH = 10
         self.HEIGHT = 7
         self.WATER = (0, 0)
         
         #Copy player names list
         self.l_player_names = []
         for name in map_to_copy.l_player_names:
            self.l_player_names.append(name)
            
         self.d_continents = {}
         self.l_continent_names = []
         #Copy list of continent names
         for name in map_to_copy.l_continent_names:
            self.l_continent_names.append(name)
         
         for name in self.l_continent_names:
            self.d_continents[name] = []
            for country in map_to_copy.d_continents[name]:
               self.d_continents[name].append(Country(country))
               
         self.d_bonuses = {} 
         for name in self.l_continent_names:
            self.d_bonuses[name] = map_to_copy.d_bonuses[name]
         
         self.ll_map = []
         for y in range(len(map_to_copy.ll_map)):
            self.ll_map.append([])
            for x in range(len(map_to_copy.ll_map[y])):
               self.ll_map[y].append((map_to_copy.ll_map[y][x][0], map_to_copy.ll_map[y][x][1]))
         
         self.ll_water_mask = []
         for y in range(len(map_to_copy.ll_water_mask)):
            self.ll_water_mask.append([])
            for x in range(len(map_to_copy.ll_water_mask[y])):
               self.ll_water_mask[y].append(map_to_copy.ll_water_mask[y][x])
               
         for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
               neighbor_is_player = 0
               if self.ll_map[(y + 1) % self.HEIGHT][(x + 1) % self.WIDTH] != self.WATER:
                  neighbor_is_player += 1 if self.d_continents[self.ll_map[(y + 1) % self.HEIGHT][(x + 1) % self.WIDTH][0]][self.ll_map[(y + 1) % self.HEIGHT][(x + 1) % self.WIDTH][1]].owner == copy_player_name else 0
               if self.ll_map[(y + 1) % self.HEIGHT][(x - 1) % self.WIDTH] != self.WATER:
                  neighbor_is_player += 1 if self.d_continents[self.ll_map[(y + 1) % self.HEIGHT][(x - 1) % self.WIDTH][0]][self.ll_map[(y + 1) % self.HEIGHT][(x - 1) % self.WIDTH][1]].owner == copy_player_name else 0
               if self.ll_map[(y + 1) % self.HEIGHT][(x) % self.WIDTH] != self.WATER:
                  neighbor_is_player += 1 if self.d_continents[self.ll_map[(y + 1) % self.HEIGHT][(x) % self.WIDTH][0]][self.ll_map[(y + 1) % self.HEIGHT][(x) % self.WIDTH][1]].owner == copy_player_name else 0
               if self.ll_map[(y - 1) % self.HEIGHT][(x + 1) % self.WIDTH] != self.WATER:
                  neighbor_is_player += 1 if self.d_continents[self.ll_map[(y - 1) % self.HEIGHT][(x + 1) % self.WIDTH][0]][self.ll_map[(y - 1) % self.HEIGHT][(x + 1) % self.WIDTH][1]].owner == copy_player_name else 0
               if self.ll_map[(y - 1) % self.HEIGHT][(x - 1) % self.WIDTH] != self.WATER:
                  neighbor_is_player += 1 if self.d_continents[self.ll_map[(y - 1) % self.HEIGHT][(x - 1) % self.WIDTH][0]][self.ll_map[(y - 1) % self.HEIGHT][(x - 1) % self.WIDTH][1]].owner == copy_player_name else 0
               if self.ll_map[(y - 1) % self.HEIGHT][(x) % self.WIDTH] != self.WATER:
                  neighbor_is_player += 1 if self.d_continents[self.ll_map[(y - 1) % self.HEIGHT][(x) % self.WIDTH][0]][self.ll_map[(y - 1) % self.HEIGHT][(x) % self.WIDTH][1]].owner == copy_player_name else 0
               if self.ll_map[(y) % self.HEIGHT][(x + 1) % self.WIDTH] != self.WATER:
                  neighbor_is_player += 1 if self.d_continents[self.ll_map[(y) % self.HEIGHT][(x + 1) % self.WIDTH][0]][self.ll_map[(y) % self.HEIGHT][(x + 1) % self.WIDTH][1]].owner == copy_player_name else 0
               if self.ll_map[(y) % self.HEIGHT][(x - 1) % self.WIDTH] != self.WATER:
                  neighbor_is_player += 1 if self.d_continents[self.ll_map[(y) % self.HEIGHT][(x - 1) % self.WIDTH][0]][self.ll_map[(y) % self.HEIGHT][(x - 1) % self.WIDTH][1]].owner == copy_player_name else 0
               if self.ll_map[(y) % self.HEIGHT][(x) % self.WIDTH] != self.WATER:
                  neighbor_is_player += 1 if self.d_continents[self.ll_map[(y) % self.HEIGHT][(x) % self.WIDTH][0]][self.ll_map[(y) % self.HEIGHT][(x) % self.WIDTH][1]].owner == copy_player_name else 0
               
               if neighbor_is_player == 0 and self.ll_map[y][x] != self.WATER:
                  #Player and unit information is hidden from the player on tiles not directly adjacent to a tile the player owns 
                  self.d_continents[self.ll_map[y][x][0]][self.ll_map[y][x][1]].owner = None
                  self.d_continents[self.ll_map[y][x][0]][self.ll_map[y][x][1]].attack_bonus = None
                  self.d_continents[self.ll_map[y][x][0]][self.ll_map[y][x][1]].defense_bonus = None
                  self.d_continents[self.ll_map[y][x][0]][self.ll_map[y][x][1]].unit_production = None
                  self.d_continents[self.ll_map[y][x][0]][self.ll_map[y][x][1]].unit_counts = None
                  
class UnitCounts:
   def __init__(self, infantry, archers, cannons, champions):
      self.infantry  = infantry
      self.archers   = archers
      self.cannons   = cannons
      self.champions = champions
   
   def __repr__(self):
      return "{infantry:" + str(self.infantry) + ",\n archers:" + str(self.archers) + ",\n cannons:" + str(self.cannons) + ",\n champions:" + str(self.champions) + "}"

   def getSummaryCount(self):
      return self.infantry + self.archers + self.cannons + self.champions
   
class Country:
   def __init__(self, country_to_copy=None):
      if country_to_copy == None:
         self.name = "" if random.randint(1, 10) != 1 else random.choice(["Great", "Greater", "Lesser", "North", "South", "East", "West", "New", "Republic of", "Kingdom of"]) + " " 
         self.name += random.choice("PKBWLTCMNDL")
         self.name += random.choice("aeiou")
         self.name += random.choice("pblwnd")
         self.name += random.choice("pbwtcmnd")
         self.name += random.choice("aeiou")
         self.name += random.choice("pbwltcmndts")
         vowel = random.choice("aeiou")
         self.name += random.choice(["ingt" + vowel + "n", "f" + vowel + "rd", "st" + vowel + "n", "b" + vowel + "rgh", "mark", vowel + "nia", "m" + vowel + "th"])
         self.owner = "Unoccupied"
         self.attack_bonus = random.randint(1, 10)
         self.defense_bonus = random.randint(1, 15)
         self.unit_production = 1
         self.unit_counts = UnitCounts(random.randint(1, 5), random.randint(0, 2), 0, 0)
      else:
         self.name = country_to_copy.name
         self.owner = country_to_copy.owner
         self.attack_bonus = country_to_copy.attack_bonus
         self.defense_bonus = country_to_copy.defense_bonus
         self.unit_production = country_to_copy.unit_production
         if country_to_copy.unit_counts != None:
            self.unit_counts = UnitCounts(country_to_copy.unit_counts.infantry, country_to_copy.unit_counts.archers, country_to_copy.unit_counts.cannons, country_to_copy.unit_counts.champions)

   def __repr__(self):
      return "{name:" + self.name + ",\n owner:" + str(self.owner) + ",\n attack_bonus:" + str(self.attack_bonus) + ",\n defense_bonus:" + str(self.defense_bonus) + ",\n unit_counts:" + str(self.unit_counts) + ",\n unit_production" + str(self.unit_production) + "}"