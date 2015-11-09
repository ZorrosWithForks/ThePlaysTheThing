#client.py
import socket
import os
import threading
from threading import Thread
import _thread
import pygame, sys, random
from pygame.locals import *
import pickle

fpsClock = pygame.time.Clock()

#constants representing colours
BLACK = (0,   0,   0  )
BROWN = (153, 76,  0  )
GREEN = (0,   255, 0  )
BLUE  = (0,   0,   255)
WHITE = (255, 255, 255)

#constants representing the different resources
DIRT  = 0
GRASS = 1
WATER = 2
COAL  = 3
DIAMOND = 4
LAVA = 5
SKY = 6
CLOUD = 7
PLANE = 8
WOOD = 9
LEAVES = 10

#a dictionary linking resources to textures
textures =   {
                DIRT   : pygame.image.load('dirt.png'),
                GRASS  : pygame.image.load('grass.png'),
                WATER  : pygame.image.load('water.png'),
                COAL   : pygame.image.load('coal.png'),
                DIAMOND : pygame.image.load('diamond.png'),
                LAVA : pygame.image.load('lava.png'),
                SKY : pygame.image.load('sky.png'),
                CLOUD : pygame.image.load('cloud.png'),
                PLANE : pygame.image.load('plane.png'),
                WOOD : pygame.image.load('wood.png'),
                LEAVES : pygame.image.load('leaves.png')
            }

inventory =   {
                DIRT    : 0,
                GRASS   : 0,
                WATER   : 0,
                COAL    : 0,
                DIAMOND : 0,
                LAVA    : 0,
                SKY     : 0
            }
            
#useful game dimensions
TILESIZE  = 20
MAPWIDTH  = 30
MAPHEIGHT = 20
BOTTOM_HALF_START = 15

#add a font for our inventory
#INVFONT = pygame.font.Font('comic.ttf', 18)
SEED_SPACE_ROW = MAPHEIGHT - 13
SEED_SPACE_COL = MAPWIDTH - 8
TOP_HALF = MAPHEIGHT - 5

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

#a list of resources
resources = [DIRT,GRASS,WATER,COAL,DIAMOND,LAVA]
#use list comprehension to create our tilemap
tilemap = [ [DIRT for w in range(MAPWIDTH)] for h in range(MAPHEIGHT) ]

#set up the display
pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE + 50))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()                           
print("test1")
port = 9999

# connection to hostname on the port.
s.connect((host, port))                               
print("test2")
# Receive no more than 1024 bytes
buf = 4096
#data, addr = s.recvfrom(buf)
#tilemap = pickle.loads(data)
pickledResponse = s.recv(4096)
tilemap = pickle.loads(pickledResponse)

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
        
        if event.type == pygame.MOUSEBUTTONDOWN or True:
            x, y = pygame.mouse.get_pos()
            print("x is " + str(x))
            print("y is " + str(y))
            x = int(x / TILESIZE)
            y = int(y / TILESIZE)
            print("x is " + str(x))
            print("y is " + str(y))
            tilemap[y][x] =  GRASS

        #if a key is pressed
        if event.type == KEYDOWN:
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
            if event.key == K_SPACE:
                #what resource is the player standing on?
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                #player now has 1 more of this resource
                inventory[currentTile] += 1

            #placing dirt
            if (event.key == K_1):
                #get the tile to swap with the dirt
                currentTile = tilemap[playerPos[1]][playerPos[0]]
                #if we have dirt in our inventory
                if inventory[DIRT] > 0:
                    #remove one dirt and place it
                    inventory[DIRT] -= 1
                    tilemap[playerPos[1]][playerPos[0]] = DIRT
                    #swap the item that was there before
                    inventory[currentTile] += 1

    #loop through each row
    for row in range(MAPHEIGHT):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilemap, using the correct colour
            DISPLAYSURF.blit(textures[tilemap[row][column]], (column * TILESIZE, row * TILESIZE))
            
    #display the player at the correct position 
    DISPLAYSURF.blit(PLAYER,(playerPos[0]*TILESIZE,playerPos[1]*TILESIZE))
    
    #display the cloud
    DISPLAYSURF.blit(textures[CLOUD].convert_alpha(),(cloud_x, cloud_y))
    #move the cloud to the left
    cloud_x+=1
    #if the cloud has moved passed the map
    if cloud_x + 50 > MAPWIDTH*TILESIZE:
        #pick a new position
        cloud_y = random.randint(0, MAPHEIGHT*TILESIZE)
        cloud_x = -200
        
    #display the plane
    DISPLAYSURF.blit(textures[PLANE].convert_alpha(),(plane_x, plane_y))
    #move the plane to the right
    plane_x-=1
    #if cloud has moved passed map on left
    if plane_x < 0:
        plane_y = random.randint(0, MAPHEIGHT*TILESIZE)
        plane_x = MAPWIDTH*TILESIZE
    
    #display the inventory, starting 10 pixels in
    placePosition = 10
    for item in resources:
        #add the image
        DISPLAYSURF.blit(textures[item],(placePosition,MAPHEIGHT*TILESIZE+20))
        placePosition += 30
        #add the text showing the amount in the inventory
        textObj = INVFONT.render(str(inventory[item]), True, WHITE, BLACK)
        DISPLAYSURF.blit(textObj,(placePosition,MAPHEIGHT*TILESIZE+20)) 
        placePosition += 50
    

    #update the display
    pygame.display.update()
    fpsClock.tick(10)


s.close()