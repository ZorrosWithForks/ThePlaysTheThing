import socket
import threading
from threading import Thread
import _thread
import pickle
import time
import select
import SimpleServer
import pygame, sys
from pygame.locals import *



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
   while True:
      client, client_address = serversocket.accept()
      player_name = client.recv(4096).decode()
      thread.append(Thread(target=listener, args = (client, client_address, clients, serversocket, player_name)).start())
      display_players()

def listener(client, client_address, clients, serversocket, player_name):
   print("Accepted connection from: ", client_address)
   with clients_lock:
      l_temp = (client, player_name, client_address)
      clients.add(l_temp)#Array of clients
      
      #print(str(len(clients)))
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
         
def display_players(x_panel_position, y_panel_position):
   print("Number of clients: " + str(len(clients)))
   for i in clients:
      DISPLAYSURFACE.blit(SERVER_BAR, (x_panel_position, y_panel_position))
      # display the name of the client
      DISPLAYSURFACE.blit(SERVER_FONT.render(str(i[1]), True, (0,0,0)), (x_panel_position + 25, y_panel_position + 25))
      DISPLAYSURFACE.blit(BOOT_BUTTON, (x_panel_position + 1300, y_panel_position + 25))
      l_boot_spots.append((x_panel_position, y_panel_position + 25, i[1]))
      y_panel_position += 100
      
def start_game():
   for client in clients:
      client[0].sendto(host.encode("ascii"), client[2])
   pygame.display.iconify()
   SimpleServer.serve(len(clients))

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

   
# Initialize pygame
pygame.init()

# Initialize servername
servername = ""

# Declare list of boot button spots
l_boot_spots = []

# Graphics Constants
IMAGE_FILE_PATH = "ImageFiles\\"
LOGIN_BACKGROUND = pygame.image.load(IMAGE_FILE_PATH + "client_login_background.png")
SERVER_BAR = pygame.image.load(IMAGE_FILE_PATH + "Server.png")
JOIN_BUTTON = pygame.image.load(IMAGE_FILE_PATH + "JoinButton.png")
REFRESH_BUTTON = pygame.image.load(IMAGE_FILE_PATH + "RefreshButton2.png")
PLAY_BUTTON = pygame.image.load(IMAGE_FILE_PATH+ "playbutton.png")
BOOT_BUTTON = pygame.image.load(IMAGE_FILE_PATH+ "BootButton.png")
SERVERNAME_BOX =  pygame.image.load(IMAGE_FILE_PATH + "username_box.png")
START_SERVER_BUTTON =  pygame.image.load(IMAGE_FILE_PATH + "start_server_button.png")
SERVER_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 35)

# Position of the text box
x_pos = 100
y_pos = 725

# Play button positions
x_play_button = 1300
y_play_button = 700

# Server panels positions
x_panel_position = 100
y_panel_position = 100

# Start server positions
x_start_server_button = 200
y_start_server_button = 800
    
    
# Declare the Surface
DISPLAYSURFACE = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

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
   for event in pygame.event.get():
      shifted = False
      if event.type == QUIT:
         #end game
         pygame.quit()
         sys.exit()
      if event.type == KEYUP:
        if event.key == K_LSHIFT or event.key == K_RSHIFT:
           shifted = False
      if event.type == KEYDOWN:
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
         if not shifted:
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
         elif shifted:
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
            
   # Blit the stuffs onto the screen
   DISPLAYSURFACE.blit(LOGIN_BACKGROUND, (0,0))
   servername_prompt = SERVER_FONT.render("Server Name: ", 1, (0,255,0))
   servername_graphics = SERVER_FONT.render(servername, 1, (0,0,0))
   DISPLAYSURFACE.blit(SERVERNAME_BOX, (330, y_pos))
   DISPLAYSURFACE.blit(servername_prompt, (x_pos, y_pos))
   DISPLAYSURFACE.blit(servername_graphics, (335, y_pos))
   DISPLAYSURFACE.blit(PLAY_BUTTON, (1300, 700))
   DISPLAYSURFACE.blit(START_SERVER_BUTTON, (x_start_server_button, y_start_server_button))
   
   
   if event.type == MOUSEBUTTONDOWN:
      x_mouse_position_main, y_mouse_position_main = pygame.mouse.get_pos()
      #print(str(x_mouse_position_main) + str(y_mouse_position_main))
     # print("clicked mounce here")
      
      # clicked play
      if x_play_button <= x_mouse_position_main <= x_play_button + 200 and y_play_button <= y_mouse_position_main <= y_play_button + 200:
        # print("clicked play")
         start_game()

      # clicked start
      if x_start_server_button <= x_mouse_position_main <= x_mouse_position_main + 150 and y_start_server_button <= y_mouse_position_main <= y_start_server_button + 75:
         pygame.display.iconify()
         begin_serving(servername, server_socket, x_panel_position, y_panel_position, clients)

   display_players(x_panel_position, y_panel_position)
   pygame.display.update()
   