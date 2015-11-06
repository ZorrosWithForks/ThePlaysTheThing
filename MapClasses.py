import random

class unitCounts:
   def __init__(self, infantry, archers, cannons, champions):
      self.infantry  = infantry
      self.archers   = archers
      self.cannons   = cannons
      self.champions = champions
      

class Country:
   def __init__(self):
      self.name =  random.choice("PKBWLTCMNDL")
      self.name += random.choice("aeiou")
      self.name += random.choice("pblmnd")
      self.name += random.choice("pbwtcmnd")
      self.name += random.choice("aeiou")
      self.name += random.choice("pbwltcmndts")
      self.name += random.choice(["ington", "ford", "stan", "burgh", "mark", "ania", "mouth"])
      self.owner = None
      self.attack_bonus = random.randint(1, 10)
      self.defense_bonus = random.randint(1, 15)
      self.unit_production = 1
      self.unit_counts = unitCounts(random.randint(1, 5), random.randint(0, 2), 0, 0)

   def __repr__(self):
      return "{name:" + self.name + ", owner:" + str(self.owner) + ", attack_bonus:" + str(self.attack_bonus) + ", defense_bonus:" + str(self.defense_bonus) + ", unit_counts:" + str(self.unit_counts) + ", unit_production" + str(self.unit_production)
      
country = Country()
print (country.name)
print (country.owner)
print ("attack bonus =" + str(country.attack_bonus))
print ("defense bonus =" + str(country.defense_bonus))
print ("unit counts =" + str(country.unit_counts))