import pygame, sys
from pygame.locals import *
import time
import random
import clientSetup
import serverSetup
import serverMake
import clientLogin

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
 
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText, black)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
 
    #pygame.display.update()
 
    time.sleep(2)
 
    game_loop()
    
def button(msg, x, y, w, h, ic, ac, action=None):
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
      pygame.draw.rect(gameDisplay, ac,(x,y,w,h), 5)

      if click[0] == 1 and action != None:
         action()
   else:
      pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

   smallText = pygame.font.Font("freesansbold.ttf",20)
   textSurf, textRect = text_objects(msg, smallText, white)
   textRect.center = ( (x+(w/2)), (y+(h/2)) )
   gameDisplay.blit(textSurf, textRect)
    
def quitgame():
   pygame.quit()

def game_intro(servername):
   intro = True
   shifted = False

   while intro:
      gameDisplay.fill(white)
      largeText = pygame.font.Font('freesansbold.ttf',95)
      TextSurf, TextRect = text_objects("Staged Conflict", largeText, black)
      TextRect.center = ((display_width/2),(display_height/2) - 150)
      gameDisplay.blit(TextSurf, TextRect)
      
      mouse = pygame.mouse.get_pos()
        
      button("Host Game",250,300,300,50,green,bright_green, serverMake.Makeserver(servername))
      button("Join Game",250,375,300,50,red,bright_red, clientLogin.Loginclient)
      button("Quit",250,450,300,50,black,grey,quitgame)
      
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
               print(username)
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
         if event.type == MOUSEBUTTONDOWN:
            x_mouse_position_main, y_mouse_position_main = pygame.mouse.get_pos()
            print(str(x_mouse_position_main) + str(y_mouse_position_main))
            print("clicked mounce here")
            
      # Blit the username onto the screen
      complete_text = font.render("Servername: "+servername, 1, (0,255,0))
      gameDisplay.blit(complete_text, (100, 500))
      pygame.display.update()

      clock.tick(15)
    

    

 
pygame.init()
 
servername = ""
font = pygame.font.Font(None, 50)
display_width = 800
display_height = 600
 
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

grey = (55,55,55)
 
block_color = (53,115,255)
 
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Staged Conflict')
clock = pygame.time.Clock()
game_intro(servername)
pygame.quit()
quit()