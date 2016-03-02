def LoginClient():
   def display_players(x_panel_position, y_panel_position, y_offset):
      for player in l_players:
         LOGIN_TOP_SURFACE.blit(SERVER_BAR, (x_panel_position, y_panel_position + y_offset))
        
         # display the name of the player
         LOGIN_TOP_SURFACE.blit(SERVER_FONT.render(str(player[1]), True, (0,0,0)), (x_panel_position + 50, y_panel_position + 25 + y_offset))
         LOGIN_TOP_SURFACE.blit(JOIN_BUTTON_UNPRESSED, (x_panel_position + 1100, y_panel_position + 25 + y_offset))
         l_join_spots.append((x_panel_position + 1100, y_panel_position + 25, player[0]))
         y_panel_position += 100
   
   
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

   # Declare Server Font
   SERVER_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 35)
   width, height = SERVER_FONT.size("Username:")

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
   no_username_message = SERVER_FONT.render("Please type your username", 1, (255,0,0))

   # Position of the text box
   X_POS = 100
   Y_POS = 725

   # Initialize bad word filter
   filter = ProfanitiesFilter(filterlist=bad_things, replacements="!")

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

   print("Made it")
   t_search = threading.Thread(target=search, args=(x_panel_position, y_panel_position, y_offset))
   t_search.daemon = True
   t_search.start()
   print("Am I here?")
   
   # Get the username
   while True:
      curr_x, curr_y = pygame.mouse.get_pos()
      
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
            if event.key == K_UP:
               SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
               y_offset -= 100
               display_servers(x_panel_position, y_panel_position, y_offset)
            if event.key == K_DOWN:
               SERVERS_AREA = LOGIN_TOP_SURFACE.get_clip()
               if (SERVERS_AREA.x <= 100 and SERVERS_AREA.y <= 100):#put in server checking too need to find out how to get the position of a surface.
                  print("Servers area x is: " + str(SERVERS_AREA.x))
                  print("Servers area y is: " + str(SERVERS_AREA.y))
                  y_offset += 100
                  display_servers(x_panel_position, y_panel_position, y_offset)
         if event.type == MOUSEBUTTONDOWN:
            # clicked back button
            if x_back_button <= curr_x <= x_back_button + 75 and y_back_button <= curr_y <= y_back_button + 50:
               client_socket.close()
               return(True)
                        
      # Blit the stuffs onto the screen
      username = filter.clean(username)
      LOGIN_TOP_SURFACE.blit(BLACK_BACKGROUND, (100, 100))
      display_servers(x_panel_position, y_panel_position, y_offset)
      LOGIN_TOP_SURFACE.blit(LOGIN_BACKGROUND, (0,0))
      LOGIN_TOP_SURFACE.blit(SERVER_FONT.render(username, 1, (0,0,0)), (285, Y_POS))
      LOGIN_TOP_SURFACE.blit(DOWN_ARROW, (arrow_x_pos, down_arrow_y_pos))
      LOGIN_TOP_SURFACE.blit(UP_ARROW, (arrow_x_pos, up_arrow_y_pos))
      if x_back_button <= curr_x <= x_back_button + 75 and y_back_button <= curr_y <= y_back_button + 50:
         LOGIN_TOP_SURFACE.blit(BACK_BUTTON_PRESSED, (x_back_button,y_back_button))
      else:
         LOGIN_TOP_SURFACE.blit(BACK_BUTTON_UNPRESSED, (x_back_button,y_back_button))
      waiting_on_players = SERVER_FONT.render("Waiting on players:", 1, (0,255,255))
               
      pygame.display.update()