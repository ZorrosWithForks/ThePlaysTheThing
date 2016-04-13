import socket
import threading
from threading import Thread
import _thread
import time
import pickle
import string
import pygame, sys
from pygame.locals import *
import random
import re
from bad_stuff import *
#import main_menu
import clientJoined

def LoginClient():
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
               print("Clicked OK")
              
         # Blit the stuffs onto the screen
         LOGIN_TOP_SURFACE.blit(BLACK_BACKGROUND, (100, 100))
         display_servers(x_panel_position, y_panel_position, y_offset)
         LOGIN_TOP_SURFACE.blit(LOGIN_BACKGROUND, (0,0))
         #LOGIN_TOP_SURFACE.blit(USERNAME_BOX, (280, Y_POS))
         #LOGIN_TOP_SURFACE.blit(SERVER_FONT.render("Username: ", 1, (0,0,0)), (X_POS, Y_POS))
         LOGIN_TOP_SURFACE.blit(SERVER_FONT.render(username, 1, (0,0,0)), (285, Y_POS))
         LOGIN_TOP_SURFACE.blit(DOWN_ARROW, (arrow_x_pos, down_arrow_y_pos))
         LOGIN_TOP_SURFACE.blit(UP_ARROW, (arrow_x_pos, up_arrow_y_pos))
         #button("Refresh",refresh_x_pos,refresh_y_pos,200,100,REFRESH_BUTTON_PRESSED,REFRESH_BUTTON_UNPRESSED)
         #pushed_back = button("Back",x_back_button,y_back_button,75,50,BACK_BUTTON_PRESSED,BACK_BUTTON_UNPRESSED)
         LOGIN_TOP_SURFACE.blit(image, (280, 0))
         LOGIN_TOP_SURFACE.blit(OK_LIT if over_ok else OK_UNLIT, OK_COORDS)
         newSurface = pygame.transform.scale(LOGIN_TOP_SURFACE,(screenInfo.current_w, screenInfo.current_h), window)
         pygame.display.update()


   def button(msg, x, y, w, h, button_pressed,button_unpressed):
      ''' x: The x location of the top left coordinate of the button box.

          y: The y location of the top left coordinate of the button box.

          w: Button width.

          h: Button height.

          ic: Inactive color (when a mouse is not hovering).

          ac: Active color (when a mouse is hovering).
      '''
      curr_x, curr_y = pygame.mouse.get_pos()
      click = pygame.mouse.get_pressed()
      curr_x *= xScale
      curr_y *= yScale
      if x+w > curr_x > x and y+h > curr_y > y:
         LOGIN_TOP_SURFACE.blit(button_pressed, (x, y))
      else:
         LOGIN_TOP_SURFACE.blit(button_unpressed, (x, y))

   def text_objects(text, font, color):
       textSurface = font.render(text, True, color)
       return textSurface, textSurface.get_rect()

   def printme():
      print ("printme")

   # Program functions
   def joinGame(ip):
      #print("attempting to join " + ip)
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      addr = (ip, 9999)
      s.settimeout(1)
      try:
         s.connect(addr)
         s.settimeout(None)
         s.sendto(username.encode('ascii'), addr)
         print("joined")
         full = clientJoined.LoginClient(username, s)
         if full:
            #print("Returned true")
            displayMessage(FULL_MESSAGE)
         #print("returned from clientJoined")
         s.close()
         del l_servers[:]
         client_socket.sendto(data.encode('ascii'), address)
      except:
         print("Failed somewhere")
         displayMessage(CRASH_MESSAGE)
         s.close()
         del l_servers[:]
         client_socket.sendto(data.encode('ascii'), address)
      
   def display_servers(x_panel_position, y_panel_position, y_offset):
      del l_join_spots[:]
      for server in l_servers:
         LOGIN_TOP_SURFACE.blit(SERVER_BAR, (x_panel_position, y_panel_position + y_offset))
        
         # display the name of the server
         LOGIN_TOP_SURFACE.blit(SERVER_FONT.render(str(server[1]), True, (0,0,0)), (x_panel_position + 50, y_panel_position + 25 + y_offset))
         LOGIN_TOP_SURFACE.blit(SERVER_FONT.render("("+str(server[2])+"/7)", True, (0,0,0)), (x_panel_position + 1100, y_panel_position + 25 + y_offset))
         LOGIN_TOP_SURFACE.blit(JOIN_BUTTON_UNPRESSED, (x_panel_position + 1200, y_panel_position + 25 + y_offset))
         l_join_spots.append((x_panel_position + 1100, y_panel_position + 25 + y_offset, server[0]))
         y_panel_position += 100
   
   def search(x_panel_position, y_panel_position, y_offset):
      while True:
         try:
            packet, addr = client_socket.recvfrom(4096)
         except OSError:
            break
         except:
            pass
         try:
            gotAServer = True
            server_info = pickle.loads(packet)
            if not server_info in l_servers:
               l_servers.append(server_info)
            display_servers(x_panel_position, y_panel_position, y_offset)
         except:
            pass
         
   def request(x_panel_position, y_panel_position, y_offset):
      #print("requesting servers")
      del l_servers[:]
      y_offset = 0
      client_socket.sendto(data.encode('ascii'), address)

   # Initialize pygame
   pygame.init()

   # Graphics Constants
   IMAGE_FILE_PATH = "ImageFiles\\"
   MESSAGE = pygame.image.load(IMAGE_FILE_PATH + "InfoVictory.png").convert_alpha()
   OK_UNLIT = pygame.image.load(IMAGE_FILE_PATH + "OK.png").convert_alpha()
   OK_LIT = pygame.image.load(IMAGE_FILE_PATH + "OKLit.png").convert_alpha()
   LOGIN_BACKGROUND = pygame.image.load(IMAGE_FILE_PATH + "client_login_background.png").convert_alpha()
   BLACK_BACKGROUND = pygame.image.load(IMAGE_FILE_PATH + "client_login_background2.png").convert_alpha()
   SERVER_BAR = pygame.image.load(IMAGE_FILE_PATH + "Server.png").convert_alpha()
   JOIN_BUTTON_PRESSED = pygame.image.load(IMAGE_FILE_PATH + "JoinButton_pressed.png").convert_alpha()
   JOIN_BUTTON_UNPRESSED = pygame.image.load(IMAGE_FILE_PATH + "JoinButton_unpressed.png").convert_alpha()
   REFRESH_BUTTON_UNPRESSED = pygame.image.load(IMAGE_FILE_PATH + "RefreshButton_unpressed.png").convert_alpha()
   REFRESH_BUTTON_PRESSED = pygame.image.load(IMAGE_FILE_PATH + "RefreshButton_pressed.png").convert_alpha()
   DOWN_ARROW =  pygame.image.load(IMAGE_FILE_PATH + "upArrow.png").convert_alpha()
   UP_ARROW =  pygame.image.load(IMAGE_FILE_PATH + "downArrow.png").convert_alpha()
   #USERNAME_BOX =  pygame.image.load(IMAGE_FILE_PATH + "username_box.png")
   BACK_BUTTON_UNPRESSED = pygame.image.load(IMAGE_FILE_PATH + "back_button_unpressed.png").convert_alpha()
   BACK_BUTTON_PRESSED = pygame.image.load(IMAGE_FILE_PATH + "back_button_pressed.png").convert_alpha()
   NO_USERNAME_MESSAGE = pygame.image.load(IMAGE_FILE_PATH + "TypeUsername.png").convert_alpha()
   MESSAGE_COORDS = (220, 620)
   CRASH_MESSAGE = pygame.image.load(IMAGE_FILE_PATH + "InfoServerLost.png").convert_alpha()
   FULL_MESSAGE = pygame.image.load(IMAGE_FILE_PATH + "InfoGameFull.png").convert_alpha()
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

   # Declare the username
   username = ""

   # Position of the text box
   X_POS = 100
   Y_POS = 725

   # Initialize bad word filter
   filter = ProfanitiesFilter(filterlist=bad_things, replacements="!")

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
   refresh_x_pos = 1300
   refresh_y_pos = 700

   # Position of the Server Panel
   x_panel_position = 100
   y_panel_position = 100

   # Offset for scrolling
   y_offset = 0
   
   pushed_back=False
   
   # Declare the Surface
   screenInfo = pygame.display.Info()
   LOGIN_TOP_SURFACE = pygame.Surface((1600,900))
   window = pygame.display.set_mode((screenInfo.current_w,screenInfo.current_h), pygame.FULLSCREEN)
   xScale = 1600.0 / float(screenInfo.current_w)
   yScale = 900.0 / float(screenInfo.current_h)
   # Client network stuff
   l_servers = []
   address = ('255.255.255.255', 8080)
   data = "Request"
   temp = socket.gethostbyname_ex(socket.gethostname())[-1]
   host = temp[-1]
   # Main starts here
   client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
   client_socket.bind((host, 8080))
   client_socket.sendto(data.encode('ascii'), address)

   t_search = threading.Thread(target=search, args=(x_panel_position, y_panel_position, y_offset))
   t_search.daemon = True
   t_search.start()

   # Get the username
   while True:
      
      #stuffs for scrolling
      servers = 0
      index = 0
      y_offset_allowed = 0
      for this_guy in l_servers:
         servers += 1
         if servers > 5:
            index += 1
            y_offset_allowed = (index * 100)
            print (servers)
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
               #print("shifted is now false")
         if event.type == KEYDOWN:
            if event.key == K_DOWN and y_offset > -y_offset_allowed and len(l_servers) > 5:
               SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
               y_offset -= 25
               #display_servers(x_panel_position, y_panel_position, y_offset)
            if event.key == K_UP and y_offset < 0 and len(l_servers) > 5:
               SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
               y_offset += 25
               #display_servers(x_panel_position, y_panel_position, y_offset)
            if event.key == K_BACKSPACE:
               username = username[:-1]
            elif event.key == K_LSHIFT or event.key == K_RSHIFT:
               shifted = True
               #print("shifted")
            if shifted == False and len(username) < 25:
               if event.key == K_a: username += "a"
               elif event.key == K_b: username += "b"
               elif event.key == K_c: username += "c"
               elif event.key == K_d: username += "d"
               elif event.key == K_e: username += "e"
               elif event.key == K_f: username += "f"
               elif event.key == K_g: username += "g"
               elif event.key == K_h: username += "h"
               elif event.key == K_i: username += "i"
               elif event.key == K_j: username += "j"
               elif event.key == K_k: username += "k"
               elif event.key == K_l: username += "l"
               elif event.key == K_m: username += "m"
               elif event.key == K_n: username += "n"
               elif event.key == K_o: username += "o"
               elif event.key == K_p: username += "p"
               elif event.key == K_q: username += "q"
               elif event.key == K_r: username += "r"
               elif event.key == K_s: username += "s"
               elif event.key == K_t: username += "t"
               elif event.key == K_u: username += "u"
               elif event.key == K_v: username += "v"
               elif event.key == K_w: username += "w"
               elif event.key == K_x: username += "x"
               elif event.key == K_y: username += "y"
               elif event.key == K_z: username += "z"
               elif event.key == K_0: username += "0"
               elif event.key == K_1: username += "1"
               elif event.key == K_2: username += "2"
               elif event.key == K_3: username += "3"
               elif event.key == K_4: username += "4"
               elif event.key == K_5: username += "5"
               elif event.key == K_6: username += "6"
               elif event.key == K_7: username += "7"
               elif event.key == K_8: username += "8"
               elif event.key == K_9: username += "9"
               elif event.key == K_BACKQUOTE: username += "`"
               elif event.key == K_MINUS: username += "-"
               elif event.key == K_EQUALS: username += "="
               elif event.key == K_LEFTBRACKET: username += "["
               elif event.key == K_RIGHTBRACKET: username += "]"
               elif event.key == K_BACKSLASH: username += '\\'
               elif event.key == K_SEMICOLON: username += ";"
               elif event.key == K_QUOTE: username += "'"
               elif event.key == K_COMMA: username += ","
               elif event.key == K_PERIOD: username += "."
               elif event.key == K_SLASH: username += "/"
               elif event.key == K_TAB: pygame.display.iconify()
            elif shifted == True and len(username) < 25:
               if event.key == K_a: username += "A"
               elif event.key == K_b: username += "B"
               elif event.key == K_c: username += "C"
               elif event.key == K_d: username += "D"
               elif event.key == K_e: username += "E"
               elif event.key == K_f: username += "F"
               elif event.key == K_g: username += "G"
               elif event.key == K_h: username += "H"
               elif event.key == K_i: username += "I"
               elif event.key == K_j: username += "J"
               elif event.key == K_k: username += "K"
               elif event.key == K_l: username += "L"
               elif event.key == K_m: username += "M"
               elif event.key == K_n: username += "N"
               elif event.key == K_o: username += "O"
               elif event.key == K_p: username += "P"
               elif event.key == K_q: username += "Q"
               elif event.key == K_r: username += "R"
               elif event.key == K_s: username += "S"
               elif event.key == K_t: username += "T"
               elif event.key == K_u: username += "U"
               elif event.key == K_v: username += "V"
               elif event.key == K_w: username += "W"
               elif event.key == K_x: username += "X"
               elif event.key == K_y: username += "Y"
               elif event.key == K_z: username += "Z"
               elif event.key == K_0: username += ")"
               elif event.key == K_1: username += "!"
               elif event.key == K_2: username += "@"
               elif event.key == K_3: username += "#"
               elif event.key == K_4: username += "$"
               elif event.key == K_5: username += "%"
               elif event.key == K_6: username += "^"
               elif event.key == K_7: username += "&"
               elif event.key == K_8: username += "*"
               elif event.key == K_9: username += "("
               elif event.key == K_BACKQUOTE: username += "~"
               elif event.key == K_MINUS: username += "_"
               elif event.key == K_EQUALS: username += "+"
               elif event.key == K_LEFTBRACKET: username += "{"
               elif event.key == K_RIGHTBRACKET: username += "}"
               elif event.key == K_BACKSLASH: username += "|"
               elif event.key == K_SEMICOLON: username += ":"
               elif event.key == K_QUOTE: username += "\""
               elif event.key == K_COMMA: username += "<"
               elif event.key == K_PERIOD: username += ">"
               elif event.key == K_SLASH: username += "?" 
         if event.type == MOUSEBUTTONDOWN:
            x_mouse_position_main, y_mouse_position_main = pygame.mouse.get_pos()
            x_mouse_position_main *= xScale
            y_mouse_position_main *= yScale
            print(str(x_mouse_position_main) + str(y_mouse_position_main))
            
            if event.button == 1:
               # click refresh
               if refresh_x_pos <= x_mouse_position_main <= refresh_x_pos + 200 and refresh_y_pos <= y_mouse_position_main <= refresh_y_pos + 100:
                  #print("clicked refresh")
                  request(x_panel_position, y_panel_position, y_offset)

               # clicked join
               for join_button in l_join_spots:
                  if join_button[0] <= x_mouse_position_main <= join_button[0] + 200 and join_button[1] <= y_mouse_position_main <= join_button[1] + 100:
                     if username == "":
                        LOGIN_TOP_SURFACE.blit(NO_USERNAME_MESSAGE, MESSAGE_COORDS)
                     else:
                        joinGame(join_button[2])
                     x_mouse_position_main = 0
                     y_mouse_position_main = 0
                  
               # clicked back button
               if x_back_button <= x_mouse_position_main <= x_back_button + 75 and y_back_button <= y_mouse_position_main <= y_back_button + 50:
                  client_socket.close()
                  return(True)
                  
               # clicked up arrow
               if arrow_x_pos <= x_mouse_position_main<= arrow_x_pos + 100 and up_arrow_y_pos <= y_mouse_position_main <= up_arrow_y_pos + 75 and y_offset > -y_offset_allowed and len(l_servers) > 5:
                  SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
                  y_offset -= 25
                  #display_servers(x_panel_position, y_panel_position, y_offset)
               
               
               # clicked down arrow
               if arrow_x_pos <= x_mouse_position_main <= arrow_x_pos + 100 and down_arrow_y_pos <= y_mouse_position_main <= down_arrow_y_pos + 75 and y_offset < 0 and len(l_servers) > 5:
                  SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
                  y_offset += 25
                  #display_servers(x_panel_position, y_panel_position, y_offset)
               
            if event.button == 4 and y_offset < 0 and len(l_servers) > 5:
               SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
               y_offset += 25
               
            if event.button == 5 and y_offset > -y_offset_allowed and len(l_servers) > 5:
               SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
               y_offset -= 25
               
      if len(l_servers) <= 5:
         y_offset = 0
                        
      # Blit the stuffs onto the screen
      username = filter.clean(username)
      LOGIN_TOP_SURFACE.blit(BLACK_BACKGROUND, (100, 100))
      display_servers(x_panel_position, y_panel_position, y_offset)
      LOGIN_TOP_SURFACE.blit(LOGIN_BACKGROUND, (0,0))
      #LOGIN_TOP_SURFACE.blit(USERNAME_BOX, (280, Y_POS))
      #LOGIN_TOP_SURFACE.blit(SERVER_FONT.render("Username: ", 1, (0,0,0)), (X_POS, Y_POS))
      LOGIN_TOP_SURFACE.blit(SERVER_FONT.render(username, 1, (0,0,0)), (285, Y_POS))
      LOGIN_TOP_SURFACE.blit(DOWN_ARROW, (arrow_x_pos, down_arrow_y_pos))
      LOGIN_TOP_SURFACE.blit(UP_ARROW, (arrow_x_pos, up_arrow_y_pos))
      button("Refresh",refresh_x_pos,refresh_y_pos,200,100,REFRESH_BUTTON_PRESSED,REFRESH_BUTTON_UNPRESSED)
      pushed_back = button("Back",x_back_button,y_back_button,75,50,BACK_BUTTON_PRESSED,BACK_BUTTON_UNPRESSED)
      if pushed_back:
         client_socket.close()
         return
      if username == "":
         LOGIN_TOP_SURFACE.blit(NO_USERNAME_MESSAGE, MESSAGE_COORDS)
      newSurface = pygame.transform.scale(LOGIN_TOP_SURFACE,(screenInfo.current_w, screenInfo.current_h), window)
      pygame.display.update()
      
if __name__ == '__main__':
   LoginClient()