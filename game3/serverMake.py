import socket
import threading
from threading import Thread
import _thread
import pickle
import time
import select
import SimpleServer
import clientLogin
import SimpleClient
import pygame, sys
from pygame.locals import *
import random
import re
import os
from bad_stuff import *
import copy

def MakeServer():
   def text_objects(text, font, color):
       textSurface = font.render(text, True, color)
       return textSurface, textSurface.get_rect()
           
   def broadcast(servername, server_socket):
      while True:
         print("Listening")
         recv_data, addr = server_socket.recvfrom(4096)
         
         print(recv_data)
         packet = pickle.dumps((host, servername)) 
         server_socket.sendto(packet, addr)

   def acceptPlayers():
      print("made it to accept players")
      serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      port = 9999
      addr = (host, port)
      serversocket.bind((host, port))
      serversocket.listen(5)
      while True: # this causes my join spots to go high
         client, client_address = serversocket.accept()
         player_name = client.recv(4096).decode()
         thread.append(Thread(target=listener, args = (client, client_address, clients, serversocket, player_name)).start())
         display_players(x_panel_position, y_panel_position, player_name)

   def listener(client, client_address, clients, serversocket, player_name):
      print("Accepted connection from: ", client_address)
      with clients_lock:
         l_temp = (client, player_name, client_address)
         clients.add(l_temp)#Array of clients
      try:
         while True:
            ready_to_read, ready_to_write, in_error = \
               select.select([serversocket,], [serversocket,], [], 5)
               
      except select.error:
         print("connection error")
               
      finally:
         with clients_lock:
            clients.remove(client)
            client.close()
            
   def display_players(x_panel_position, y_panel_position, player_name):
      #print("Number of clients: " + str(len(clients)))
      del l_boot_spots[:]
      for i in clients:
         #length of clients is 1, but boot spots countinually grows....
         DISPLAYSURF.blit(SERVER_BAR, (x_panel_position, y_panel_position))
         print("blitted bar")
         l_boot_spots.append((x_panel_position + 1200, y_panel_position + 25, str(i[1])))
         # display the name of the client
         DISPLAYSURF.blit(SERVER_FONT.render(str(i[1]), True, (0,0,0)), (x_panel_position + 25, y_panel_position + 25))
         DISPLAYSURF.blit(BOOT_BUTTON, (x_panel_position + 1200, y_panel_position + 25))
         y_panel_position += 100
         
   def start_game():
      for client in clients:
         client[0].sendto(host.encode("ascii"), client[2])
      addr = (host, 9998)
      t_become_server = threading.Thread(target=SimpleServer.serve, args=(len(clients) + 1,))
      t_become_server.daemon = True
      t_become_server.start()
      server_socket.close()
      SimpleClient.play(addr, servername)

   def begin_serving(servername, server_socket, x_panel_position, y_panel_position, clients):
      print("this prints")
      t_broadcast = threading.Thread(target=broadcast, args=(servername, server_socket))
      t_broadcast.daemon = True
      t_broadcast.start()
      print("this prints too")
      print("host is: " + str(host))
      t_accept_players = threading.Thread(target=acceptPlayers, args=())
      t_accept_players.daemon = True
      t_accept_players.start()

   def button(msg,x,y,w,h,button_pressed,button_unpressed):
      ''' x: The x location of the top left coordinate of the button box.

          y: The y location of the top left coordinate of the button box.

          w: Button width.

          h: Button height.

          ic: Inactive color (when a mouse is not hovering).

          ac: Active color (when a mouse is hovering).
      '''
      mouse = pygame.mouse.get_pos()
      click = pygame.mouse.get_pressed()
      
      if x+w > mouse[0] > x and y+h > mouse[1] > y:
         DISPLAYSURF.blit(button_pressed, (x, y))
      else:
         DISPLAYSURF.blit(button_unpressed, (x, y))
         
      smallText = pygame.font.Font("freesansbold.ttf",20)
      textSurf, textRect = text_objects(msg, smallText, l_colors[WHITE])
      textRect.center = ( (x+(w/2)), (y+(h/2)) )
      
   # Initialize pygame
   pygame.init()

   # Initilize bad word list
   filter = ProfanitiesFilter(bad_things, replacements="-")
   
   # Specify that shift is not pressed
   shifted = False
   
   # Declare list of boot button spots
   l_boot_spots = []

   # Graphics Constants
   IMAGE_FILE_PATH = "ImageFiles\\"
   LOGIN_BACKGROUND = pygame.image.load(IMAGE_FILE_PATH + "server_login_background.png")
   BLACK_BACKGROUND = pygame.image.load(IMAGE_FILE_PATH + "client_login_background2.png")
   SERVER_BAR = pygame.image.load(IMAGE_FILE_PATH + "Server.png")
   JOIN_BUTTON = pygame.image.load(IMAGE_FILE_PATH + "JoinButton_unpressed.png")
   REFRESH_BUTTON = pygame.image.load(IMAGE_FILE_PATH + "RefreshButton2.png")
   PLAY_BUTTON_PRESSED = pygame.image.load(IMAGE_FILE_PATH + "playbutton_down.png")
   PLAY_BUTTON_UNPRESSED = pygame.image.load(IMAGE_FILE_PATH + "playbutton_up.png")
   BOOT_BUTTON = pygame.image.load(IMAGE_FILE_PATH+ "BootButton.png")
   SERVERNAME_BOX =  pygame.image.load(IMAGE_FILE_PATH + "username_box.png")
   START_SERVER_BUTTON_PRESSED =  pygame.image.load(IMAGE_FILE_PATH + "start_server_button_pressed.png")
   START_SERVER_BUTTON_UNPRESSED =  pygame.image.load(IMAGE_FILE_PATH + "start_server_button_unpressed.png")
   SERVER_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 35)
   BACK_BUTTON_UNPRESSED = pygame.image.load(IMAGE_FILE_PATH + "back_button_unpressed.png")
   BACK_BUTTON_PRESSED = pygame.image.load(IMAGE_FILE_PATH + "back_button_pressed.png")
   WAITING_PANEL = pygame.image.load(IMAGE_FILE_PATH + "Waiting.png")

   BLACK = 1
   WHITE = 2
   RED = 3
   GREEN = 4
   BLUE = 5
   BABY_BLUE = 6
   BRIGHT_RED = 7
   BRIGHT_GREEN = 8
   
   # Colors for buttons
   l_colors = {
               BLACK :(0,0,0),
               WHITE :(255,255,255),
               RED :(200,0,0),
               GREEN :(0,200,0),
               BLUE :(0,66,255),
               BABY_BLUE :(0,223,255),
               BRIGHT_RED :(255,0,0),
               BRIGHT_GREEN :(0,255,0),
               }

   # Initialize servername
   servername = ""
   no_servername_message = SERVER_FONT.render("Please type your servername", 1, (255,0,0))
    
   # Address
   addr = ()
    
   # Position of the text box
   x_pos = 100
   y_pos = 725

   # Waiting for players
   waiting_for_players = False
   
   # Play button positions
   x_play_button = 1300
   y_play_button = 700

   # Position of back button
   x_back_button = 5
   y_back_button = 5
   
   # Position waiting panel
   x_waiting_panel =750
   y_waiting_panel =800
   
   # No servername positions
   x_no_servername = 350
   y_no_servername = 800
   
   # Server panels positions
   x_panel_position = 100
   y_panel_position = 100

   # Start server positions
   x_start_server_button = 200
   y_start_server_button = 800
       
   # Booted string
   booted = "boot"
   # Play string
   play = "play"
   
   pushed_back = False
   just_accessed = True
   # Declare the Surface
   DISPLAYSURF = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

   thread = []
   clients = set()
   clients_lock = threading.Lock()
   temp = socket.gethostbyname_ex(socket.gethostname())[-1]
   host = temp[-1]
   broadcast_address = ('', 8080)
   server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
   server_socket.bind(broadcast_address)

   # Play the game when the play button is pressed
   while True:
      DISPLAYSURF.blit(BLACK_BACKGROUND, (100, 100))
      display_players(x_panel_position, y_panel_position, None)
      
      for event in pygame.event.get():
         if event.type == QUIT:
            #end game
            pygame.quit()
            sys.exit()
         if event.type == KEYUP:
           if event.key == K_LSHIFT or event.key == K_RSHIFT:
              shifted = False
         if event.type == KEYDOWN:
            just_accessed = False
            if event.key == K_ESCAPE:
               #end the game and close the window
               print(servername)
               print("something")
               pygame.quit()
               sys.exit()
            if event.key == K_BACKSPACE:
               servername = servername[:-1]
            elif event.key == K_LSHIFT or event.key == K_RSHIFT:
               shifted = True
            if not shifted and len(servername) < 25:
               if event.key == K_a: servername += "a"
               elif event.key == K_b: servername += "b"
               elif event.key == K_c: servername += "c"
               elif event.key == K_d: servername += "d"
               elif event.key == K_e: servername += "e"
               elif event.key == K_f: servername += "f"
               elif event.key == K_g: servername += "g"
               elif event.key == K_h: servername += "h"
               elif event.key == K_i: servername += "i"
               elif event.key == K_j: servername += "j"
               elif event.key == K_k: servername += "k"
               elif event.key == K_l: servername += "l"
               elif event.key == K_m: servername += "m"
               elif event.key == K_n: servername += "n"
               elif event.key == K_o: servername += "o"
               elif event.key == K_p: servername += "p"
               elif event.key == K_q: servername += "q"
               elif event.key == K_r: servername += "r"
               elif event.key == K_s: servername += "s"
               elif event.key == K_t: servername += "t"
               elif event.key == K_u: servername += "u"
               elif event.key == K_v: servername += "v"
               elif event.key == K_w: servername += "w"
               elif event.key == K_x: servername += "x"
               elif event.key == K_y: servername += "y"
               elif event.key == K_z: servername += "z"
               elif event.key == K_0: servername += "0"
               elif event.key == K_1: servername += "1"
               elif event.key == K_2: servername += "2"
               elif event.key == K_3: servername += "3"
               elif event.key == K_4: servername += "4"
               elif event.key == K_5: servername += "5"
               elif event.key == K_6: servername += "6"
               elif event.key == K_7: servername += "7"
               elif event.key == K_8: servername += "8"
               elif event.key == K_9: servername += "9"
               elif event.key == K_BACKQUOTE: servername += "`"
               elif event.key == K_MINUS: servername += "-"
               elif event.key == K_EQUALS: servername += "="
               elif event.key == K_LEFTBRACKET: servername += "["
               elif event.key == K_RIGHTBRACKET: servername += "]"
               elif event.key == K_BACKSLASH: servername += '\\'
               elif event.key == K_SEMICOLON: servername += ";"
               elif event.key == K_QUOTE: servername += "'"
               elif event.key == K_COMMA: servername += ","
               elif event.key == K_PERIOD: servername += "."
               elif event.key == K_SLASH: servername += "/"
               elif event.key == K_TAB: pygame.display.iconify()
            elif shifted and len(servername) < 25:
               if event.key == K_a: servername += "A"
               elif event.key == K_b: servername += "B"
               elif event.key == K_c: servername += "C"
               elif event.key == K_d: servername += "D"
               elif event.key == K_e: servername += "E"
               elif event.key == K_f: servername += "F"
               elif event.key == K_g: servername += "G"
               elif event.key == K_h: servername += "H"
               elif event.key == K_i: servername += "I"
               elif event.key == K_j: servername += "J"
               elif event.key == K_k: servername += "K"
               elif event.key == K_l: servername += "L"
               elif event.key == K_m: servername += "M"
               elif event.key == K_n: servername += "N"
               elif event.key == K_o: servername += "O"
               elif event.key == K_p: servername += "P"
               elif event.key == K_q: servername += "Q"
               elif event.key == K_r: servername += "R"
               elif event.key == K_s: servername += "S"
               elif event.key == K_t: servername += "T"
               elif event.key == K_u: servername += "U"
               elif event.key == K_v: servername += "V"
               elif event.key == K_w: servername += "W"
               elif event.key == K_x: servername += "X"
               elif event.key == K_y: servername += "Y"
               elif event.key == K_z: servername += "Z"
               elif event.key == K_0: servername += ")"
               elif event.key == K_1: servername += "!"
               elif event.key == K_2: servername += "@"
               elif event.key == K_3: servername += "#"
               elif event.key == K_4: servername += "$"
               elif event.key == K_5: servername += "%"
               elif event.key == K_6: servername += "^"
               elif event.key == K_7: servername += "&"
               elif event.key == K_8: servername += "*"
               elif event.key == K_9: servername += "("
               elif event.key == K_BACKQUOTE: servername += "~"
               elif event.key == K_MINUS: servername += "_"
               elif event.key == K_EQUALS: servername += "+"
               elif event.key == K_LEFTBRACKET: servername += "{"
               elif event.key == K_RIGHTBRACKET: servername += "}"
               elif event.key == K_BACKSLASH: servername += "|"
               elif event.key == K_SEMICOLON: servername += ":"
               elif event.key == K_QUOTE: servername += "\""
               elif event.key == K_COMMA: servername += "<"
               elif event.key == K_PERIOD: servername += ">"
               elif event.key == K_SLASH: servername += "?"
         if event.type == MOUSEBUTTONDOWN:
            print("MOUSEBUTTONDOWN")
            print(str(l_boot_spots)) # still exists
            x_mouse_position_main, y_mouse_position_main = pygame.mouse.get_pos()
            
            # clicked start server
            if x_start_server_button <= x_mouse_position_main <= x_start_server_button + 150 and y_start_server_button <= y_mouse_position_main <= y_start_server_button + 75 and servername != "":
               waiting_for_players = True
               begin_serving(servername, server_socket, x_panel_position, y_panel_position, clients)
            if servername=="":
               just_accessed = False
               
            # clicked play
            if x_play_button <= x_mouse_position_main <= x_play_button + 200 and y_play_button <= y_mouse_position_main <= y_play_button + 200:
               start_game()
               
            # clicked back
            if x_back_button <= x_mouse_position_main <= x_back_button + 75 and y_back_button <= y_mouse_position_main <= y_back_button + 50:
               server_socket.close()
               return(True)
               
            # clicked boot
            for boot_spot in l_boot_spots:
               print(str(boot_spot[0]) + ' ' +str(boot_spot[1]))
               if boot_spot[0] <= x_mouse_position_main <= boot_spot[0] + 100 and boot_spot[1] <= y_mouse_position_main <= boot_spot[1] + 50:
                  print(boot_spot[2])
                  temp_client_set = copy.copy(clients)
                  for client in temp_client_set:
                     if client[1] == boot_spot[2]: # check to see if the names match
                        client[0].sendto(booted.encode("ascii"), client[2])
                        clients.remove(client)
                        print("\ndeleted: " + boot_spot[2] + client[1])
  

         
      # Blit the stuffs onto the screen
      DISPLAYSURF.blit(LOGIN_BACKGROUND, (0,0))
      servername = filter.clean(servername)
      servername_graphics = SERVER_FONT.render(servername, 1, (0,0,0))
      #DISPLAYSURF.blit(SERVERNAME_BOX, (330, y_pos))
      #DISPLAYSURF.blit(SERVER_FONT.render("Server Name: ", 1, (0,255,0)), (x_pos, y_pos))
      DISPLAYSURF.blit(BACK_BUTTON_UNPRESSED, (x_back_button, y_back_button))
      DISPLAYSURF.blit(servername_graphics, (285, y_pos))
      #DISPLAYSURF.blit(PLAY_BUTTON, (1300, 700))
      #DISPLAYSURF.blit(START_SERVER_BUTTON, (x_start_server_button, y_start_server_button))
      button("Start",x_start_server_button,y_start_server_button,150,75,START_SERVER_BUTTON_PRESSED,START_SERVER_BUTTON_UNPRESSED)
      button("Play",x_play_button,y_play_button,200,200,PLAY_BUTTON_PRESSED,PLAY_BUTTON_UNPRESSED)
      pushed_back = button("Back",x_back_button,y_back_button,75,50,BACK_BUTTON_PRESSED,BACK_BUTTON_UNPRESSED)
      if waiting_for_players == True:
         DISPLAYSURF.blit(WAITING_PANEL, (x_waiting_panel, y_waiting_panel))
      if pushed_back == True:
         server_socket.close()
         return
      if servername == "" and just_accessed == False:
         DISPLAYSURF.blit(no_servername_message, (x_no_servername, y_no_servername))
         #print(str(x_mouse_position_main) + str(y_mouse_position_main))
        # print("clicked mounce here")
         
         # clicked play
         # if x_play_button <= x_mouse_position_main <= x_play_button + 200 and y_play_button <= y_mouse_position_main <= y_play_button + 200:
           # # print("clicked play")
            # start_game()

         # clicked start
         # if x_start_server_button <= x_mouse_position_main <= x_mouse_position_main + 150 and y_start_server_button <= y_mouse_position_main <= y_start_server_button + 75:
            # pygame.display.iconify()
            # begin_serving(servername, server_socket, x_panel_position, y_panel_position, clients)
      pygame.display.update()
      
if __name__ == '__main__':
   MakeServer()