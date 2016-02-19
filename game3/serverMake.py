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
import random
import re


def MakeServer():

   """
   Module that provides a class that filters profanities

   """

   __author__ = "leoluk"
   __version__ = '0.0.1'

   class ProfanitiesFilter(object):
       def __init__(self, filterlist, ignore_case=True, replacements="$@%-?!", 
                    complete=True, inside_words=True):
           """
           Inits the profanity filter.

           filterlist -- a list of regular expressions that
           matches words that are forbidden
           ignore_case -- ignore capitalization
           replacements -- string with characters to replace the forbidden word
           complete -- completely remove the word or keep the first and last char?
           inside_words -- search inside other words?

           """

           self.badwords = filterlist
           self.ignore_case = ignore_case
           self.replacements = replacements
           self.complete = complete
           self.inside_words = inside_words

       def _make_clean_word(self, length):
           """
           Generates a random replacement string of a given length
           using the chars in self.replacements.

           """
           return ''.join([random.choice(self.replacements) for i in
                     range(length)])

       def __replacer(self, match):
           value = match.group()
           if self.complete:
               return self._make_clean_word(len(value))
           else:
               return value[0]+self._make_clean_word(len(value)-2)+value[-1]

       def clean(self, text):
           """Cleans a string from profanity."""

           regexp_insidewords = {
               True: r'(%s)',
               False: r'\b(%s)\b',
               }

           regexp = (regexp_insidewords[self.inside_words] % 
                     '|'.join(self.badwords))

           r = re.compile(regexp, re.IGNORECASE if self.ignore_case else 0)

           return r.sub(self.__replacer, text)

   
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
         DISPLAYSURFACE.blit(button_pressed, (x, y))
         if click[0] == 1 and msg == "Start":
            print("THIS PRINTS IN THE BUTTON")
            request(x_panel_position, y_panel_position, y_offset)
      else:
         DISPLAYSURFACE.blit(button_unpressed, (x, y))
         
      smallText = pygame.font.Font("freesansbold.ttf",20)
      textSurf, textRect = text_objects(msg, smallText, l_colors[WHITE])
      textRect.center = ( (x+(w/2)), (y+(h/2)) )
      
   # Initialize pygame
   pygame.init()

   # Initilize bad word list
   filter = ProfanitiesFilter([
                              "2g1c",
                              "2 girls 1 cup",
                              "acrotomophilia",
                              "anal",
                              "anilingus",
                              "anus",
                              "arsehole",
                              "ass",
                              "asshole",
                              "assmunch",
                              "auto erotic",
                              "autoerotic",
                              "babeland",
                              "baby batter",
                              "ball gag",
                              "ball gravy",
                              "ball kicking",
                              "ball licking",
                              "ball sack",
                              "ball sucking",
                              "bangbros",
                              "bareback",
                              "barely legal",
                              "barenaked",
                              "bastardo",
                              "bastinado",
                              "bbw",
                              "bdsm",
                              "beaver cleaver",
                              "beaver lips",
                              "bestiality",
                              "bi curious",
                              "big black",
                              "big breasts",
                              "big knockers",
                              "big tits",
                              "bimbos",
                              "birdlock",
                              "bitch",
                              "black cock",
                              "blonde action",
                              "blonde on blonde action",
                              "blow j",
                              "blow your l",
                              "blue waffle",
                              "blumpkin",
                              "bollocks",
                              "bondage",
                              "boner",
                              "boob",
                              "boobs",
                              "booty call",
                              "brown showers",
                              "brunette action",
                              "bukkake",
                              "bulldyke",
                              "bullet vibe",
                              "bung hole",
                              "bunghole",
                              "busty",
                              "butt",
                              "buttcheeks",
                              "butthole",
                              "camel toe",
                              "camgirl",
                              "camslut",
                              "camwhore",
                              "carpet muncher",
                              "carpetmuncher",
                              "chocolate rosebuds",
                              "circlejerk",
                              "cleveland steamer",
                              "clit",
                              "clitoris",
                              "clover clamps",
                              "clusterfuck",
                              "cock",
                              "cocks",
                              "coprolagnia",
                              "coprophilia",
                              "cornhole",
                              "cum",
                              "cumming",
                              "cunnilingus",
                              "cunt",
                              "darkie",
                              "date rape",
                              "daterape",
                              "deep throat",
                              "deepthroat",
                              "dick",
                              "dildo",
                              "dirty pillows",
                              "dirty sanchez",
                              "dog style",
                              "doggie style",
                              "doggiestyle",
                              "doggy style",
                              "doggystyle",
                              "dolcett",
                              "domination",
                              "dominatrix",
                              "dommes",
                              "donkey punch",
                              "double dong",
                              "double penetration",
                              "dp action",
                              "eat my ass",
                              "ecchi",
                              "ejaculation",
                              "erotic",
                              "erotism",
                              "escort",
                              "ethical slut",
                              "eunuch",
                              "faggot",
                              "fecal",
                              "felch",
                              "fellatio",
                              "feltch",
                              "female squirting",
                              "femdom",
                              "figging",
                              "fingering",
                              "fisting",
                              "foot fetish",
                              "footjob",
                              "frotting",
                              "fuck",
                              "fucking",
                              "fuck buttons",
                              "fudge packer",
                              "fudgepacker",
                              "futanari",
                              "g-spot",
                              "gang bang",
                              "gay sex",
                              "genitals",
                              "giant cock",
                              "girl on",
                              "girl on top",
                              "girls gone wild",
                              "goatcx",
                              "goatse",
                              "gokkun",
                              "golden shower",
                              "goo girl",
                              "goodpoop",
                              "goregasm",
                              "grope",
                              "group sex",
                              "guro",
                              "hand job",
                              "handjob",
                              "hard core",
                              "hardcore",
                              "hentai",
                              "homoerotic",
                              "honkey",
                              "hooker",
                              "hot chick",
                              "how to kill",
                              "how to murder",
                              "huge fat",
                              "humping",
                              "incest",
                              "intercourse",
                              "jack off",
                              "jail bait",
                              "jailbait",
                              "jerk off",
                              "jigaboo",
                              "jiggaboo",
                              "jiggerboo",
                              "jizz",
                              "juggs",
                              "kike",
                              "kinbaku",
                              "kinkster",
                              "kinky",
                              "knobbing",
                              "leather restraint",
                              "leather straight jacket",
                              "lemon party",
                              "lolita",
                              "lovemaking",
                              "make me come",
                              "male squirting",
                              "masturbate",
                              "menage a trois",
                              "milf",
                              "missionary position",
                              "motherfucker",
                              "mound of venus",
                              "mr hands",
                              "muff diver",
                              "muffdiving",
                              "nambla",
                              "nawashi",
                              "negro",
                              "neonazi",
                              "nig nog",
                              "nigga",
                              "nigger",
                              "nimphomania",
                              "nipple",
                              "nipples",
                              "nsfw images",
                              "nude",
                              "nudity",
                              "nympho",
                              "nymphomania",
                              "octopussy",
                              "omorashi",
                              "one cup two girls",
                              "one guy one jar",
                              "orgasm",
                              "orgy",
                              "paedophile",
                              "panties",
                              "panty",
                              "pedobear",
                              "pedophile",
                              "pegging",
                              "penis",
                              "phone sex",
                              "piece of shit",
                              "piss pig",
                              "pissing",
                              "pisspig",
                              "playboy",
                              "pleasure chest",
                              "pole smoker",
                              "ponyplay",
                              "poof",
                              "poop chute",
                              "poopchute",
                              "porn",
                              "porno",
                              "pornography",
                              "prince albert piercing",
                              "pthc",
                              "pubes",
                              "pussy",
                              "queaf",
                              "raghead",
                              "raging boner",
                              "rape",
                              "raping",
                              "rapist",
                              "rectum",
                              "reverse cowgirl",
                              "rimjob",
                              "rimming",
                              "rosy palm",
                              "rosy palm and her 5 sisters",
                              "rusty trombone",
                              "s&m",
                              "sadism",
                              "scat",
                              "schlong",
                              "scissoring",
                              "semen",
                              "sex",
                              "sexo",
                              "sexy",
                              "shaved beaver",
                              "shaved pussy",
                              "shemale",
                              "shibari",
                              "shit",
                              "shota",
                              "shrimping",
                              "slanteye",
                              "slut",
                              "smut",
                              "snatch",
                              "snowballing",
                              "sodomize",
                              "sodomy",
                              "spic",
                              "spooge",
                              "spread legs",
                              "strap on",
                              "strapon",
                              "strappado",
                              "strip club",
                              "style doggy",
                              "suck",
                              "sucks",
                              "suicide girls",
                              "sultry women",
                              "swastika",
                              "swinger",
                              "tainted love",
                              "taste my",
                              "tea bagging",
                              "threesome",
                              "throating",
                              "tied up",
                              "tight white",
                              "tit",
                              "tits",
                              "titties",
                              "titty",
                              "tongue in a",
                              "topless",
                              "tosser",
                              "towelhead",
                              "tranny",
                              "tribadism",
                              "tub girl",
                              "tubgirl",
                              "tushy",
                              "twat",
                              "twink",
                              "twinkie",
                              "two girls one cup",
                              "undressing",
                              "upskirt",
                              "urethra play",
                              "urophilia",
                              "vagina",
                              "venus mound",
                              "vibrator",
                              "violet blue",
                              "violet wand",
                              "vorarephilia",
                              "voyeur",
                              "vulva",
                              "wank",
                              "wet dream",
                              "wetback",
                              "white power",
                              "women rapping",
                              "wrapping men",
                              "wrinkled starfish",
                              "xx",
                              "xxx",
                              "yaoi",
                              "yellow showers",
                              "yiffy",
                              "zoophilia"
                              "damn"], replacements="-")
                              
   # Initialize servername
   servername = ""

   # Specify that shift is not pressed
   shifted = False
   
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
   START_SERVER_BUTTON_PRESSED =  pygame.image.load(IMAGE_FILE_PATH + "start_server_button_pressed.png")
   START_SERVER_BUTTON_UNPRESSED =  pygame.image.load(IMAGE_FILE_PATH + "start_server_button_unpressed.png")
   SERVER_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 35)
   
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
      servername = filter.clean(servername)
      servername_graphics = SERVER_FONT.render(servername, 1, (0,0,0))
      DISPLAYSURFACE.blit(SERVERNAME_BOX, (330, y_pos))
      DISPLAYSURFACE.blit(servername_prompt, (x_pos, y_pos))
      DISPLAYSURFACE.blit(servername_graphics, (335, y_pos))
      DISPLAYSURFACE.blit(PLAY_BUTTON, (1300, 700))
      #DISPLAYSURFACE.blit(START_SERVER_BUTTON, (x_start_server_button, y_start_server_button))
      button("Start",x_start_server_button,y_start_server_button,150,75,START_SERVER_BUTTON_PRESSED,START_SERVER_BUTTON_UNPRESSED)
      #button("Play",1300,700,200,200,START_SERVER_BUTTON_PRESSED,START_SERVER_BUTTON_UNPRESSED)
      
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
      
if __name__ == '__main__':
   MakeServer()