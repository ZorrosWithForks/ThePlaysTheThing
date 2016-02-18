#client.py
import socket
import os
import threading
from threading import Thread
import _thread
import pygame, sys, random
from pygame.locals import *
from pygame import font
import pickle
from Maps import *
import time
import Player

pygame.font.init()

pygame.init()

fpsClock = pygame.time.Clock()
   
#constants representing the different resources
IMAGE_FILE_PATH = "ImageFiles\\"
CONTINENT_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 40)
COUNTRY_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 25)
UNIT_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 35)
MONEY_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 22)
CONTINENT_1 = 1
CONTINENT_2 = 2
CONTINENT_3 = 3
CONTINENT_4 = 4
CONTINENT_5 = 5
CONTINENT_6 = 6
CONTINENT_7 = 7
CONTINENT_8 = 8
UNOCCUPIED = "Unoccupied"
WATER = (0,0)
DEEP_WATER = 10
OVERLAY = 9

class CursorGraphic:
   def __init__(self):
      self.CursorOver = False
      self.ON = pygame.image.load(IMAGE_FILE_PATH + 'CursorOn.png')
      
   def updateCursor(self, DISPLAYSURF):
      x, y = pygame.mouse.get_pos()
      if self.CursorOver:
         DISPLAYSURF.blit(self.ON, (x - 50, y - 50))

playCursor = CursorGraphic()

# Graphics Constants
MOUSE_OVER = pygame.image.load(IMAGE_FILE_PATH + 'MouseOver.png')
MOUSE_OVER_UNKNOWN = pygame.image.load(IMAGE_FILE_PATH + 'MouseOverUnknown.png')
INFO_MARQUEE = pygame.image.load(IMAGE_FILE_PATH + "InfoMarque.png")
INFO_OVERLAY = pygame.image.load(IMAGE_FILE_PATH + "InfoMarqueOverlay.png")
MAP_FRAME = pygame.image.load(IMAGE_FILE_PATH + "MapFrame.png")
MAP_LIGHT = pygame.image.load(IMAGE_FILE_PATH + "MapLighting.png")
SELECTED_TILE = pygame.image.load(IMAGE_FILE_PATH + "Selected.png")

#a dictionary linking resources to textures
textures =   {
                WATER  : pygame.image.load(IMAGE_FILE_PATH + 'water.png'),
                DEEP_WATER : pygame.image.load(IMAGE_FILE_PATH + 'deep_water.png'),
                OVERLAY : pygame.image.load(IMAGE_FILE_PATH + 'overlay.png'),
                CONTINENT_1 : pygame.image.load(IMAGE_FILE_PATH + 'continent_1.png'),
                CONTINENT_2 : pygame.image.load(IMAGE_FILE_PATH + 'continent_2.png'),
                CONTINENT_3 : pygame.image.load(IMAGE_FILE_PATH + 'continent_3.png'),
                CONTINENT_4 : pygame.image.load(IMAGE_FILE_PATH + 'continent_4.png'),
                CONTINENT_5 : pygame.image.load(IMAGE_FILE_PATH + 'continent_5.png'),
                CONTINENT_6 : pygame.image.load(IMAGE_FILE_PATH + 'continent_6.png'),
                CONTINENT_7 : pygame.image.load(IMAGE_FILE_PATH + 'continent_7.png'),
                CONTINENT_8 : pygame.image.load(IMAGE_FILE_PATH + 'continent_8.png'),
            }

l_playerLogos = [
                pygame.image.load(IMAGE_FILE_PATH + 'NoPlayer.png'),
                pygame.image.load(IMAGE_FILE_PATH + 'Player1.png'),
                pygame.image.load(IMAGE_FILE_PATH + 'Player2.png'),
                pygame.image.load(IMAGE_FILE_PATH + 'Player3.png'),
                pygame.image.load(IMAGE_FILE_PATH + 'Player4.png'),
                pygame.image.load(IMAGE_FILE_PATH + 'Player5.png'),
                pygame.image.load(IMAGE_FILE_PATH + 'Player6.png'),
                pygame.image.load(IMAGE_FILE_PATH + 'Player7.png')
              ]

d_playerLogoIndexes = { UNOCCUPIED: 0 }

#useful game dimensions
MARGIN = 50
TILESIZE  = 100
BOTTOM_HALF_START = 15

d_continent_tiles = {}

def moveMap(x_offset, y_offset, map):
   ll_temp_map = [[map.WATER for x in range(map.WIDTH)] for y in range(map.HEIGHT)]
   for row in range(map.HEIGHT):
      for column in range(map.WIDTH):
         ll_temp_map[row][column] = map.ll_map[(row + y_offset) % map.HEIGHT][(column + x_offset) % map.WIDTH]
   map.ll_map = ll_temp_map

def standardInfo(map, DISPLAYSURF, params):
    #Highlight country mouse is over and display country info
    curr_x, curr_y = pygame.mouse.get_pos()
    if (curr_x < map.WIDTH * TILESIZE and curr_y < map.HEIGHT * TILESIZE and map.ll_map[int(curr_y / TILESIZE)][int(curr_x / TILESIZE)] != map.WATER):
      curr_country = map.ll_map[int(curr_y / TILESIZE)][int(curr_x / TILESIZE)]
      DISPLAYSURF.blit(MOUSE_OVER if map.d_continents[curr_country[0]][curr_country[1]].owner != None else MOUSE_OVER_UNKNOWN, (int(curr_x / TILESIZE) * TILESIZE - MARGIN, int(curr_y / TILESIZE) * TILESIZE - MARGIN), special_flags=BLEND_ADD)
      current_tile = map.ll_map[int(curr_y / TILESIZE)][int(curr_x / TILESIZE)]
      DISPLAYSURF.blit(CONTINENT_FONT.render("Continent: " + current_tile[0], True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 120))
      DISPLAYSURF.blit(COUNTRY_FONT.render("Country: " + map.d_continents[current_tile[0]][current_tile[1]].name, True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 170))
      
      if map.d_continents[current_tile[0]][current_tile[1]].owner != None: 
         # Unit counts by type
         DISPLAYSURF.blit(COUNTRY_FONT.render("Pistoleers: " + str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.infantry), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 225))
         DISPLAYSURF.blit(COUNTRY_FONT.render("Musketeers: " + str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.archers), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 250))
         DISPLAYSURF.blit(COUNTRY_FONT.render("Cannons: " + str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.cannons), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 275))
         DISPLAYSURF.blit(COUNTRY_FONT.render("Airships: " + str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.champions), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 300))
         
         # Country bonuses
         DISPLAYSURF.blit(COUNTRY_FONT.render("Attack Bonus: " + str(map.d_continents[current_tile[0]][current_tile[1]].attack_bonus), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 350))
         DISPLAYSURF.blit(COUNTRY_FONT.render("Defense Bonus: " + str(map.d_continents[current_tile[0]][current_tile[1]].defense_bonus), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 375))
         
         # Owner
         DISPLAYSURF.blit(COUNTRY_FONT.render("Owner: " + str(map.d_continents[current_tile[0]][current_tile[1]].owner if map.d_continents[current_tile[0]][current_tile[1]].owner != None else "Neutral"), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 425))
         
         DISPLAYSURF.blit(CONTINENT_FONT.render("Continent Bonus: " + str(map.d_bonuses[current_tile[0]]), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 500))
    else:
      x_offset = 120
      y_offset = 180
      DISPLAYSURF.blit(CONTINENT_FONT.render("Players:", True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 130))
      for name in map.l_player_names:
         DISPLAYSURF.blit(COUNTRY_FONT.render(name, True, (0,0,0)), (map.WIDTH * TILESIZE + x_offset, y_offset))
         y_offset += 25
      y_offset += 25
      DISPLAYSURF.blit(CONTINENT_FONT.render("Continent Strengths:", True, (0,0,0)), (map.WIDTH * TILESIZE + 100, y_offset))
      y_offset += 20
      for continent_name in map.l_continent_names:
         y_offset += 25
         DISPLAYSURF.blit(COUNTRY_FONT.render(continent_name + ": " + str(map.d_bonuses[continent_name]), True, (0,0,0)), (map.WIDTH * TILESIZE + x_offset, y_offset))

def selectedInfo(map, DISPLAYSURF, params):
    current_tile = map.ll_map[params[1]][params[0]]

    # Unit counts by type
    DISPLAYSURF.blit(COUNTRY_FONT.render("Pistoleers: " + str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.infantry), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 225))
    DISPLAYSURF.blit(COUNTRY_FONT.render("Musketeers: " + str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.archers), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 250))
    DISPLAYSURF.blit(COUNTRY_FONT.render("Cannons: " + str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.cannons), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 275))
    DISPLAYSURF.blit(COUNTRY_FONT.render("Airships: " + str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.champions), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 300))
    
    # Country bonuses
    DISPLAYSURF.blit(COUNTRY_FONT.render("Attack Bonus: " + str(map.d_continents[current_tile[0]][current_tile[1]].attack_bonus), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 350))
    DISPLAYSURF.blit(COUNTRY_FONT.render("Defense Bonus: " + str(map.d_continents[current_tile[0]][current_tile[1]].defense_bonus), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 375))
    
    # Owner
    DISPLAYSURF.blit(COUNTRY_FONT.render("Owner: " + str(map.d_continents[current_tile[0]][current_tile[1]].owner if map.d_continents[current_tile[0]][current_tile[1]].owner != None else "Neutral"), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 425))
    
    DISPLAYSURF.blit(CONTINENT_FONT.render("Continent Bonus: " + str(map.d_bonuses[current_tile[0]]), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 500))
    
def printMap(map, DISPLAYSURF, infoDisplay, params=None):
    #loop through each row
    for row in range(map.HEIGHT):
        #loop through each column in the row
        for column in range(map.WIDTH):
            #draw the resource at that position in the tilemap, using the correct colour
            if (map.ll_map[row][column] != WATER):
               DISPLAYSURF.blit(textures[d_continent_tiles[map.ll_map[row][column][0]]], (((column) % map.WIDTH) * TILESIZE, ((row) % map.HEIGHT) * TILESIZE))
  
    #loop through each row
    for row in range(map.HEIGHT):
        #loop through each column in the row
        for column in range(map.WIDTH):
            #draw the resource at that position in the tilemap, using the correct colour
            if (map.ll_map[row][column] == WATER):
               DISPLAYSURF.blit(textures[WATER], (((column) % map.WIDTH) * TILESIZE - MARGIN, ((row) % map.HEIGHT) * TILESIZE - MARGIN))
          
    #loop through each row
    for row in range(map.HEIGHT):
        #loop through each column in the row
        for column in range(map.WIDTH):
            #draw the resource at that position in the tilemap, using the correct colour
            if (map.ll_map[row][column] == WATER):
               DISPLAYSURF.blit(textures[DEEP_WATER], (((column) % map.WIDTH) * TILESIZE - MARGIN, ((row) % map.HEIGHT) * TILESIZE - MARGIN))

    DISPLAYSURF.blit(source=textures[OVERLAY], dest=(0,0), special_flags=BLEND_MULT)
    DISPLAYSURF.blit(MAP_FRAME, dest=(0,0))
    DISPLAYSURF.blit(MAP_LIGHT, dest=(0,0), special_flags=BLEND_ADD)
			   
	 #loop through each row
    for row in range(map.HEIGHT):
        #loop through each column in the row
        for column in range(map.WIDTH):
            #draw the resource at that position in the tilemap, using the correct colour
            if (map.ll_map[row][column] != WATER):
               current_country = map.d_continents[map.ll_map[row][column][0]][map.ll_map[row][column][1]]
               if current_country.owner != None:
                  DISPLAYSURF.blit(l_playerLogos[d_playerLogoIndexes[current_country.owner]], (((column) % map.WIDTH) * TILESIZE, ((row) % map.HEIGHT) * TILESIZE))
                  count = str(current_country.unit_counts.getSummaryCount())
                  DISPLAYSURF.blit(UNIT_FONT.render(count, True, (0,0,0)), (((column) % map.WIDTH) * TILESIZE + 45 - len(count) * 7, ((row) % map.HEIGHT) * TILESIZE + 25))

    DISPLAYSURF.blit(source=INFO_MARQUEE, dest=(map.WIDTH * TILESIZE, 0))
    DISPLAYSURF.blit(source=pygame.image.load(IMAGE_FILE_PATH + "BaseBoard.png"), dest=(0, map.HEIGHT * TILESIZE))
    
    infoDisplay(map, DISPLAYSURF, params)

    DISPLAYSURF.blit(source=INFO_OVERLAY, dest=(map.WIDTH * TILESIZE, 0), special_flags=BLEND_RGBA_ADD)

def handleGeneral(event, map, map_X_offset, map_Y_offset, temp_map=None):
  if event.type == QUIT:
      #and the game and close the window
      pygame.quit()
      sys.exit()
  pygame.mouse.set_visible(True)

  #if a key is pressed
  if event.type == KEYDOWN:
      if event.key == K_i:
         pygame.display.iconify()
      if event.key == K_ESCAPE:
         #and the game and close the window
         pygame.quit()
         sys.exit()
      #if the right arrow is pressed
      if event.key == K_RIGHT:
         #Change the map render offset
         map_X_offset = (map_X_offset - 1) % map.WIDTH
         moveMap(1, 0, map)
         if temp_map != None: moveMap(1, 0, temp_map)
      if event.key == K_LEFT:
         #Change the map render offset
         map_X_offset = (map_X_offset + 1) % map.WIDTH
         moveMap(-1, 0, map)
         if temp_map != None: moveMap(-1, 0, temp_map)
      if event.key == K_UP:
         #Change the map render offset
         map_Y_offset = (map_Y_offset + 1) % map.HEIGHT
         moveMap(0, -1, map)
         if temp_map != None: moveMap(0, -1, temp_map)
      if event.key == K_DOWN:
         #Change the map render offset
         map_Y_offset = (map_Y_offset - 1) % map.HEIGHT
         moveMap(0, 1, map)
         if temp_map != None: moveMap(0, 1, temp_map)

def placeUnits(DISPLAYSURF, map, map_X_offset, map_Y_offset, player):
   BUY_PISTOLEERS = pygame.image.load(IMAGE_FILE_PATH + "PistoleersBuy.png")
   BUY_MUSKETEERS = pygame.image.load(IMAGE_FILE_PATH + "MusketeersBuy.png")
   BUY_CANNONS = pygame.image.load(IMAGE_FILE_PATH + "CannonBuy.png")
   BUY_AIRSHIPS = pygame.image.load(IMAGE_FILE_PATH + "AirshipBuy.png")
   MONEY_SCREEN = pygame.image.load(IMAGE_FILE_PATH + "MoneyScreen.png")
   DONE_BUTTON = pygame.image.load(IMAGE_FILE_PATH + "DoneButton.png")
   DONE_BUTTON_ACTIVE = pygame.image.load(IMAGE_FILE_PATH + "DoneButtonActive.png")
   placing = True
   selectedCountry = None
   temp_map = Map(map_to_copy=map, copy_player_name=player.user_name)
   
   while placing:          
       #get all the user events
       curr_x, curr_y = pygame.mouse.get_pos()
       for event in pygame.event.get():
           #if the user wants to quit
           if selectedCountry == None:
              handleGeneral(event, map, map_X_offset, map_Y_offset, temp_map)
           
           if event.type == MOUSEBUTTONDOWN:
             if curr_x < map.WIDTH * TILESIZE and curr_y < map.HEIGHT * TILESIZE:
                curr_country = map.ll_map[int(curr_y / TILESIZE)][int(curr_x / TILESIZE)]
                if (curr_country != map.WATER and map.d_continents[curr_country[0]][curr_country[1]].owner == map.current_player):
                  if selectedCountry == None or selectedCountry != (int(curr_x / TILESIZE), int(curr_y / TILESIZE)):
                     selectedCountry = (int(curr_x / TILESIZE), int(curr_y / TILESIZE))
                  else:
                     selectedCountry = None
             elif selectedCountry != None:
                curr_country = map.ll_map[selectedCountry[1]][selectedCountry[0]]
                
                #Pistoleers
                if 175 + 250 <= curr_x <= 175 + 300 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120: # "All" for Pistoleers
                  map.d_continents[curr_country[0]][curr_country[1]].unit_counts.infantry += player.unit_counts
                  player.unit_counts = 0
                elif 175 + 300 <= curr_x <= 175 + 350 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120 and player.unit_counts > 0: # "+" for Pistoleers
                  map.d_continents[curr_country[0]][curr_country[1]].unit_counts.infantry += 1
                  player.unit_counts -= 1
                elif 175 + 350 <= curr_x <= 175 + 400 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120: # "-" for Pistoleers
                  if map.d_continents[curr_country[0]][curr_country[1]].unit_counts.infantry > temp_map.d_continents[curr_country[0]][curr_country[1]].unit_counts.infantry:
                     map.d_continents[curr_country[0]][curr_country[1]].unit_counts.infantry -= 1
                     player.unit_counts += 1
                
                #Musketeers
                if 580 + 250 <= curr_x <= 580 + 300 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120: # "All" for Musketeers
                  map.d_continents[curr_country[0]][curr_country[1]].unit_counts.archers += int(player.unit_counts / 2)
                  player.unit_counts = player.unit_counts % 2
                elif 580 + 300 <= curr_x <= 580 + 350 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120 and player.unit_counts > 1: # "+" for Musketeers
                  map.d_continents[curr_country[0]][curr_country[1]].unit_counts.archers += 1
                  player.unit_counts -= 2
                elif 580 + 350 <= curr_x <= 580 + 400 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120: # "-" for Musketeers
                  if map.d_continents[curr_country[0]][curr_country[1]].unit_counts.archers > temp_map.d_continents[curr_country[0]][curr_country[1]].unit_counts.archers:
                     map.d_continents[curr_country[0]][curr_country[1]].unit_counts.archers -= 1
                     player.unit_counts += 2
                     
                #Cannons
                if 175 + 250 <= curr_x <= 175 + 300 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175: # "All" for Cannons
                  map.d_continents[curr_country[0]][curr_country[1]].unit_counts.cannons += int(player.unit_counts / 2)
                  player.unit_counts = player.unit_counts % 2
                elif 175 + 300 <= curr_x <= 175 + 350 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175 and player.unit_counts > 1: # "+" for Cannons
                  map.d_continents[curr_country[0]][curr_country[1]].unit_counts.cannons += 1
                  player.unit_counts -= 2
                elif 175 + 350 <= curr_x <= 175 + 400 and map.HEIGHT * TILESIZE + 125 < curr_y <= map.HEIGHT * TILESIZE + 175: # "-" for Cannons
                  if map.d_continents[curr_country[0]][curr_country[1]].unit_counts.cannons > temp_map.d_continents[curr_country[0]][curr_country[1]].unit_counts.cannons:
                     map.d_continents[curr_country[0]][curr_country[1]].unit_counts.cannons -= 1
                     player.unit_counts += 2
                     
                #Airships
                if 580 + 250 <= curr_x <= 580 + 300 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175: # "All" for Airships
                  map.d_continents[curr_country[0]][curr_country[1]].unit_counts.champions += int(player.unit_counts / 5)
                  player.unit_counts = player.unit_counts % 5
                elif 580 + 300 <= curr_x <= 580 + 350 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175 and player.unit_counts > 4: # "+" for Airships
                  map.d_continents[curr_country[0]][curr_country[1]].unit_counts.champions += 1
                  player.unit_counts -= 5
                elif 580 + 350 <= curr_x <= 580 + 400 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175: # "-" for Airships
                  if map.d_continents[curr_country[0]][curr_country[1]].unit_counts.champions > temp_map.d_continents[curr_country[0]][curr_country[1]].unit_counts.champions:
                     map.d_continents[curr_country[0]][curr_country[1]].unit_counts.champions -= 1
                     player.unit_counts += 5
                
       if selectedCountry != None:
          selectedCountry = (selectedCountry[0] + map_X_offset, selectedCountry[1] + map_Y_offset)
       
       if selectedCountry == None:
         printMap(map, DISPLAYSURF, standardInfo)
       else:
         printMap(map, DISPLAYSURF, selectedInfo, selectedCountry)
       
       if selectedCountry != None:
         DISPLAYSURF.blit(SELECTED_TILE, (selectedCountry[0] * TILESIZE, selectedCountry[1] * TILESIZE), special_flags=BLEND_ADD)
       
       DISPLAYSURF.blit(MONEY_SCREEN, (70, map.HEIGHT * TILESIZE + 70))
       DISPLAYSURF.blit(MONEY_FONT.render(str(player.unit_counts), True, (255, 0, 0)), (95, map.HEIGHT * TILESIZE + 103))
       DISPLAYSURF.blit(BUY_PISTOLEERS, (170, map.HEIGHT * TILESIZE + 70))
       DISPLAYSURF.blit(BUY_MUSKETEERS, (575, map.HEIGHT * TILESIZE + 70))
       DISPLAYSURF.blit(BUY_CANNONS, (170, map.HEIGHT * TILESIZE + 125))
       DISPLAYSURF.blit(BUY_AIRSHIPS, (575, map.HEIGHT * TILESIZE + 125))
       DISPLAYSURF.blit(DONE_BUTTON if player.unit_counts > 0 else DONE_BUTTON_ACTIVE, (980, map.HEIGHT * TILESIZE + 70))
       
       playCursor.CursorOver = (175 + 250 <= curr_x <= 175 + 400 or 580 + 250 <= curr_x <= 580 + 400)
       playCursor.CursorOver = playCursor.CursorOver and (map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120 or map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175)
       playCursor.CursorOver = playCursor.CursorOver or (980 <= curr_x <= 1080 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 175)
       playCursor.updateCursor(DISPLAYSURF)
       #update the display
       pygame.display.update()
       #fpsClock.tick(50)
       
def declareAttacks(DISPLAYSURF, map, map_X_offset, map_Y_offset):
   declaring = True

   while declaring:
       #get all the user events
       for event in pygame.event.get():
           #if the user wants to quit
           handleGeneral(event, map, map_X_offset, map_Y_offset)
                  
       printMap(map, DISPLAYSURF)
       
       #update the display
       pygame.display.update()
       #fpsClock.tick(50)
       
def resolveBattles(DISPLAYSURF, map, map_X_offset, map_Y_offset):
   resolving = True

   while resolving:
       #get all the user events
       for event in pygame.event.get():
           #if the user wants to quit
           handleGeneral(event, map, map_X_offset, map_Y_offset)
                  
       printMap(map, DISPLAYSURF)
       
       #update the display
       pygame.display.update()
       #fpsClock.tick(50)
       
def moveTroops(DISPLAYSURF, map, map_X_offset, map_Y_offset):
   moving = True

   while moving:
       #get all the user events
       for event in pygame.event.get():
           #if the user wants to quit
           handleGeneral(event, map, map_X_offset, map_Y_offset)
                  
       printMap(map, DISPLAYSURF)
       
       #update the display
       pygame.display.update()
       #fpsClock.tick(50)
       
         
def play(host_address, player_name):
   map_X_offset = 0
   map_Y_offset = 0
   #set up the display
   print("Enter play")
   DISPLAYSURF = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

   #initialize the movie
   pygame.mixer.quit()
   movie = pygame.movie.Movie('These Guys XD_mpeg1video.mpg')

   #use list comprehension to create our tilemap
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   print("About to connect to host")
   # connection to hostname on the port.
   s.connect(host_address)                               
   print("Connected to host")
   s.sendto(player_name.encode("ascii"), host_address)
   # Receive no more than 1024 bytes
   pickledResponse = s.recv(8192)
   map, player = pickle.loads(pickledResponse)
   print("Got the map")
   
   s.sendto(player_name.encode("ascii"), host_address)

   # Map continent names to tiles
   incrementor = 0
   for continent in map.l_continent_names:
      incrementor += 1
      d_continent_tiles[continent] = incrementor
   
   # Populate texture map index dictionary based on player names
   temp_index = 0
   for name in map.l_player_names:
      temp_index += 1
      d_playerLogoIndexes[name] = temp_index
   
   map.current_player = player_name
   print(player_name)
   
   while True:
      placeUnits(DISPLAYSURF, map, map_X_offset, map_Y_offset, player)

   s.close()