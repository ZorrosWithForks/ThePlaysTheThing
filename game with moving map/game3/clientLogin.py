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

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def printme():
   print ("printme")

# Program functions
def joinGame(ip):
   print("attempting to join " + ip)
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   addr = (ip, 9999)
   
   s.connect(addr)
   s.sendto(username.encode('ascii'), addr)
   print("joined")

   new_server = (s.recv(1024).decode(), 9998)
   s.close()
   SimpleClient.play(new_server, username)
   
def display_servers(l_servers, x_panel_position, y_panel_position):

   for server in l_servers:
      #print("server name is: ", + server[2])
      print("have a server from " + server[0])
      DISPLAYSURFACE.blit(SERVER_BAR, (x_panel_position, y_panel_position))
	  
      # display the name of the server
      DISPLAYSURFACE.blit(SERVER_FONT.render(str(server[1]), True, (0,0,0)), (x_panel_position + 900, y_panel_position + 25))
	  
      # any room for password?
      DISPLAYSURFACE.blit(JOIN_BUTTON, (x_panel_position + 1100, y_panel_position + 25))
      l_join_spots.append((x_panel_position + 1100, y_panel_position + 25, server[0]))
      y_panel_position += 100
      pygame.display.update()

def search(l_servers, x_panel_position, y_panel_position):
   while True:
      packet, addr = client_socket.recvfrom(4096)
      if packet != None:
         try:
            server_info = pickle.loads(packet)
            l_servers.append(server_info)
            print("added a server: " + server_info[0])
            display_servers(l_servers, x_panel_position, y_panel_position)
         except:
            #This is happening. why?
            print("Client tried connecting to itself")
      else:
         print("No recv_data")
      print("done displaying servers")
      
def request(l_servers, x_panel_position, y_panel_position):
   print("looping requesting servers")
   del l_servers[:]
   display_servers(l_servers, x_panel_position, y_panel_position)
   client_socket.sendto(data.encode('ascii'), address)

#def Loginclient():
# Initialize pygame
pygame.init()

# Graphics Constants
IMAGE_FILE_PATH = "ImageFiles\\"
LOGIN_BACKGROUND = pygame.image.load(IMAGE_FILE_PATH + "client_login_background.png")
SERVER_BAR = pygame.image.load(IMAGE_FILE_PATH + "Server.png")
JOIN_BUTTON = pygame.image.load(IMAGE_FILE_PATH + "JoinButton.png")
REFRESH_BUTTON = pygame.image.load(IMAGE_FILE_PATH + "RefreshButton2.png")

# Declare list of join button spots
l_join_spots = []

# Declare Server Font
SERVER_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 40)

# Declare the username
username = ""
font = pygame.font.Font(None, 50)
complete_text = "Username: "

# Position of the text box
x_pos = 600
y_pos = 700

# Position of the Server Panel
x_panel_position = 100
y_panel_position = 100

# Declare the Surface
DISPLAYSURFACE = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

# Client network stuff
l_servers = []
address = ('255.255.255.255', 8080)
data = "Request"
temp = socket.gethostbyname_ex(socket.gethostname())[-1]
host = temp[-1]
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_socket.bind((host, 8080))
client_socket.sendto(data.encode('ascii'), address)

print("Made it")
t_search = threading.Thread(target=search, args=(l_servers, x_panel_position, y_panel_position))
t_search.daemon = True
t_search.start()
print("Am I here?")

# Get the username
while True:
   mouse = pygame.mouse.get_pos()

   #specify that shift is not pressed
   shifted = False
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
      if event.type == KEYDOWN:
         if event.key == K_ESCAPE:
            #and the game and close the window
            print(username)
            print("something")
            pygame.quit()
            sys.exit()
         if event.key == K_BACKSPACE:
            username = username[:-1]
         elif event.key == K_LSHIFT or event.key == K_RSHIFT:
            shifted = True
         if not shifted:
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
         elif shifted:
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
         print(str(x_mouse_position_main) + str(y_mouse_position_main))
         print("clicked mounce here")
         if 1300 <= x_mouse_position_main <= 1500 and 700 <= y_mouse_position_main <= 800:
            print("clicked refresh")
            request(l_servers, x_panel_position, y_panel_position)
         for button in l_join_spots:
            if button[0] <= x_mouse_position_main <= button[0] + 200 and button[1] <= y_mouse_position_main <= button[1] + 100:
               pygame.display.iconify()
               joinGame(button[2])

   
   # Blit the username onto the screen
   complete_text = font.render("Username: "+username, 1, (0,255,0))
   DISPLAYSURFACE.blit(LOGIN_BACKGROUND, (0,0))
   DISPLAYSURFACE.blit(complete_text, (x_pos, y_pos))

   # Refresh the page
   DISPLAYSURFACE.blit(REFRESH_BUTTON, (1300, 700))

   pygame.display.update()
# if __name__ == '__main__':
# Loginclient()