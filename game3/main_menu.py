import pygame
import time
import random
#import clientSetup
import serverMake
import clientLogin

#^Imported libraries MUST have the function/if_MAIN thing at the end or else they will be run
# immediately upon import

pygame.init()
 
#display_width = 800
#display_height = 600
 
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

grey = (55,55,55)
 
block_color = (53,115,255)

MENU = 1

HOST = 2

JOIN = 3

QUIT = 0
 
#gameDisplay = pygame.display.set_mode((display_width,display_height))
gameDisplay = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
display_width = gameDisplay.get_width()
display_height = gameDisplay.get_height()


pygame.display.set_caption('Staged Conflict')
clock = pygame.time.Clock()
 
 
def text_objects(text, font, color):
   textSurface = font.render(text, True, color)
   return textSurface, textSurface.get_rect()
 
def message_display(text):
   largeText = pygame.font.Font('freesansbold.ttf',115)
   TextSurf, TextRect = text_objects(text, largeText, black)
   TextRect.center = ((display_width/2),(display_height/2))
   gameDisplay.blit(TextSurf, TextRect)
 
   pygame.display.update()
 
   time.sleep(2)
 
   game_loop()
    
def button(msg,x,y,w,h,ic,ac,action=None):
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
         #pygame.display.iconify()
         action()
   else:
      pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

   smallText = pygame.font.Font("freesansbold.ttf",20)
   textSurf, textRect = text_objects(msg, smallText, ac)
   textRect.center = ( (x+(w/2)), (y+(h/2)) )
   gameDisplay.blit(textSurf, textRect)
    
def quitgame():
   pygame.quit()

def game_intro():

   intro = True

   while intro:
      for event in pygame.event.get():
         #print(event)
         if event.type == pygame.QUIT:
            pygame.quit()
            quit()
                
      gameDisplay.fill(white)
      largeText = pygame.font.Font('freesansbold.ttf',190)
      TextSurf, TextRect = text_objects("Staged Conflict", largeText, black)
      TextRect.center = ((display_width/2),(display_height/2) - 150)
      gameDisplay.blit(TextSurf, TextRect)
        
      mouse = pygame.mouse.get_pos()
        
      button("Host Game",450,450,700,100,green,bright_green, serverMake.MakeServer)
      button("Join Game",450,600,700,100,red,bright_red, clientLogin.LoginClient)
      button("Quit",450,750,700,100,black,grey,quitgame)

      pygame.display.update()
      clock.tick(15)
    
in_menu = True
in_game = False
    
# Will need to edit the looping logic to allow quitting to return to the main menu
game_intro()
pygame.quit()
quit()

'''
game_state = MENU

while game_state != QUIT
   if game_state == MENU
      game_state = game_intro()
   elif game_state == HOST
      serverSetup.setupServer()
      game_state = MENU
   elif game_state == JOIN
      clientSetup.setupClient()
      game_state = MENU

pygame.quit()
quit()

'''