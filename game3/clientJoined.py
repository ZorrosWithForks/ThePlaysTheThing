import pickle
import threading
from threading import Thread
import _thread
import socket
import os
import pygame, sys, random
from pygame.locals import *
from pygame import font
from Maps import *
import Player
import SimpleClient
import copy

l_players = []
play = False
newServer = None
joined = True
def LoginClient(username, s):
   global joined
   global play
   play = False
   joined = True
   def displayPlayers(x_panel_position, y_panel_position, y_offset):
      tempPlayers = copy.copy(l_players)
      for player in tempPlayers:
         LOGIN_TOP_SURFACE.blit(SERVER_BAR, (x_panel_position, y_panel_position + y_offset))
        
         # display the name of the player
         LOGIN_TOP_SURFACE.blit(SERVER_FONT.render(player, True, (0,0,0)), (x_panel_position + 50, y_panel_position + 25 + y_offset))
         y_panel_position += 100
   
   def getPlayers():
      global joined
      global l_players
      global play
      global newServer
      while True:
         try:
            packet = s.recv(4096)
            info = pickle.loads(packet)
            if info[0]:
               newServer = (info[1], 9998)
               s.close()
               play = True
            else:
               if info[2] == "boot":
                  s.close()
                  print("Got booted")
                  joined = False
                  return
               else:
                  if len(l_players) > 0:
                     del l_players[:]
                  l_players = copy.copy(info[1])
                  l_players.insert(0, info[2])
         except:
            print("Server died")
            joined = False
            return
      
   
   # Initialize pygame
   pygame.init()

   
   # Graphics Constants
   IMAGE_FILE_PATH = "ImageFiles\\"
   LOGIN_BACKGROUND = pygame.image.load(IMAGE_FILE_PATH + "waiting_background.png")
   BLACK_BACKGROUND = pygame.image.load(IMAGE_FILE_PATH + "client_login_background2.png")
   SERVER_BAR = pygame.image.load(IMAGE_FILE_PATH + "Server.png")
   UP_ARROW =  pygame.image.load(IMAGE_FILE_PATH + "upArrow.png")
   DOWN_ARROW =  pygame.image.load(IMAGE_FILE_PATH + "downArrow.png")
   BACK_BUTTON_UNPRESSED = pygame.image.load(IMAGE_FILE_PATH + "back_button_unpressed.png")
   BACK_BUTTON_PRESSED = pygame.image.load(IMAGE_FILE_PATH + "back_button_pressed.png")

   # Declare Server Font
   SERVER_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 35)
   width, height = SERVER_FONT.size("Username:")

   # Position of the text box
   X_POS = 100
   Y_POS = 725

   # Position of back button
   x_back_button = 5
   y_back_button = 5

   # Position of the arrows
   arrow_x_pos = 1500
   up_arrow_y_pos = 550
   down_arrow_y_pos = 50

   # Position of refresh button
   refresh_x_pos = 1300
   refresh_y_pos = 700

   # Position of the Server Panel
   x_panel_position = 100
   y_panel_position = 100

   # Offset for scrolling
   y_offset = 0
   
   # Declare the Surface
   LOGIN_TOP_SURFACE = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

   t_search = threading.Thread(target=getPlayers)
   t_search.daemon = True
   t_search.start()
   # Get the username
   while joined:
      curr_x, curr_y = pygame.mouse.get_pos()
      
      #stuffs for scrolling
      players = 0
      index = 0
      y_offset_allowed = 0
      for this_guy in l_players:
         players += 1
         if players > 5:
            index += 1
            y_offset_allowed = (index * 100)
            print (players)
            print (y_offset_allowed)
         
      #get user events
      events = pygame.event.get()
      for event in events:
         if event.type == QUIT:
            #end game
            pygame.quit()
            sys.exit()
         if event.type == KEYUP:
            if event.key == K_LSHIFT or event.key == K_RSHIFT:
               shifted = False
               print("shifted is now false")
         if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
               #end the game and close the window
               print(username)
               print("something")
               pygame.quit()
               sys.exit()
            if event.key == K_DOWN and y_offset > -y_offset_allowed and len(l_players) > 5:
               SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
               y_offset -= 100
            if event.key == K_UP and y_offset < 0 and len(l_players) > 5:
               SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
               y_offset += 100
         if event.type == MOUSEBUTTONDOWN:
            x_mouse_position_main, y_mouse_position_main = pygame.mouse.get_pos()
            # clicked back button
            if x_back_button <= curr_x <= x_back_button + 75 and y_back_button <= curr_y <= y_back_button + 50:
               s.close()
               return(True)
               
            # clicked up arrow
            if arrow_x_pos <= x_mouse_position_main<= arrow_x_pos + 100 and up_arrow_y_pos <= y_mouse_position_main <= up_arrow_y_pos + 50 and y_offset < 0 and len(l_players) > 5: # only allows me to scroll once...
               SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
               y_offset += 100
               display_servers(x_panel_position, y_panel_position, y_offset)
               
            # clicked down arrow
            if arrow_x_pos <= x_mouse_position_main<= arrow_x_pos + 100 and down_arrow_y_pos <= y_mouse_position_main <= down_arrow_y_pos + 50 and y_offset > -y_offset_allowed and len(l_players) > 5:
               SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
               y_offset -= 100
               display_servers(x_panel_position, y_panel_position, y_offset)
                        
      # Blit the stuffs onto the screen
      LOGIN_TOP_SURFACE.blit(BLACK_BACKGROUND, (100, 100))
      displayPlayers(x_panel_position, y_panel_position, y_offset)
      LOGIN_TOP_SURFACE.blit(LOGIN_BACKGROUND, (0,0))
      LOGIN_TOP_SURFACE.blit(SERVER_FONT.render(username, 1, (0,0,0)), (285, Y_POS))
      LOGIN_TOP_SURFACE.blit(DOWN_ARROW, (arrow_x_pos, down_arrow_y_pos))
      LOGIN_TOP_SURFACE.blit(UP_ARROW, (arrow_x_pos, up_arrow_y_pos))
      if x_back_button <= curr_x <= x_back_button + 75 and y_back_button <= curr_y <= y_back_button + 50:
         LOGIN_TOP_SURFACE.blit(BACK_BUTTON_PRESSED, (x_back_button,y_back_button))
      else:
         LOGIN_TOP_SURFACE.blit(BACK_BUTTON_UNPRESSED, (x_back_button,y_back_button))
      waiting_on_players = SERVER_FONT.render("Waiting on players:", 1, (0,255,255))
      
      if play:
         SimpleClient.play(newServer, username)
      else:
         pygame.display.update()
      
   return