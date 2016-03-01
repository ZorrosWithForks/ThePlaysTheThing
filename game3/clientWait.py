import socket
import threading
from threading import Thread
import _thread
import time
import SimpleClient
import pickle
import string
import pygame, sys
from pygame.locals import *
import random
import re
from bad_stuff import *
#import main_menu

def clientWait(s, username):
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
         # pygame.draw.rect(LOGIN_TOP_SURFACE, ac,(x,y,w,h))
         LOGIN_TOP_SURFACE.blit(button_pressed, (x, y))
         if click[0] == 1 and msg == "Quit":
            #LOGIN_TOP_SURFACE.blit(REFRESH_BUTTON_PRESSED, (1300, 700))
            return(True)
         if click[0] == 1 and msg == "Back":
            return(True)
      else:
         # pygame.draw.rect(LOGIN_TOP_SURFACE, ic,(x,y,w,h))
         LOGIN_TOP_SURFACE.blit(button_unpressed, (x, y))
         
      smallText = pygame.font.Font("OldNewspaperTypes.ttf",20)
      textSurf, textRect = text_objects(msg, smallText, l_colors[WHITE])
      textRect.center = ( (x+(w/2)), (y+(h/2)) )
      #LOGIN_TOP_SURFACE.blit(textSurf, textRect)



   def text_objects(text, font, color):
       textSurface = font.render(text, True, color)
       return textSurface, textSurface.get_rect()

   # Program function
      
   def display_players(x_panel_position, y_panel_position):
      print("Number of clients: " + str(len(clients)))
      for i in clients:
         DISPLAYSURF.blit(SERVER_BAR, (x_panel_position, y_panel_position))
         # display the name of the client
         DISPLAYSURF.blit(SERVER_FONT.render(str(i[1]), True, (0,0,0)), (x_panel_position + 25, y_panel_position + 25))
         DISPLAYSURF.blit(BOOT_BUTTON, (x_panel_position + 1200, y_panel_position + 25))
         l_boot_spots.append((x_panel_position, y_panel_position + 25, i[1]))
         y_panel_position += 100
         
   def search(x_panel_position, y_panel_position, y_offset):
      while True:
         packet, addr = client_socket.recvfrom(4096)
         if packet != None:
            try:
               server_info = pickle.loads(packet)
               l_servers.append(server_info)
               print("added a server: " + server_info[0])
               print("server length is: " + str(l_servers))
               #display_servers(x_panel_position, y_panel_position, y_offset)
            except:
               #This is happening. why?
               print("Client tried connecting to itself")
         else:
            print("No recv_data")
         print("done displaying servers")
         
   def request(x_panel_position, y_panel_position, y_offset):
      print("looping requesting servers")
      del l_servers[:]
      y_offset = 0
      print("servers after deleting: ", str(l_servers))
      client_socket.sendto(data.encode('ascii'), address)

   def beginGame(s):
      new_server = (s[0].recv(1024).decode(), 9998)
      s[0].close()
      SimpleClient.play(new_server, s[1])

   #def Loginclient():
   # Initialize pygame
   pygame.init()

   # Graphics Constants
   IMAGE_FILE_PATH = "ImageFiles\\"
   LOGIN_BACKGROUND = pygame.image.load(IMAGE_FILE_PATH + "client_login_background.png")
   BLACK_BACKGROUND = pygame.image.load(IMAGE_FILE_PATH + "client_login_background2.png")
   SERVER_BAR = pygame.image.load(IMAGE_FILE_PATH + "Server.png")
   JOIN_BUTTON_PRESSED = pygame.image.load(IMAGE_FILE_PATH + "JoinButton_pressed.png")
   JOIN_BUTTON_UNPRESSED = pygame.image.load(IMAGE_FILE_PATH + "JoinButton_unpressed.png")
   REFRESH_BUTTON_UNPRESSED = pygame.image.load(IMAGE_FILE_PATH + "RefreshButton_unpressed.png")
   REFRESH_BUTTON_PRESSED = pygame.image.load(IMAGE_FILE_PATH + "RefreshButton_pressed.png")
   UP_ARROW =  pygame.image.load(IMAGE_FILE_PATH + "upArrow.png")
   DOWN_ARROW =  pygame.image.load(IMAGE_FILE_PATH + "downArrow.png")
   BACK_BUTTON_UNPRESSED = pygame.image.load(IMAGE_FILE_PATH + "back_button_unpressed.png")
   BACK_BUTTON_PRESSED = pygame.image.load(IMAGE_FILE_PATH + "back_button_pressed.png")
   #specify that shift is not pressed
   shifted = False

   # Declare list of join button spots
   l_join_spots = []

   # Declare Server Font
   SERVER_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 35)
   width, height = SERVER_FONT.size("Username:")
   print("width of A is: " + str(width))
   print("height of A is: " + str(height))

   BLACK = 1
   WHITE = 2
   RED = 3
   GREEN = 4
   BLUE = 5
   BABY_BLUE = 6
   BRIGHT_RED = 7
   BRIGHT_GREEN = 8

   # Position of the text box
   x_pos = 100
   y_pos = 725

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

   GRAY = (55,55,55)

   BLOCK_COLOR = (53,115,255)

   # Position of back button
   x_back_button = 5
   y_back_button = 5

   # Position of the arrows
   arrow_x_pos = 1500
   up_arrow_y_pos = 550
   down_arrow_y_pos = 50

   # Position of refresh button
   refresh_x_pos = 1500
   refresh_y_pos = 700

   # Position of the Server Panel
   x_panel_position = 100
   y_panel_position = 100

   # Offset for scrolling
   y_offset = 0
   
   pushed_back=False
   
   # Declare the Surface
   LOGIN_TOP_SURFACE = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

   waiting_for_response = SERVER_FONT.render("Waiting for Server response...", 1, (255,0,0))
   
   #socket_exists = False
   '''
   # Client network stuff
   l_servers = []
   address = ('255.255.255.255', 8080)
   data = "Request"
   temp = socket.gethostbyname_ex(socket.gethostname())[-1]
   host = temp[-1]
   # Main starts here
   if socket_exists == False:
      client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
      client_socket.bind((host, 8080))
      client_socket.sendto(data.encode('ascii'), address)
   '''
   
   t_connect = threading.Thread(target=beginGame, args=(s,username))
   t_connect.daemon = True
   t_connect.start()

   # Get the username
   while True:
      mouse = pygame.mouse.get_pos()
      LOGIN_TOP_SURFACE.blit(waiting_for_response, (200, 800))
      
      #get user events
      events = pygame.event.get()
      for event in events:
         if event.type == QUIT:
            #end game
            t_connect.close()
            pygame.quit()
            sys.exit()
         if event.type == KEYUP:
            if event.key == K_LSHIFT or event.key == K_RSHIFT:
               shifted = False
               print("shifted is now false")
         if event.type == KEYDOWN:
            just_accessed = False
            if event.key == K_ESCAPE:
               #and the game and close the window
               pygame.quit()
               sys.exit()
            if event.key == K_UP:
               SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
               #if (len(l_servers) > 5):
               LOGIN_TOP_SURFACE.blit(BLACK_BACKGROUND, (100, 100))
               y_offset -= 100
               #display_servers(x_panel_position, y_panel_position, y_offset)
            if event.key == K_DOWN:
               SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
               if (SERVERS_AREA.x <= 100 and SERVERS_AREA.y <= 100):#put in server checking too need to find out how to get the position of a surface.
                  print("Servers area x is: " + str(SERVERS_AREA.x))
                  print("Servers area y is: " + str(SERVERS_AREA.y))
                  LOGIN_TOP_SURFACE.blit(BLACK_BACKGROUND, (100, 100))
                  y_offset += 100
                  #display_servers(x_panel_position, y_panel_position, y_offset)

         if event.type == MOUSEBUTTONDOWN:
            x_mouse_position_main, y_mouse_position_main = pygame.mouse.get_pos()
            print(str(x_mouse_position_main) + str(y_mouse_position_main))
            print("clicked mounce here")
            
            #click refresh
            if refresh_x_pos <= x_mouse_position_main <= refresh_x_pos + 200 and refresh_y_pos <= y_mouse_position_main <= refresh_y_pos + 100:
               # print("clicked refresh")
               # request(x_panel_position, y_panel_position, y_offset)
               t_connect._stop()
               s.close()
               return(True)
      # Blit the stuffs onto the screen
      #display_servers(x_panel_position, y_panel_position, y_offset)
      LOGIN_TOP_SURFACE.blit(LOGIN_BACKGROUND, (0,0))
      LOGIN_TOP_SURFACE.blit(DOWN_ARROW, (arrow_x_pos, down_arrow_y_pos))
      LOGIN_TOP_SURFACE.blit(UP_ARROW, (arrow_x_pos, up_arrow_y_pos))
      waiting_on_players = SERVER_FONT.render("Waiting on players:", 1, (0,255,255))
      LOGIN_TOP_SURFACE.blit(waiting_for_response, (200, 800))
      pushed_back = button("Quit",refresh_x_pos,refresh_y_pos,200,100,REFRESH_BUTTON_PRESSED,REFRESH_BUTTON_UNPRESSED)
      pushed_back = button("Back",x_back_button,y_back_button,75,50,BACK_BUTTON_PRESSED,BACK_BUTTON_UNPRESSED)
            
      
                     
            #click back button
            # if x_back_button <= x_mouse_position_main <= x_back_button + 75 and y_back_button <= y_mouse_position_main <= y_back_button + 50:
               # client_socket.close()
               # return
                     
            # #click up arrow
            # if arrow_x_pos <= x_mouse_position_main <= arrow_x_pos + 100 and up_arrow_y_pos <= y_mouse_position_main <= up_arrow_y_pos + 50:
               # SERVERS_SURFACE.scroll(0, -100)
            # #click down arrow
            # if arrow_x_pos <= x_mouse_position_main <= arrow_x_pos + 100 and down_arrow_y_pos <= y_mouse_position_main <= down_arrow_y_pos + 50:
               # SERVERS_SURFACE.scroll(0, 100)
               
      pygame.display.update()
      
if __name__ == '__main__':
   clientWait()