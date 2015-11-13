#client.py
import socket
import os
import threading
from threading import Thread
import _thread
import pygame, sys, random
from pygame.locals import *
import pickle
from Maps import *

fpsClock = pygame.time.Clock()

#constants representing colours
BLACK = (0,   0,   0  )
BROWN = (153, 76,  0  )
GREEN = (0,   255, 0  )
BLUE  = (0,   0,   255)
WHITE = (255, 255, 255)

#constants representing the different resources

CONTINENT_1 = 1
CONTINENT_2 = 2
CONTINENT_3 = 3
CONTINENT_4 = 4
CONTINENT_5 = 5
CONTINENT_6 = 6
CONTINENT_7 = 7
CONTINENT_8 = 8
GRASS = 12
WATER = (0,0)
DEEP_WATER = 10
OVERLAY = 9

#a dictionary linking resources to textures
textures =   {
                GRASS  : pygame.image.load('grass.png'),
                WATER  : pygame.image.load('water.png'),
                DEEP_WATER : pygame.image.load ('deep_water.png'),
                OVERLAY : pygame.image.load('overlay.png'),
                CONTINENT_1 : pygame.image.load('continent_1.png'),
                CONTINENT_2 : pygame.image.load('continent_2.png'),
                CONTINENT_3 : pygame.image.load('continent_3.png'),
                CONTINENT_4 : pygame.image.load('continent_4.png'),
                CONTINENT_5 : pygame.image.load('continent_5.png'),
                CONTINENT_6 : pygame.image.load('continent_6.png'),
                CONTINENT_7 : pygame.image.load('continent_7.png'),
                CONTINENT_8 : pygame.image.load('continent_8.png')
            }


#useful game dimensions
MARGIN = 50
TILESIZE  = 100
MAPWIDTH  = 11
MAPHEIGHT = 8
BOTTOM_HALF_START = 15

#set up the display
pygame.init()
DISPLAYSURF = pygame.display.set_mode((0,0), pygame.FULLSCREEN)


#cloud position
cloud_x = -200
cloud_y = 0

#plane position
plane_x = MAPWIDTH*TILESIZE
plane_y = 50

#the player image
PLAYER = pygame.image.load('player2.png')
#the position of the player [x,y]
playerPos = [0,0]

#use list comprehension to create our tilemap
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()                           
print("test1")
port = 9999

# connection to hostname on the port.
s.connect((host, port))                               
print("test2")
# Receive no more than 1024 bytes
pickledResponse = s.recv(4096)
map = pickle.loads(pickledResponse)

#main()
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
            if event.key == K_ESCAPE:
                #and the game and close the window
                pygame.quit()
                sys.exit()
            #if the right arrow is pressed
            if event.key == K_RIGHT and playerPos[0] < MAPWIDTH - 1:
                #change the player's x position
                playerPos[0] += 1
            if event.key == K_LEFT and playerPos[0] > 0:
                #change the player's x position
                playerPos[0] -= 1
            if event.key == K_UP and playerPos[1] > 0:
                #change the player's x position
                playerPos[1] -= 1
            if event.key == K_DOWN and playerPos[1] < MAPHEIGHT -1:
                #change the player's x position
                playerPos[1] += 1

    #loop through each row
    for row in range(MAPHEIGHT):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilemap, using the correct colour
            if (map.ll_map[row][column] != WATER):
               DISPLAYSURF.blit(textures[GRASS], (column * TILESIZE, row * TILESIZE))

       
    #loop through each row
    for row in range(MAPHEIGHT):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilemap, using the correct colour
            if (map.ll_map[row][column] == WATER):
               DISPLAYSURF.blit(textures[WATER], (column * TILESIZE - MARGIN, row * TILESIZE - MARGIN))
          
#loop through each row
    for row in range(MAPHEIGHT):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilemap, using the correct colour
            if (map.ll_map[row][column] == WATER):
               DISPLAYSURF.blit(textures[DEEP_WATER], (column * TILESIZE - MARGIN, row * TILESIZE - MARGIN))

    DISPLAYSURF.blit(source=textures[OVERLAY], dest=(0,0), special_flags=BLEND_MULT)
            
    #display the player at the correct position 
    DISPLAYSURF.blit(PLAYER,(playerPos[0]*TILESIZE,playerPos[1]*TILESIZE))

    #update the display
    pygame.display.update()
    fpsClock.tick(10)


s.close()