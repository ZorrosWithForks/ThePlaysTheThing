class Player:
   def __init__(self, user_name, connection_object):
      self.user_name = user_name
      self.unit_counts = 50 #This is subject to change
      self.connection_object = connection_object #Connection data object