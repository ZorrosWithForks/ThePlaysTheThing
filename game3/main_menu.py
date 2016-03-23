import pygame
from pygame.locals import *
import time
import random
#import clientSetup
#import serverSetup
import clientLogin
import serverMake

#^Imported libraries MUST have the function/if_MAIN thing at the end or else they will be run
# immediately upon import

pygame.init()

MENU_SURFACE = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

IMAGE_FILE_PATH = "ImageFiles\\"
MENU_BACKGROUND = pygame.image.load(IMAGE_FILE_PATH + "Main_menu.png").convert_alpha()
JOIN_UNLIT = pygame.image.load(IMAGE_FILE_PATH + "JoinGame.png").convert_alpha()
JOIN_LIT = pygame.image.load(IMAGE_FILE_PATH + "JoinGameLit.png").convert_alpha()
NEW_UNLIT = pygame.image.load(IMAGE_FILE_PATH + "NewGame.png").convert_alpha()
NEW_LIT = pygame.image.load(IMAGE_FILE_PATH + "NewGameLit.png").convert_alpha()
EXIT_UNLIT = pygame.image.load(IMAGE_FILE_PATH + "Exit.png").convert_alpha()
EXIT_LIT = pygame.image.load(IMAGE_FILE_PATH + "ExitLit.png").convert_alpha()

SOUND_FILE_PATH = "Sounds\\"
pygame.mixer.music.load(SOUND_FILE_PATH + "The Pyre.mp3")
pygame.mixer.music.play(-1)
 
#gameDisplay = pygame.display.set_mode((display_width,display_height))
gameDisplay = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
display_width = gameDisplay.get_width()
display_height = gameDisplay.get_height()

def game_intro():
   JOIN_COORDS = (450, 400)
   NEW_COORDS = (800, 400)
   EXIT_COORDS = (670, 720)
   intro = True

   while intro:
      mouse_x, mouse_y = pygame.mouse.get_pos()
      over_join = JOIN_COORDS[0] <= mouse_x <= JOIN_COORDS[0] + 300 and JOIN_COORDS[1] <= mouse_y <= JOIN_COORDS[1] + 300
      over_new = NEW_COORDS[0] <= mouse_x <= NEW_COORDS[0] + 300 and NEW_COORDS[1] <= mouse_y <= NEW_COORDS[1] + 300
      over_exit = EXIT_COORDS[0] <= mouse_x <= EXIT_COORDS[0] + 300 and EXIT_COORDS[1] <= mouse_y <= EXIT_COORDS[1] + 300
      for event in pygame.event.get():
         #print(event)
         if event.type == MOUSEBUTTONDOWN:
            if over_join:
               clientLogin.LoginClient()
            elif over_new:
               serverMake.MakeServer()
            elif over_exit:
               intro = False
         if event.type == KEYDOWN and event.key == K_ESCAPE:
            intro = False
            
      MENU_SURFACE.blit(MENU_BACKGROUND, (0,0))
      MENU_SURFACE.blit(JOIN_LIT if over_join else JOIN_UNLIT, JOIN_COORDS)
      MENU_SURFACE.blit(NEW_LIT if over_new else NEW_UNLIT, NEW_COORDS)
      MENU_SURFACE.blit(EXIT_LIT if over_exit else EXIT_UNLIT, EXIT_COORDS)

      pygame.display.update()
    
in_menu = True
in_game = False
    
# Will need to edit the looping logic to allow quitting to return to the main menu
game_intro()
pygame.quit()
quit()