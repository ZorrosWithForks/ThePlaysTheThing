class Player:
   def __init__(self, user_name, connection_object):
      self.user_name = user_name
      self.unit_points = 50 #This is subject to change
      self.connection_object = connection_object #Connection data object
      self.unit_totals       = unitCounts(0, 0, 0, 0)
      
def addUnits(player, country, unit):
   if unit == "infantry" and player.unit_points >= 3:
      player.unit_points -= 3
      country.unitCounts.infantry += 1
      player.unit_totals.infantry += 1
   elif unit == "archer" and player.unit_points >= 5:
      player.unit_points -= 5
      country.unitCounts.archers += 1
      player.unit_totals.archers += 1
   elif unit == "cannon" and player.unit_points >= 5:
      player.unit_points -= 5
      country.unitCounts.cannons += 1
      player.unit_totals.cannons += 1
   elif unit == "champion" and player.unit_points >= 7:
      player.unit_points -= 7
      country.unitCounts.champions += 1
      player.unit_totals.champions += 1