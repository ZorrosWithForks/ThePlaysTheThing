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

# Graphics Constants
INFO_MARQUEE = pygame.image.load(IMAGE_FILE_PATH + "InfoMarque.png")
INFO_OVERLAY = pygame.image.load(IMAGE_FILE_PATH + "InfoMarqueOverlay.png")
MAP_FRAME = pygame.image.load(IMAGE_FILE_PATH + "MapFrame.png")
MAP_LIGHT = pygame.image.load(IMAGE_FILE_PATH + "MapLighting.png")

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
   
def printMap(map, DISPLAYSURF):
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
                  DISPLAYSURF.blit(UNIT_FONT.render(str(current_country.unit_counts.getSummaryCount()), True, (0,0,0)), (((column) % map.WIDTH) * TILESIZE + 40, ((row) % map.HEIGHT) * TILESIZE + 25))

    DISPLAYSURF.blit(source=INFO_MARQUEE, dest=(map.WIDTH * TILESIZE, 0))
    DISPLAYSURF.blit(source=pygame.image.load(IMAGE_FILE_PATH + "BaseBoard.png"), dest=(0, map.HEIGHT * TILESIZE))
    
    #Highlight country mouse is over and display country info
    curr_x, curr_y = pygame.mouse.get_pos()
    if (curr_x < map.WIDTH * TILESIZE and curr_y < map.HEIGHT * TILESIZE and map.ll_map[int(curr_y / TILESIZE)][int(curr_x / TILESIZE)] != map.WATER):
      DISPLAYSURF.blit(pygame.image.load(IMAGE_FILE_PATH + 'MouseOver.png'), (int(curr_x / TILESIZE) * TILESIZE - MARGIN, int(curr_y / TILESIZE) * TILESIZE - MARGIN), special_flags=BLEND_ADD)
      current_tile = map.ll_map[int(curr_y / TILESIZE)][int(curr_x / TILESIZE)]
      DISPLAYSURF.blit(CONTINENT_FONT.render("Continent: " + current_tile[0], True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 120))
      DISPLAYSURF.blit(COUNTRY_FONT.render("Country: " + map.d_continents[current_tile[0]][current_tile[1]].name, True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 170))
      
      if map.d_continents[current_tile[0]][current_tile[1]].owner != None: 
         # Unit counts by type
         DISPLAYSURF.blit(COUNTRY_FONT.render("Infantry: "  + str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.infantry), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 225))
         DISPLAYSURF.blit(COUNTRY_FONT.render("Archers: "   + str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.archers), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 250))
         DISPLAYSURF.blit(COUNTRY_FONT.render("Cannons: "   + str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.cannons), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 275))
         DISPLAYSURF.blit(COUNTRY_FONT.render("Champions: " + str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.champions), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 300))
         
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

    DISPLAYSURF.blit(source=INFO_OVERLAY, dest=(map.WIDTH * TILESIZE, 0), special_flags=BLEND_RGBA_ADD)

    #update the display
    pygame.display.update()

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
   map = pickle.loads(pickledResponse)
   print("Got the map")
   
   s.sendto(player_name.encode("ascii"), host_address)

   # Map continent names to tiles
   incrementor = 0
   for continent in map.l_continent_names:
      incrementor += 1
      d_continent_tiles[continent] = incrementor
   
   # Populate texture map index dictionary based on player names
   temp_index = 0
   for player_name in map.l_player_names:
      temp_index += 1
      d_playerLogoIndexes[player_name] = temp_index
   
   while True:
       #get all the user events
       for event in pygame.event.get():
           #if the user wants to quit
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
                  map_X_offset = (map_X_offset + 1) % map.WIDTH
                  moveMap(-1, 0, map)
               if event.key == K_LEFT:
                  #Change the map render offset
                  map_X_offset = (map_X_offset - 1) % map.WIDTH
                  moveMap(1, 0, map)
               if event.key == K_UP:
                  #Change the map render offset
                  map_Y_offset = (map_Y_offset - 1) % map.HEIGHT
                  moveMap(0, 1, map)
               if event.key == K_DOWN:
                  #Change the map render offset
                  map_Y_offset = (map_Y_offset + 1) % map.HEIGHT
                  moveMap(0, -1, map)
               
               if event.key == K_m:
                  #play the movie
                  #screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                  info = pygame.display.Info()
                  movie_screen = pygame.Surface(movie.get_size())
                  movie_screen.blit(textures[WATER], (200,200))
                  movie.set_display(movie_screen)
                  time_started = time.time()
                  int(time_started)
                  movie.set_volume(.99)
                  movie.play()
                  playing = True
                  while playing:
                     if event.type == KEYDOWN:
                         if event.key == K_p:
                            movie.pause()
                         if event.key == K_s:
                            movie.stop()
                            playing = False
                     current_time = time.time()
                     int(current_time)
                     print("current time is: ", str(current_time))
                     DISPLAYSURF.blit(movie_screen,(map.WIDTH * TILESIZE + 100, 120))
                     pygame.display.update()
                     if current_time - time_started >= int(movie.get_length()):
                        playing = False
                        movie.rewind()
                        pygame.event.clear()
                        print("HERE?")
                  print ("made it here")
       printMap(map, DISPLAYSURF)
       
       #update the display
       pygame.display.update()
       fpsClock.tick(10)

   s.close()