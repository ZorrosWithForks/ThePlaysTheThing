import random

class unitCounts:
   def __init__(self, infantry, archers, cannons, champions):
      self.infantry  = infantry
      self.archers   = archers
      self.cannons   = cannons
      self.champions = champions
      

class Country:
   def __init__(self):
      self.name = random.choice("PKBWLTCMNDL")
      self.name += random.choice("aeiou")
      self.name += random.choice("pkbwltcmndl")
      self.name += random.choice("aeiou")
      self.name += random.choice("pkbwltcmndl")
      self.name += random.choice(["ington", "ford", "stan", "burgh", "mark"])
      print(self.name)
      self.owner = None
      self.attack_bonus = random.randint(1, 10)
      self.defense_bonus = random.randint(1, 15)
      print(self.attack_bonus)
      print(self.defense_bonus)
      self.unit_production = 1
      self.unit_counts = unitCounts(random.randint(1, 5), random.randint(0, 2), 0, 0)
      