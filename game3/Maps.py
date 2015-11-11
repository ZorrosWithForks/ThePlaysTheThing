import random

class Map:
   def __init__(self, player_count):
      self.WIDTH = 11
      self.HEIGHT = 8
      self.WATER = 0 #Constant representing water in map, If a particular tile is not water, it's a country
      
      self.ll_map = [[self.WATER for x in range(self.WIDTH)] for x in range(self.HEIGHT)]
      
      # Generate list of countries
      l_countries = []
      for country in range(0, player_count * 6 + 5):
         l_countries.append(Country())
         print(l_countries[country]) #Remove!
      
      # Generate the name for, and put the minimum 3 countries in, each continent
      self.d_continents = {}
      self.l_continent_names = []
      for continent in range(0, player_count + 1):
         continent_name = random.choice("AEIOU")
         continent_name += random.choice("pbwtcmnds")
         continent_name += random.choice("aeiou")
         continent_name += random.choice(["sia", "rica", "rope", "tica", "lia"])
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
         self.d_bonuses[continent] = self.d_continents[continent].length() + random.randint(0, 2)
         
      #########################
      # Populate the map next #
      #########################
      # Assemble each continent
      for continent in self.l_continent_names:
         for country in self.d_continents[continent]:
            None #Will fill in later
            

class UnitCounts:
   def __init__(self, infantry, archers, cannons, champions):
      self.infantry  = infantry
      self.archers   = archers
      self.cannons   = cannons
      self.champions = champions
   
   def __repr__(self):
      return "{infantry:" + str(self.infantry) + ", archers:" + str(self.archers) + ", cannons:" + str(self.cannons) + ", champions:" + str(self.champions) + "}"

class Country:
   def __init__(self):
      self.name =  random.choice("PKBWLTCMNDL")
      self.name += random.choice("aeiou")
      self.name += random.choice("pblmnd")
      self.name += random.choice("pbwtcmnd")
      self.name += random.choice("aeiou")
      self.name += random.choice("pbwltcmndts")
      vowel = random.choice("aeiou")
      self.name += random.choice(["ingt" + vowel + "n", "f" + vowel + "rd", "st" + vowel + "n", "b" + vowel + "rgh", "mark", vowel + "nia", "m" + vowel + "th"])
      self.owner = None
      self.attack_bonus = random.randint(1, 10)
      self.defense_bonus = random.randint(1, 15)
      self.unit_production = 1
      self.unit_counts = UnitCounts(random.randint(1, 5), random.randint(0, 2), 0, 0)

   def __repr__(self):
      return "{name:" + self.name + ", owner:" + str(self.owner) + ", attack_bonus:" + str(self.attack_bonus) + ", defense_bonus:" + str(self.defense_bonus) + ", unit_counts:" + str(self.unit_counts) + ", unit_production" + str(self.unit_production) + "}"