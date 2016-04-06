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
play = None
newServer = None
joined = True
IMAGE_FILE_PATH = "ImageFiles\\"
BOOT_MESSAGE = pygame.image.load(IMAGE_FILE_PATH + "InfoBooted.png").convert_alpha()
CRASH_MESSAGE = pygame.image.load(IMAGE_FILE_PATH + "InfoServerLost.png").convert_alpha()
DOWN_ARROW =  pygame.image.load(IMAGE_FILE_PATH + "upArrow.png").convert_alpha()
UP_ARROW =  pygame.image.load(IMAGE_FILE_PATH + "downArrow.png").convert_alpha()
# Position of the arrows
arrow_x_pos = 1500
up_arrow_y_pos = 550
down_arrow_y_pos = 50
name = None

def LoginClient(username, s):
   global joined
   global play
   global name
   name = username
   play = None
   joined = True
   print("In clientJoined")
   
   def displayMessage(image):
      OK_COORDS = (650,650)
      clickedOK = False
      while not clickedOK:
         curr_x, curr_y = pygame.mouse.get_pos()
         curr_x *= xScale
         curr_y *= yScale
         over_ok = OK_COORDS[0] <= curr_x <= OK_COORDS[0] + 200 and OK_COORDS[1] <= curr_y <= OK_COORDS[1] + 100
         for event in pygame.event.get():
            if over_ok and event.type == MOUSEBUTTONDOWN:
               clickedOK = True
              
         # Blit the stuffs onto the screen
         LOGIN_TOP_SURFACE.blit(BLACK_BACKGROUND, (100, 100))
         LOGIN_TOP_SURFACE.blit(LOGIN_BACKGROUND, (0,0))
         LOGIN_TOP_SURFACE.blit(SERVER_FONT.render(name, 1, (0,0,0)), (285, Y_POS))
         LOGIN_TOP_SURFACE.blit(DOWN_ARROW, (arrow_x_pos, down_arrow_y_pos))
         LOGIN_TOP_SURFACE.blit(UP_ARROW, (arrow_x_pos, up_arrow_y_pos))
         if x_back_button <= curr_x <= x_back_button + 75 and y_back_button <= curr_y <= y_back_button + 50:
            LOGIN_TOP_SURFACE.blit(BACK_BUTTON_PRESSED, (x_back_button,y_back_button))
         else:
            LOGIN_TOP_SURFACE.blit(BACK_BUTTON_UNPRESSED, (x_back_button,y_back_button))
         LOGIN_TOP_SURFACE.blit(image, (280, 0))
         LOGIN_TOP_SURFACE.blit(OK_LIT if over_ok else OK_UNLIT, OK_COORDS)
         newSurface = pygame.transform.scale(LOGIN_TOP_SURFACE,(screenInfo.current_w, screenInfo.current_h), window)
         pygame.display.update()
            
   def displayPlayers(x_panel_position, y_panel_position, y_offset):
      tempPlayers = copy.copy(l_players)
      for player in tempPlayers:
         LOGIN_TOP_SURFACE.blit(SERVER_BAR, (x_panel_position, y_panel_position + y_offset))
        
         # display the name of the player
         LOGIN_TOP_SURFACE.blit(SERVER_FONT.render(player, True, (0,0,0)), (x_panel_position + 50, y_panel_position + 25 + y_offset))
         y_panel_position += 100
   
   def getPlayers():
      global name
      global l_players
      global play
      global newServer
      while True:
         try:
            packet = s.recv(8192)
            info = pickle.loads(packet)
            print("length of info: " + str(len(info)))
            
            if info[0]:
               newServer = (info[1])
               s.close()
               play = "play"
               return
            else:
               if info[2] == "boot" or info[2] == "full":
                  s.close()
                  #print("Got booted")
                  play = info[2]
                  print("info is: " + str(info[2]))
                  return
               else:
                  if len(l_players) > 0:
                     del l_players[:]
                  l_players = copy.copy(info[1])
                  l_players.insert(0, info[2])
                  if len(info) == 4:
                     name = info[3]
                     
         except:
            print("Server died")
            play = "crashed"
            return
      
   
   # Initialize pygame
   pygame.init()

   
   # Graphics Constants
   IMAGE_FILE_PATH = "ImageFiles\\"
   OK_UNLIT = pygame.image.load(IMAGE_FILE_PATH + "OK.png")
   OK_LIT = pygame.image.load(IMAGE_FILE_PATH + "OKLit.png")
   LOGIN_BACKGROUND = pygame.image.load(IMAGE_FILE_PATH + "waiting_background.png").convert_alpha()
   BLACK_BACKGROUND = pygame.image.load(IMAGE_FILE_PATH + "client_login_background2.png").convert_alpha()
   SERVER_BAR = pygame.image.load(IMAGE_FILE_PATH + "Server.png").convert_alpha()
   UP_ARROW =  pygame.image.load(IMAGE_FILE_PATH + "downArrow.png").convert_alpha()
   BACK_BUTTON_UNPRESSED = pygame.image.load(IMAGE_FILE_PATH + "back_button_unpressed.png").convert_alpha()
   BACK_BUTTON_PRESSED = pygame.image.load(IMAGE_FILE_PATH + "back_button_pressed.png").convert_alpha()

   # Declare Server Font
   SERVER_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 35)
   width, height = SERVER_FONT.size("Username:")

   # Position of the text box
   X_POS = 100
   Y_POS = 725

   # Position of back button
   x_back_button = 5
   y_back_button = 5

   # Position of refresh button
   refresh_x_pos = 1300
   refresh_y_pos = 700

   # Position of the Server Panel
   x_panel_position = 100
   y_panel_position = 100

   # Offset for scrolling
   y_offset = 0
   
   # Declare the Surface
   screenInfo = pygame.display.Info()
   LOGIN_TOP_SURFACE = pygame.Surface((1600,900))
   window = pygame.display.set_mode((screenInfo.current_w,screenInfo.current_h), pygame.FULLSCREEN)
   xScale = 1600.0 / float(screenInfo.current_w)
   yScale = 900.0 / float(screenInfo.current_h)
   
   # try:
      # temp = s.recvfrom(2048)
      # username = pickle.loads(temp)
   # except:
      # print(str(temp))

   t_search = threading.Thread(target=getPlayers)
   t_search.daemon = True
   t_search.start()
   # Get the username
   while joined:
      curr_x, curr_y = pygame.mouse.get_pos()
      curr_x *= xScale
      curr_y *= yScale
      
      #stuffs for scrolling
      players = 0
      index = 0
      y_offset_allowed = 0
      for this_guy in l_players:
         players += 1
         if players > 5:
            index += 1
            y_offset_allowed = (index * 100)
         
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
               #print("shifted is now false")
            if event.key == K_DOWN and y_offset > -y_offset_allowed and len(l_players) > 5:
               SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
               y_offset -= 25
            if event.key == K_UP and y_offset < 0 and len(l_players) > 5:
               SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
               y_offset += 25
         if event.type == MOUSEBUTTONDOWN:
            x_mouse_position_main, y_mouse_position_main = pygame.mouse.get_pos()
            x_mouse_position_main *= xScale
            y_mouse_position_main *= yScale
            
            if event.button == 1:
               # clicked back button
               if x_back_button <= curr_x <= x_back_button + 75 and y_back_button <= curr_y <= y_back_button + 50:
                  s.close()
                  #print("Clicked back button")
                  return False
                  
               # clicked up arrow
               if arrow_x_pos <= x_mouse_position_main<= arrow_x_pos + 100 and up_arrow_y_pos <= y_mouse_position_main <= up_arrow_y_pos + 75 and y_offset > -y_offset_allowed and len(l_players) > 5: # only allows me to scroll once...
                  SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
                  y_offset -= 25
                  
               # clicked down arrow
               if arrow_x_pos <= x_mouse_position_main<= arrow_x_pos + 100 and down_arrow_y_pos <= y_mouse_position_main <= down_arrow_y_pos + 75 and y_offset < 0 and len(l_players) > 5:
                  SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
                  y_offset += 25
               
            if event.button == 4 and y_offset < 0 and len(l_players) > 5:
               SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
               y_offset += 25
               
            if event.button == 5 and y_offset > -y_offset_allowed and len(l_players) > 5:
               SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
               y_offset -= 25
               
      if len(l_players) <= 5:
         y_offset = 0
                        
      # Blit the stuffs onto the screen
      LOGIN_TOP_SURFACE.blit(BLACK_BACKGROUND, (100, 100))
      displayPlayers(x_panel_position, y_panel_position, y_offset)
      LOGIN_TOP_SURFACE.blit(LOGIN_BACKGROUND, (0,0))
      LOGIN_TOP_SURFACE.blit(SERVER_FONT.render(name, 1, (0,0,0)), (285, Y_POS))
      LOGIN_TOP_SURFACE.blit(DOWN_ARROW, (arrow_x_pos, down_arrow_y_pos))
      LOGIN_TOP_SURFACE.blit(UP_ARROW, (arrow_x_pos, up_arrow_y_pos))
      if x_back_button <= curr_x <= x_back_button + 75 and y_back_button <= curr_y <= y_back_button + 50:
         LOGIN_TOP_SURFACE.blit(BACK_BUTTON_PRESSED, (x_back_button,y_back_button))
      else:
         LOGIN_TOP_SURFACE.blit(BACK_BUTTON_UNPRESSED, (x_back_button,y_back_button))
      
      if play == "play":
         #print("play")
         SimpleClient.play(newServer, name)
         return False
      elif play == "boot":
         print("boot")
         displayMessage(BOOT_MESSAGE)
         joined = False
      elif play == "full":
         return True
      elif play == "crashed":
         print("crashed")
         displayMessage(CRASH_MESSAGE)
         joined = False
      else:
         newSurface = pygame.transform.scale(LOGIN_TOP_SURFACE,(screenInfo.current_w, screenInfo.current_h), window)
         pygame.display.update()
   #print("Leaving clientJoined")   
   return False