#client.py
import socket
import os
import copy
import threading
from threading import Thread
import _thread
import pygame, sys, random
from pygame.locals import *
from pygame import font
import pickle
from Maps import *
import time
import Player
from os import listdir

pygame.font.init()

pygame.init()

screenInfo = pygame.display.Info()
DISPLAYSURF = pygame.Surface((1600,900))
window = pygame.display.set_mode((screenInfo.current_w,screenInfo.current_h), pygame.FULLSCREEN)
xScale = 1600.0 / float(screenInfo.current_w)
yScale = 900.0 / float(screenInfo.current_h)

   
#constants representing the different resources
IMAGE_FILE_PATH = "ImageFiles\\"
GAME_STAGE_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 55)
CONTINENT_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 40)
COUNTRY_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 25)
UNIT_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 35)
MONEY_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 22)
TURN_READOUT_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 18)
VICTOR_COLOR = (0, 50, 100)
ATTACK_COLOR = (100, 0, 0)
DEFEND_COLOR = (50, 50, 0)
ATTACK_COUNT_COLOR = (255, 0, 0)
DEFEND_COUNT_COLOR = (255, 255, 0)
CONTINENT_1 = 1
CONTINENT_2 = 2
CONTINENT_3 = 3
CONTINENT_4 = 4
CONTINENT_5 = 5
CONTINENT_6 = 6
CONTINENT_7 = 7
CONTINENT_8 = 8
UNOCCUPIED = "Unoccupied"
WATER = (0,0)
DEEP_WATER = 10
OVERLAY = 9
HELP_COORDS = [1135, 820]

# Graphics Constants
WATER_OUTLINE = pygame.image.load(IMAGE_FILE_PATH + 'water.png').convert_alpha()
t_WATER_OUTLINES = (
                     WATER_OUTLINE,
                     pygame.transform.rotate(WATER_OUTLINE, 90),
                     pygame.transform.rotate(WATER_OUTLINE, 180),
                     pygame.transform.rotate(WATER_OUTLINE, 270)
                   )
WATER_TEXTURE = pygame.image.load(IMAGE_FILE_PATH + 'deep_water.png').convert_alpha()
t_WATER_TEXTURES = (
                     WATER_TEXTURE,
                     pygame.transform.rotate(WATER_TEXTURE, 90),
                     pygame.transform.rotate(WATER_TEXTURE, 180),
                     pygame.transform.rotate(WATER_TEXTURE, 270)
                   )

GAME_CLOSE = pygame.image.load(IMAGE_FILE_PATH + "CloseGame.png").convert_alpha()
GAME_MINIM = pygame.image.load(IMAGE_FILE_PATH + "MinimizeGame.png").convert_alpha()
                   
INFO_BUY_UNITS = pygame.image.load(IMAGE_FILE_PATH + "InfoBuyUnits.png").convert_alpha()
INFO_ATTACK = pygame.image.load(IMAGE_FILE_PATH + "InfoAttack.png").convert_alpha()
INFO_RESOLVE = pygame.image.load(IMAGE_FILE_PATH + "InfoBattle.png").convert_alpha()
INFO_MOVE = pygame.image.load(IMAGE_FILE_PATH + "InfoMove.png").convert_alpha()
INFO_PISTOLEERS = pygame.image.load(IMAGE_FILE_PATH + "InfoPistoleers.png").convert_alpha()
INFO_MUSKETEERS = pygame.image.load(IMAGE_FILE_PATH + "InfoMusketeers.png").convert_alpha()
INFO_CANNONS = pygame.image.load(IMAGE_FILE_PATH + "InfoCannons.png").convert_alpha()
INFO_AIRSHIPS = pygame.image.load(IMAGE_FILE_PATH + "InfoAirships.png").convert_alpha()
INFO_BUTTON_OFF = pygame.image.load(IMAGE_FILE_PATH + "HelpButton.png").convert_alpha()
INFO_BUTTON_ON = pygame.image.load(IMAGE_FILE_PATH + "HelpButtonActive.png").convert_alpha()

ATK_UP = pygame.image.load(IMAGE_FILE_PATH + "AttackUp.png").convert_alpha()
ATK_DO = pygame.image.load(IMAGE_FILE_PATH + "AttackDown.png").convert_alpha()
ATK_LE = pygame.image.load(IMAGE_FILE_PATH + "AttackLeft.png").convert_alpha()
ATK_RI = pygame.image.load(IMAGE_FILE_PATH + "AttackRight.png").convert_alpha()
ATK_UR = pygame.image.load(IMAGE_FILE_PATH + "AttackUpRight.png").convert_alpha()
ATK_DL = pygame.image.load(IMAGE_FILE_PATH + "AttackLowLeft.png").convert_alpha()
ATK_UL = pygame.image.load(IMAGE_FILE_PATH + "AttackUpLeft.png").convert_alpha()
ATK_DR = pygame.image.load(IMAGE_FILE_PATH + "AttackLowRight.png").convert_alpha()
ATK_ER = pygame.image.load(IMAGE_FILE_PATH + "AttackRightEdge.png").convert_alpha()
ATK_EU = pygame.image.load(IMAGE_FILE_PATH + "AttackTopEdge.png").convert_alpha()
ATK_EL = pygame.image.load(IMAGE_FILE_PATH + "AttackLeftEdge.png").convert_alpha()
ATK_ED = pygame.image.load(IMAGE_FILE_PATH + "AttackBottomEdge.png").convert_alpha()

MOVE_UP = pygame.image.load(IMAGE_FILE_PATH + "MoveUp.png").convert_alpha()
MOVE_DO = pygame.image.load(IMAGE_FILE_PATH + "MoveDown.png").convert_alpha()
MOVE_LE = pygame.image.load(IMAGE_FILE_PATH + "MoveLeft.png").convert_alpha()
MOVE_RI = pygame.image.load(IMAGE_FILE_PATH + "MoveRight.png").convert_alpha()
MOVE_UR = pygame.image.load(IMAGE_FILE_PATH + "MoveUpRight.png").convert_alpha()
MOVE_DL = pygame.image.load(IMAGE_FILE_PATH + "MoveDownLeft.png").convert_alpha()
MOVE_UL = pygame.image.load(IMAGE_FILE_PATH + "MoveUpLeft.png").convert_alpha()
MOVE_DR = pygame.image.load(IMAGE_FILE_PATH + "MoveDownRight.png").convert_alpha()
MOVE_ER = pygame.image.load(IMAGE_FILE_PATH + "MoveRightEdge.png").convert_alpha()
MOVE_EU = pygame.image.load(IMAGE_FILE_PATH + "MoveTopEdge.png").convert_alpha()
MOVE_EL = pygame.image.load(IMAGE_FILE_PATH + "MoveLeftEdge.png").convert_alpha()
MOVE_ED = pygame.image.load(IMAGE_FILE_PATH + "MoveBottomEdge.png").convert_alpha()

MOUSE_OVER = pygame.image.load(IMAGE_FILE_PATH + 'MouseOver.png').convert_alpha()
MOUSE_OVER_UNKNOWN = pygame.image.load(IMAGE_FILE_PATH + 'MouseOverUnknown.png').convert_alpha()
BASE_BOARD = pygame.image.load(IMAGE_FILE_PATH + "BaseBoard.png").convert_alpha()
INFO_MARQUEE = pygame.image.load(IMAGE_FILE_PATH + "InfoMarque.png").convert_alpha()
INFO_OVERLAY = pygame.image.load(IMAGE_FILE_PATH + "InfoMarqueOverlay.png").convert_alpha()
MAP_FRAME = pygame.image.load(IMAGE_FILE_PATH + "MapFrame.png").convert_alpha()
MAP_LIGHT = pygame.image.load(IMAGE_FILE_PATH + "MapLighting.png").convert_alpha()
SELECTED_TILE = pygame.image.load(IMAGE_FILE_PATH + "Selected.png").convert_alpha()
ATTACK_OPTION = pygame.image.load(IMAGE_FILE_PATH + "AttackOption.png").convert_alpha()
MOVE_OPTION = pygame.image.load(IMAGE_FILE_PATH + "MoveOption.png").convert_alpha()
ATTACKER = pygame.image.load(IMAGE_FILE_PATH + "Attacker.png").convert_alpha()
DEFENDER = pygame.image.load(IMAGE_FILE_PATH + "Defender.png").convert_alpha()
SOURCE = pygame.image.load(IMAGE_FILE_PATH + "MoveSource.png").convert_alpha()
DESTINATION = pygame.image.load(IMAGE_FILE_PATH + "MoveDestination.png").convert_alpha()
WAITING = pygame.image.load(IMAGE_FILE_PATH + "Waiting.png").convert_alpha()

SEND_PISTOLEERS = pygame.image.load(IMAGE_FILE_PATH + "SendPistoleers.png").convert_alpha()
SEND_MUSKETEERS = pygame.image.load(IMAGE_FILE_PATH + "SendMusketeers.png").convert_alpha()
SEND_CANNONS = pygame.image.load(IMAGE_FILE_PATH + "SendCannons.png").convert_alpha()
SEND_AIRSHIPS = pygame.image.load(IMAGE_FILE_PATH + "SendAirships.png").convert_alpha()
DONE_BUTTON = pygame.image.load(IMAGE_FILE_PATH + "DoneButton.png").convert_alpha()
DONE_BUTTON_ACTIVE = pygame.image.load(IMAGE_FILE_PATH + "DoneButtonActive.png").convert_alpha()

MOVE_PISTOLEERS = pygame.image.load(IMAGE_FILE_PATH + "MovePistoleers.png").convert_alpha()
MOVE_MUSKETEERS = pygame.image.load(IMAGE_FILE_PATH + "MoveMusketeers.png").convert_alpha()
MOVE_CANNONS    = pygame.image.load(IMAGE_FILE_PATH + "MoveCannons.png").convert_alpha()
MOVE_AIRSHIPS   = pygame.image.load(IMAGE_FILE_PATH + "MoveAirships.png").convert_alpha()

UNIT_ATTACK_HIGHLIGHT = pygame.image.load(IMAGE_FILE_PATH + "UnitHighlightAttack.png").convert_alpha()
UNIT_MOVE_HIGHLIGHT = pygame.image.load(IMAGE_FILE_PATH + "UnitHighlightMove.png").convert_alpha()
ATTACK_INDICATOR = pygame.image.load(IMAGE_FILE_PATH + "AttackIndicator.png").convert_alpha()
MOVE_INDICATOR = pygame.image.load(IMAGE_FILE_PATH + "MoveIndicator.png").convert_alpha()

CRASH_MESSAGE = pygame.image.load(IMAGE_FILE_PATH + "InfoServerLost.png").convert_alpha()
ATTACK_RESULTS = pygame.image.load(IMAGE_FILE_PATH + "AttackResults.png").convert_alpha()
OK_UNLIT = pygame.image.load(IMAGE_FILE_PATH + "OK.png").convert_alpha()
OK_LIT = pygame.image.load(IMAGE_FILE_PATH + "OKLit.png").convert_alpha()
EXIT_UNLIT = pygame.image.load(IMAGE_FILE_PATH + "Exit.png").convert_alpha()
EXIT_LIT = pygame.image.load(IMAGE_FILE_PATH + "ExitLit.png").convert_alpha()
WINNER = pygame.image.load(IMAGE_FILE_PATH + "InfoVictory.png").convert_alpha()
LOSER = pygame.image.load(IMAGE_FILE_PATH + "InfoDefeat.png").convert_alpha()

MOUSE_LIT = pygame.image.load(IMAGE_FILE_PATH + "MouseLit.png").convert_alpha()
MOUSE_UNLIT = pygame.image.load(IMAGE_FILE_PATH + "MouseUnlit.png").convert_alpha()

BACKGROUND = pygame.display.set_mode((screenInfo.current_w,screenInfo.current_h), pygame.FULLSCREEN)
backgroundSurface = None

SOUND_FILE_PATH = "Sounds\\"
try:
   pygame.mixer.init(size=16)
   SONG_END = pygame.USEREVENT + 1
   pygame.mixer.music.set_endevent(SONG_END)
   l_songs = listdir(SOUND_FILE_PATH)
   l_bad = []

   for file in l_songs:
      if file[-3:] not in ("mp3", "ogg"):
         l_bad.append(file)

   for bad in l_bad:
      l_songs.remove(bad)
   song_index = 0
except:
   pass

def blitInfo(DISPLAYSURF, map, phase_info, displayUnitThings=True):
   curr_x, curr_y = pygame.mouse.get_pos()
   curr_x *= xScale
   curr_y *= yScale
   
   if displayUnitThings:
      if 170 <= curr_x <= 70 + 350 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120:
         DISPLAYSURF.blit(INFO_PISTOLEERS, (0, 0))
      elif 575 <= curr_x <= 575 + 250 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120:
         DISPLAYSURF.blit(INFO_MUSKETEERS, (0, 0))
      elif 170 <= curr_x <= 70 + 350 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175:
         DISPLAYSURF.blit(INFO_CANNONS, (0, 0))
      elif 575 <= curr_x <= 575 + 250 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175:
         DISPLAYSURF.blit(INFO_AIRSHIPS, (0, 0))
   
   if 1085 <= curr_x <= 1185 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 175:
      DISPLAYSURF.blit(phase_info, (0, 0))
      DISPLAYSURF.blit(INFO_BUTTON_ON, (1085, map.HEIGHT * TILESIZE + 70))
   else:
      DISPLAYSURF.blit(INFO_BUTTON_OFF, (1085, map.HEIGHT * TILESIZE + 70))

def blitBattle(map, DISPLAYSURF, attack_coords, defend_coords):
   blitCoords = (attack_coords[0] * TILESIZE - 50, attack_coords[1] * TILESIZE - 50)

   if attack_coords[0] == 0 and defend_coords[0] == map.WIDTH - 1:
      DISPLAYSURF.blit(ATK_EL, blitCoords, special_flags=BLEND_ADD)
   elif attack_coords[0] == map.WIDTH - 1 and defend_coords[0] == 0:
      DISPLAYSURF.blit(ATK_ER, blitCoords, special_flags=BLEND_ADD)
   elif attack_coords[1] == 0 and defend_coords[1] == map.HEIGHT - 1:
      DISPLAYSURF.blit(ATK_EU, blitCoords, special_flags=BLEND_ADD)
   elif attack_coords[1] == map.HEIGHT - 1 and defend_coords[1] == 0:
      DISPLAYSURF.blit(ATK_ED, blitCoords, special_flags=BLEND_ADD)
   elif attack_coords[0] == defend_coords[0]:
      if attack_coords[1] < defend_coords[1]:
         DISPLAYSURF.blit(ATK_DO, blitCoords, special_flags=BLEND_ADD)
      else: # attack_coords[1] > defend_coords[1]:
         DISPLAYSURF.blit(ATK_UP, blitCoords, special_flags=BLEND_ADD)
   elif attack_coords[1] == defend_coords[1]:
      if attack_coords[0] < defend_coords[0]:
         DISPLAYSURF.blit(ATK_RI, blitCoords, special_flags=BLEND_ADD)
      else: # attack_coords[0] > defend_coords[0]:
         DISPLAYSURF.blit(ATK_LE, blitCoords, special_flags=BLEND_ADD)
   elif attack_coords[0] < defend_coords[0]:
      if attack_coords[1] < defend_coords[1]:
         DISPLAYSURF.blit(ATK_DR, blitCoords, special_flags=BLEND_ADD)
      elif attack_coords[1] > defend_coords[1]:
         DISPLAYSURF.blit(ATK_UR, blitCoords, special_flags=BLEND_ADD)
   elif attack_coords[0] > defend_coords[0]:
      if attack_coords[1] < defend_coords[1]:
         DISPLAYSURF.blit(ATK_DL, blitCoords, special_flags=BLEND_ADD)
      elif attack_coords[1] > defend_coords[1]:
         DISPLAYSURF.blit(ATK_UL, blitCoords, special_flags=BLEND_ADD)
      

def blitMove(map, DISPLAYSURF, source_coords, dest_coords):
   blitCoords = (source_coords[0] * TILESIZE - 50, source_coords[1] * TILESIZE - 50)

   if source_coords[0] == 0 and dest_coords[0] == map.WIDTH - 1:
      DISPLAYSURF.blit(MOVE_EL, blitCoords, special_flags=BLEND_ADD)
   elif source_coords[0] == map.WIDTH - 1 and dest_coords[0] == 0:
      DISPLAYSURF.blit(MOVE_ER, blitCoords, special_flags=BLEND_ADD)
   elif source_coords[1] == 0 and dest_coords[1] == map.HEIGHT - 1:
      DISPLAYSURF.blit(MOVE_EU, blitCoords, special_flags=BLEND_ADD)
   elif source_coords[1] == map.HEIGHT - 1 and dest_coords[1] == 0:
      DISPLAYSURF.blit(MOVE_ED, blitCoords, special_flags=BLEND_ADD)
   elif source_coords[0] == dest_coords[0]:
      if source_coords[1] < dest_coords[1]:
         DISPLAYSURF.blit(MOVE_DO, blitCoords, special_flags=BLEND_ADD)
      else: # source_coords[1] > dest_coords[1]:
         DISPLAYSURF.blit(MOVE_UP, blitCoords, special_flags=BLEND_ADD)
   elif source_coords[1] == dest_coords[1]:
      if source_coords[0] < dest_coords[0]:
         DISPLAYSURF.blit(MOVE_RI, blitCoords, special_flags=BLEND_ADD)
      else: # source_coords[0] > dest_coords[0]:
         DISPLAYSURF.blit(MOVE_LE, blitCoords, special_flags=BLEND_ADD)
   elif source_coords[0] < dest_coords[0]:
      if source_coords[1] < dest_coords[1]:
         DISPLAYSURF.blit(MOVE_DR, blitCoords, special_flags=BLEND_ADD)
      elif source_coords[1] > dest_coords[1]:
         DISPLAYSURF.blit(MOVE_UR, blitCoords, special_flags=BLEND_ADD)
   elif source_coords[0] > dest_coords[0]:
      if source_coords[1] < dest_coords[1]:
         DISPLAYSURF.blit(MOVE_DL, blitCoords, special_flags=BLEND_ADD)
      elif source_coords[1] > dest_coords[1]:
         DISPLAYSURF.blit(MOVE_UL, blitCoords, special_flags=BLEND_ADD)

#a dictionary linking resources to textures
textures =   {
                OVERLAY : pygame.image.load(IMAGE_FILE_PATH + 'overlay.png'),
                CONTINENT_1 : pygame.image.load(IMAGE_FILE_PATH + 'continent_1.png'),
                CONTINENT_2 : pygame.image.load(IMAGE_FILE_PATH + 'continent_2.png'),
                CONTINENT_3 : pygame.image.load(IMAGE_FILE_PATH + 'continent_3.png'),
                CONTINENT_4 : pygame.image.load(IMAGE_FILE_PATH + 'continent_4.png'),
                CONTINENT_5 : pygame.image.load(IMAGE_FILE_PATH + 'continent_5.png'),
                CONTINENT_6 : pygame.image.load(IMAGE_FILE_PATH + 'continent_6.png'),
                CONTINENT_7 : pygame.image.load(IMAGE_FILE_PATH + 'continent_7.png'),
                CONTINENT_8 : pygame.image.load(IMAGE_FILE_PATH + 'continent_8.png'),
            }

l_playerLogos = [
                pygame.image.load(IMAGE_FILE_PATH + 'NoPlayer.png'),
                pygame.image.load(IMAGE_FILE_PATH + 'Player1.png'),
                pygame.image.load(IMAGE_FILE_PATH + 'Player2.png'),
                pygame.image.load(IMAGE_FILE_PATH + 'Player3.png'),
                pygame.image.load(IMAGE_FILE_PATH + 'Player4.png'),
                pygame.image.load(IMAGE_FILE_PATH + 'Player5.png'),
                pygame.image.load(IMAGE_FILE_PATH + 'Player6.png'),
                pygame.image.load(IMAGE_FILE_PATH + 'Player7.png')
              ]

l_playerColors = [
                (0,0,0), #Black
                (20,200,45), #Green
                (220,220,0), #Yellow
                (220,0,0), #Red
                (0,0,100), #Dark Blue
                (255,255,255), #White
                (220,110,0), #Orange
                (110,55,0) #Brown
              ]

d_playerLogoIndexes = { UNOCCUPIED: 0 }

#useful game dimensions
MARGIN = 50
TILESIZE  = 100
BOTTOM_HALF_START = 15

map_X_offset = 0
map_Y_offset = 0

d_continent_tiles = {}

def isOverButton(map, curr_x, curr_y):
   return ((175 + 245 <= curr_x <= 175 + 395 or 580 + 245 <= curr_x <= 580 + 395) and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120) or \
   ((175 + 245 <= curr_x <= 175 + 395 or 580 + 245 <= curr_x <= 580 + 395) and map.HEIGHT * TILESIZE + 125 < curr_y <= map.HEIGHT * TILESIZE + 175)
    
def printIndicator(image, map, DISPLAYSURF, curr_x, curr_y):
   if 175 + 245 <= curr_x <= 175 + 395 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120:
      DISPLAYSURF.blit(image, (map.WIDTH * TILESIZE + 25, 317), special_flags=BLEND_ADD)
   elif 580 + 245 <= curr_x <= 580 + 395 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120:
      DISPLAYSURF.blit(image, (map.WIDTH * TILESIZE + 25, 367), special_flags=BLEND_ADD)
   elif 175 + 245 <= curr_x <= 175 + 395 and map.HEIGHT * TILESIZE + 125 < curr_y <= map.HEIGHT * TILESIZE + 175:
      DISPLAYSURF.blit(image, (map.WIDTH * TILESIZE + 25, 417), special_flags=BLEND_ADD)
   elif 580 + 245 <= curr_x <= 580 + 395 and map.HEIGHT * TILESIZE + 125 < curr_y <= map.HEIGHT * TILESIZE + 175:
      DISPLAYSURF.blit(image, (map.WIDTH * TILESIZE + 25, 467), special_flags=BLEND_ADD)
      
def standardInfo(map, DISPLAYSURF, params):
   #Highlight country mouse is over and display country info
   curr_x, curr_y = pygame.mouse.get_pos()
   curr_x *= xScale
   curr_y *= yScale
   if (curr_x < map.WIDTH * TILESIZE and curr_y < map.HEIGHT * TILESIZE and map.ll_map[int(curr_y / TILESIZE)][int(curr_x / TILESIZE)] != map.WATER):
      curr_country = map.ll_map[int(curr_y / TILESIZE)][int(curr_x / TILESIZE)]
      DISPLAYSURF.blit(MOUSE_OVER if map.d_continents[curr_country[0]][curr_country[1]].owner != None else MOUSE_OVER_UNKNOWN, (int(curr_x / TILESIZE) * TILESIZE - MARGIN, int(curr_y / TILESIZE) * TILESIZE - MARGIN), special_flags=BLEND_ADD)
      current_tile = map.ll_map[int(curr_y / TILESIZE)][int(curr_x / TILESIZE)]
      DISPLAYSURF.blit(CONTINENT_FONT.render("Continent: " + current_tile[0], True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 120))
      DISPLAYSURF.blit(COUNTRY_FONT.render("Country: " + map.d_continents[current_tile[0]][current_tile[1]].name, True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 170))
      
      country_known = map.d_continents[current_tile[0]][current_tile[1]].owner != None 
      # Unit counts by type
      DISPLAYSURF.blit(COUNTRY_FONT.render("Pistoleers:", True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 225))
      DISPLAYSURF.blit(COUNTRY_FONT.render("Musketeers:", True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 250))
      DISPLAYSURF.blit(COUNTRY_FONT.render("Cannons:", True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 275))
      DISPLAYSURF.blit(COUNTRY_FONT.render("Airships:", True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 300))
      
      DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.infantry) if country_known else "?", True, (0,0,0)), (map.WIDTH * TILESIZE + 250, 225))
      DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.archers) if country_known else "?", True, (0,0,0)), (map.WIDTH * TILESIZE + 250, 250))
      DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.cannons) if country_known else "?", True, (0,0,0)), (map.WIDTH * TILESIZE + 250, 275))
      DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.champions) if country_known else "?", True, (0,0,0)), (map.WIDTH * TILESIZE + 250, 300))
      
      # Country bonuses
      DISPLAYSURF.blit(COUNTRY_FONT.render("Attack Bonus: " + (str(map.d_continents[current_tile[0]][current_tile[1]].attack_bonus) + "%" if country_known else "?"), True, ATTACK_COLOR), (map.WIDTH * TILESIZE + 100, 350))
      DISPLAYSURF.blit(COUNTRY_FONT.render("Defense Bonus: " + (str(map.d_continents[current_tile[0]][current_tile[1]].defense_bonus) + "%" if country_known else "?"), True, DEFEND_COLOR), (map.WIDTH * TILESIZE + 100, 375))
      
      # Owner
      DISPLAYSURF.blit(COUNTRY_FONT.render("Owner: " + (str(map.d_continents[current_tile[0]][current_tile[1]].owner) if country_known else "?"), True, l_playerColors[d_playerLogoIndexes[map.d_continents[current_tile[0]][current_tile[1]].owner]] if country_known else (0,0,0)), (map.WIDTH * TILESIZE + 100, 425))
         
      DISPLAYSURF.blit(CONTINENT_FONT.render("Continent Bonus: $" + str(map.d_bonuses[current_tile[0]]), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 500))
   else:
      x_offset = 120
      y_offset = 180
      DISPLAYSURF.blit(CONTINENT_FONT.render("Leaderboard:", True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 130))
      l_place = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th"]
      place_index = 0
      for name in map.l_player_names:
         playerName = COUNTRY_FONT.render(l_place[place_index] + ": " + name, True, l_playerColors[d_playerLogoIndexes[name]])
         DISPLAYSURF.blit(playerName, (map.WIDTH * TILESIZE + x_offset, y_offset))
         place_index += 1
         if params != None and name not in params[0]:
            pygame.draw.line(DISPLAYSURF, l_playerColors[d_playerLogoIndexes[name]], (map.WIDTH * TILESIZE + x_offset, y_offset + 17), (map.WIDTH * TILESIZE + x_offset + playerName.get_width(), y_offset + 17), 2)
         y_offset += 25
      y_offset += 25
      DISPLAYSURF.blit(CONTINENT_FONT.render("Continent Bonuses:", True, (0,0,0)), (map.WIDTH * TILESIZE + 100, y_offset))
      y_offset += 20
      for continent_name in map.l_continent_names:
         y_offset += 25
         DISPLAYSURF.blit(COUNTRY_FONT.render(continent_name + ": $" + str(map.d_bonuses[continent_name]), True, (0,0,0)), (map.WIDTH * TILESIZE + x_offset, y_offset))

def selectedInfo(map, DISPLAYSURF, params):
   current_tile = map.ll_map[params[1]][params[0]]
    
   DISPLAYSURF.blit(CONTINENT_FONT.render("Continent: " + current_tile[0], True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 120))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Country: " + map.d_continents[current_tile[0]][current_tile[1]].name, True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 170))

   # Unit counts by type
   DISPLAYSURF.blit(COUNTRY_FONT.render("Pistoleers:", True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 225))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Musketeers:", True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 250))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Cannons:", True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 275))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Airships:", True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 300))
   
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.infantry), True, (0,0,0)), (map.WIDTH * TILESIZE + 250, 225))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.archers), True, (0,0,0)), (map.WIDTH * TILESIZE + 250, 250))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.cannons), True, (0,0,0)), (map.WIDTH * TILESIZE + 250, 275))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.champions), True, (0,0,0)), (map.WIDTH * TILESIZE + 250, 300))
    
   # Country bonuses
   DISPLAYSURF.blit(COUNTRY_FONT.render("Attack Bonus: " + str(map.d_continents[current_tile[0]][current_tile[1]].attack_bonus) + "%" , True, ATTACK_COLOR), (map.WIDTH * TILESIZE + 100, 350))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Defense Bonus: " + str(map.d_continents[current_tile[0]][current_tile[1]].defense_bonus) + "%", True, DEFEND_COLOR), (map.WIDTH * TILESIZE + 100, 375))
    
   # Owner
   DISPLAYSURF.blit(COUNTRY_FONT.render("Owner: " + map.d_continents[current_tile[0]][current_tile[1]].owner, True, l_playerColors[d_playerLogoIndexes[map.d_continents[current_tile[0]][current_tile[1]].owner]]), (map.WIDTH * TILESIZE + 100, 425))
    
   DISPLAYSURF.blit(CONTINENT_FONT.render("Continent Bonus: $" + str(map.d_bonuses[current_tile[0]]), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 500))
    
def attackInfo(map, DISPLAYSURF, params):
   attacker = map.ll_map[params[0][1]][params[0][0]]
   defender = params[1][0]
   attackerUnits = params[1][1]
   
   DISPLAYSURF.blit(COUNTRY_FONT.render(map.d_continents[attacker[0]][attacker[1]].name, True, ATTACK_COLOR), (map.WIDTH * TILESIZE + 100, 125))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Attacking", True, (0,0,0)), (map.WIDTH * TILESIZE + 120, 165))
   DISPLAYSURF.blit(COUNTRY_FONT.render(map.d_continents[defender[0]][defender[1]].name, True, DEFEND_COLOR), (map.WIDTH * TILESIZE + 140, 205))
   
   DISPLAYSURF.blit(COUNTRY_FONT.render("Attacker", True, ATTACK_COLOR), (map.WIDTH * TILESIZE + 210, 275))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Defender", True, DEFEND_COLOR), (map.WIDTH * TILESIZE + 360, 275))
   
   DISPLAYSURF.blit(COUNTRY_FONT.render("Pistoleers:", True, (0,0,0)), (map.WIDTH * TILESIZE + 75, 325))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Musketeers:", True, (0,0,0)), (map.WIDTH * TILESIZE + 75, 375))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Cannons:", True, (0,0,0)), (map.WIDTH * TILESIZE + 75, 425))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Airships:", True, (0,0,0)), (map.WIDTH * TILESIZE + 75, 475))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Bonus:", True, (0,0,0)), (map.WIDTH * TILESIZE + 75, 525))
   
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(attackerUnits.infantry) + "/" + str(map.d_continents[attacker[0]][attacker[1]].unit_counts.infantry), True, ATTACK_COLOR), (map.WIDTH * TILESIZE + 250, 325))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(attackerUnits.archers) + "/" + str(map.d_continents[attacker[0]][attacker[1]].unit_counts.archers), True, ATTACK_COLOR), (map.WIDTH * TILESIZE + 250, 375))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(attackerUnits.cannons) + "/" + str(map.d_continents[attacker[0]][attacker[1]].unit_counts.cannons), True, ATTACK_COLOR), (map.WIDTH * TILESIZE + 250, 425))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(attackerUnits.champions) + "/" + str(map.d_continents[attacker[0]][attacker[1]].unit_counts.champions), True, ATTACK_COLOR), (map.WIDTH * TILESIZE + 250, 475))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[attacker[0]][attacker[1]].attack_bonus) + "%", True, ATTACK_COLOR), (map.WIDTH * TILESIZE + 250, 525))
   
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[defender[0]][defender[1]].unit_counts.infantry), True, DEFEND_COLOR), (map.WIDTH * TILESIZE + 400, 325))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[defender[0]][defender[1]].unit_counts.archers), True, DEFEND_COLOR), (map.WIDTH * TILESIZE + 400, 375))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[defender[0]][defender[1]].unit_counts.cannons), True, DEFEND_COLOR), (map.WIDTH * TILESIZE + 400, 425))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[defender[0]][defender[1]].unit_counts.champions), True, DEFEND_COLOR), (map.WIDTH * TILESIZE + 400, 475))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[defender[0]][defender[1]].defense_bonus) + "%", True, DEFEND_COLOR), (map.WIDTH * TILESIZE + 400, 525))
   
def moveInfo(map, DISPLAYSURF, params):
   attacker = map.ll_map[params[0][1]][params[0][0]]
   defender = params[1][0]
   attackerUnits = params[1][1]
   
   DISPLAYSURF.blit(COUNTRY_FONT.render("From " + map.d_continents[attacker[0]][attacker[1]].name, True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 125))
   DISPLAYSURF.blit(COUNTRY_FONT.render("To " + map.d_continents[defender[0]][defender[1]].name, True, (0,0,0)), (map.WIDTH * TILESIZE + 120, 165))
   
   DISPLAYSURF.blit(COUNTRY_FONT.render("Source", True, (0,0,0)), (map.WIDTH * TILESIZE + 210, 275))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Destination", True, (0,0,0)), (map.WIDTH * TILESIZE + 360, 275))
   
   DISPLAYSURF.blit(COUNTRY_FONT.render("Pistoleers:", True, (0,0,0)), (map.WIDTH * TILESIZE + 75, 325))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Musketeers:", True, (0,0,0)), (map.WIDTH * TILESIZE + 75, 375))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Cannons:", True, (0,0,0)), (map.WIDTH * TILESIZE + 75, 425))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Airships:", True, (0,0,0)), (map.WIDTH * TILESIZE + 75, 475))
   
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(attackerUnits.infantry) + "/" + str(map.d_continents[attacker[0]][attacker[1]].unit_counts.infantry), True, (0,0,0)), (map.WIDTH * TILESIZE + 250, 325))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(attackerUnits.archers) + "/" + str(map.d_continents[attacker[0]][attacker[1]].unit_counts.archers), True, (0,0,0)), (map.WIDTH * TILESIZE + 250, 375))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(attackerUnits.cannons) + "/" + str(map.d_continents[attacker[0]][attacker[1]].unit_counts.cannons), True, (0,0,0)), (map.WIDTH * TILESIZE + 250, 425))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(attackerUnits.champions) + "/" + str(map.d_continents[attacker[0]][attacker[1]].unit_counts.champions), True, (0,0,0)), (map.WIDTH * TILESIZE + 250, 475))
   
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[defender[0]][defender[1]].unit_counts.infantry), True, (0,0,0)), (map.WIDTH * TILESIZE + 400, 325))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[defender[0]][defender[1]].unit_counts.archers), True, (0,0,0)), (map.WIDTH * TILESIZE + 400, 375))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[defender[0]][defender[1]].unit_counts.cannons), True, (0,0,0)), (map.WIDTH * TILESIZE + 400, 425))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[defender[0]][defender[1]].unit_counts.champions), True, (0,0,0)), (map.WIDTH * TILESIZE + 400, 475))
   
def battleInfo(map, DISPLAYSURF, params):
   attacker = map.ll_map[params[0][1]][params[0][0]]
   defender = params[1][0]
   attackerUnits = params[1][1]
   
   DISPLAYSURF.blit(COUNTRY_FONT.render(map.d_continents[attacker[0]][attacker[1]].name, True, ATTACK_COLOR), (map.WIDTH * TILESIZE + 100, 125))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Attacking", True, (0,0,0)), (map.WIDTH * TILESIZE + 120, 165))
   DISPLAYSURF.blit(COUNTRY_FONT.render(map.d_continents[defender[0]][defender[1]].name, True, DEFEND_COLOR), (map.WIDTH * TILESIZE + 140, 205))
   
   DISPLAYSURF.blit(COUNTRY_FONT.render("Attacker", True, ATTACK_COLOR), (map.WIDTH * TILESIZE + 210, 275))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Defender", True, DEFEND_COLOR), (map.WIDTH * TILESIZE + 360, 275))
   
   DISPLAYSURF.blit(COUNTRY_FONT.render("Pistoleers:", True, (0,0,0)), (map.WIDTH * TILESIZE + 75, 325))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Musketeers:", True, (0,0,0)), (map.WIDTH * TILESIZE + 75, 375))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Cannons:", True, (0,0,0)), (map.WIDTH * TILESIZE + 75, 425))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Airships:", True, (0,0,0)), (map.WIDTH * TILESIZE + 75, 475))
   
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(attackerUnits.infantry), True, ATTACK_COLOR), (map.WIDTH * TILESIZE + 250, 325))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(attackerUnits.archers), True, ATTACK_COLOR), (map.WIDTH * TILESIZE + 250, 375))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(attackerUnits.cannons), True, ATTACK_COLOR), (map.WIDTH * TILESIZE + 250, 425))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(attackerUnits.champions), True, ATTACK_COLOR), (map.WIDTH * TILESIZE + 250, 475))
   
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[defender[0]][defender[1]].unit_counts.infantry), True, DEFEND_COLOR), (map.WIDTH * TILESIZE + 400, 325))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[defender[0]][defender[1]].unit_counts.archers), True, DEFEND_COLOR), (map.WIDTH * TILESIZE + 400, 375))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[defender[0]][defender[1]].unit_counts.cannons), True, DEFEND_COLOR), (map.WIDTH * TILESIZE + 400, 425))
   DISPLAYSURF.blit(COUNTRY_FONT.render(str(map.d_continents[defender[0]][defender[1]].unit_counts.champions), True, DEFEND_COLOR), (map.WIDTH * TILESIZE + 400, 475))
    
def printMap(map, DISPLAYSURF, gameStage, infoDisplay, params=None):

   DISPLAYSURF.blit(backgroundSurface, (0, 0))
   
   #loop through each row
   for row in range(map.HEIGHT):
      #loop through each column in the row
      for column in range(map.WIDTH):
         #draw the resource at that position in the tilemap, using the correct colour
         if (map.ll_map[row][column] != WATER):
            current_country = map.d_continents[map.ll_map[row][column][0]][map.ll_map[row][column][1]]
            if current_country.owner != None:
               DISPLAYSURF.blit(l_playerLogos[d_playerLogoIndexes[current_country.owner]], (((column) % map.WIDTH) * TILESIZE, ((row) % map.HEIGHT) * TILESIZE))
               count = str(current_country.unit_counts.getSummaryCount())
               DISPLAYSURF.blit(UNIT_FONT.render(count, True, (0,0,0)), (((column) % map.WIDTH) * TILESIZE + 45 - len(count) * 7, ((row) % map.HEIGHT) * TILESIZE + 25))

   
   DISPLAYSURF.blit(source=GAME_STAGE_FONT.render(gameStage, True, (0,0,0)), dest=(map.WIDTH * TILESIZE + 100, 50))

   infoDisplay(map, DISPLAYSURF, params)

   DISPLAYSURF.blit(source=INFO_OVERLAY, dest=(map.WIDTH * TILESIZE, 0), special_flags=BLEND_RGBA_ADD)

def prepareBackground(map, DISPLAYSURF):
   global backgroundSurface
   #loop through each row
   for row in range(map.HEIGHT):
      #loop through each column in the row
      for column in range(map.WIDTH):
         #draw the resource at that position in the tilemap, using the correct colour
         if (map.ll_map[row][column] != WATER):
            DISPLAYSURF.blit(textures[d_continent_tiles[map.ll_map[row][column][0]]], (((column) % map.WIDTH) * TILESIZE, ((row) % map.HEIGHT) * TILESIZE))
  
    #loop through each row
   for row in range(map.HEIGHT):
      #loop through each column in the row
      for column in range(map.WIDTH):
         #draw the resource at that position in the tilemap, using the correct colour
         if (map.ll_map[row][column] == WATER):
            DISPLAYSURF.blit(t_WATER_OUTLINES[map.ll_water_mask[row][column]], (((column) % map.WIDTH) * TILESIZE - MARGIN, ((row) % map.HEIGHT) * TILESIZE - MARGIN))
          
    #loop through each row
   for row in range(map.HEIGHT):
      #loop through each column in the row
      for column in range(map.WIDTH):
         #draw the resource at that position in the tilemap, using the correct colour
         if (map.ll_map[row][column] == WATER):
            DISPLAYSURF.blit(t_WATER_TEXTURES[map.ll_water_mask[row][column]], (((column) % map.WIDTH) * TILESIZE - MARGIN, ((row) % map.HEIGHT) * TILESIZE - MARGIN))

   DISPLAYSURF.blit(source=textures[OVERLAY], dest=(0,0), special_flags=BLEND_MULT)
   DISPLAYSURF.blit(MAP_FRAME, dest=(0,0))
   DISPLAYSURF.blit(MAP_LIGHT, dest=(0,0), special_flags=BLEND_ADD)
   
   DISPLAYSURF.blit(source=INFO_MARQUEE, dest=(map.WIDTH * TILESIZE, 0))
   pygame.draw.line(DISPLAYSURF, (0,0,0), (map.WIDTH * TILESIZE + 28, 112), (map.WIDTH * TILESIZE + 700, 112), 3)
   DISPLAYSURF.blit(source=BASE_BOARD, dest=(0, map.HEIGHT * TILESIZE))
   DISPLAYSURF.blit(GAME_CLOSE, (1560,0))
   DISPLAYSURF.blit(GAME_MINIM, (1520,0))
   
   backgroundSurface = copy.copy(DISPLAYSURF)
   backgroundSurface = backgroundSurface.convert_alpha()
   
def handleGeneral(event, map, temp_map=None, selectedCountry=None):
   global map_X_offset
   global map_Y_offset
   global song_index
   if event.type == QUIT:
      #and the game and close the window
      pygame.quit()
      sys.exit()
         
   if event.type == MOUSEBUTTONDOWN:
      curr_x, curr_y = pygame.mouse.get_pos()
      curr_x *= xScale
      curr_y *= yScale
      if 1520 < curr_x < 1556 and 0 < curr_y < 20:
         pygame.display.iconify()
      if 1560 < curr_x < 1596 and 0 < curr_y < 20:
         return True
   try:
      if event.type == SONG_END:
         song_index = (song_index + 1) % len(l_songs)
         pygame.mixer.music.load(SOUND_FILE_PATH + l_songs[song_index])
         pygame.mixer.music.play(1)
   except:
      pass
      
   return False

def displayMessage(image, map, DISPLAYSURF, turnState, l_playerNames, d_playerCountries, battles = None):
   OK_COORDS = (450,650)
   clickedOK = False
   
   while not clickedOK:
      curr_x, curr_y = pygame.mouse.get_pos()
      curr_x *= xScale
      curr_y *= yScale
      over_ok = OK_COORDS[0] <= curr_x <= OK_COORDS[0] + 200 and OK_COORDS[1] <= curr_y <= OK_COORDS[1] + 100
      for event in pygame.event.get():
         handleGeneral(event, map)
         if over_ok and event.type == MOUSEBUTTONDOWN:
            clickedOK = True
      printMap(map, DISPLAYSURF, turnState, standardInfo, (l_playerNames, d_playerCountries))
      DISPLAYSURF.blit(image, (0, 0))
      if battles != None:
         DISPLAYSURF.blit(COUNTRY_FONT.render("Countries Conquered", True, VICTOR_COLOR),(150,140))
         DISPLAYSURF.blit(COUNTRY_FONT.render("Countries Lost", True, DEFEND_COLOR),(435,140))
         DISPLAYSURF.blit(COUNTRY_FONT.render("Attacks Failed", True, ATTACK_COLOR),(650,140))
         pygame.draw.line(DISPLAYSURF, (0,0,0), (150, 170), (850, 170), 3)
         y_offset = 30
         for countryConquered in battles[0]:
            DISPLAYSURF.blit(TURN_READOUT_FONT.render(countryConquered, True, VICTOR_COLOR),(150,140 + y_offset))
            y_offset += 25
         y_offset = 30
         for countryLost in battles[1]:
            DISPLAYSURF.blit(TURN_READOUT_FONT.render(countryLost, True, DEFEND_COLOR),(435,140 + y_offset))
            y_offset += 25
         y_offset = 30
         for attackLost in battles[2]:
            DISPLAYSURF.blit(TURN_READOUT_FONT.render(attackLost, True, ATTACK_COLOR),(650,140 + y_offset))
            y_offset += 30
      DISPLAYSURF.blit(OK_LIT if over_ok else OK_UNLIT, OK_COORDS)
      DISPLAYSURF.blit(MOUSE_LIT if over_ok else MOUSE_UNLIT, (curr_x, curr_y))
      newSurface = pygame.transform.scale(DISPLAYSURF,(screenInfo.current_w, screenInfo.current_h), window)
      pygame.display.update()

def placeUnits(DISPLAYSURF, map, player, socket, host_address, l_playerNames, d_playerCountries):
   BUY_PISTOLEERS = pygame.image.load(IMAGE_FILE_PATH + "PistoleersBuy.png")
   BUY_MUSKETEERS = pygame.image.load(IMAGE_FILE_PATH + "MusketeersBuy.png")
   BUY_CANNONS = pygame.image.load(IMAGE_FILE_PATH + "CannonBuy.png")
   BUY_AIRSHIPS = pygame.image.load(IMAGE_FILE_PATH + "AirshipBuy.png")
   MONEY_SCREEN = pygame.image.load(IMAGE_FILE_PATH + "MoneyScreen.png")
   DONE_BUTTON = pygame.image.load(IMAGE_FILE_PATH + "DoneButton.png")
   DONE_BUTTON_ACTIVE = pygame.image.load(IMAGE_FILE_PATH + "DoneButtonActive.png")
   placing = True
   selectedCountry = None
   temp_map = Map(map_to_copy=map, copy_player_name=player.user_name)
   while placing:
       #get all the user events
       curr_x, curr_y = pygame.mouse.get_pos()
       curr_x *= xScale
       curr_y *= yScale
       for event in pygame.event.get():
           #if the user wants to quit
           if handleGeneral(event, map, temp_map, selectedCountry):
             return None
           if event.type == MOUSEBUTTONDOWN:
             if curr_x < map.WIDTH * TILESIZE and curr_y < map.HEIGHT * TILESIZE:
                curr_country = map.ll_map[int(curr_y / TILESIZE)][int(curr_x / TILESIZE)] #Continent name and country index
                if (curr_country != map.WATER and map.d_continents[curr_country[0]][curr_country[1]].owner == map.current_player):
                  if map.d_continents[curr_country[0]][curr_country[1]].owner == player.user_name and selectedCountry != [int(curr_x / TILESIZE), int(curr_y / TILESIZE)]:
                     selectedCountry = [int(curr_x / TILESIZE), int(curr_y / TILESIZE)] #Coordinates of the current selected country
                  else:
                     selectedCountry = None
                else:
                  selectedCountry = None
             elif selectedCountry != None:
                curr_country = map.ll_map[selectedCountry[1]][selectedCountry[0]]
                
                #Pistoleers
                if 175 + 245 <= curr_x <= 175 + 295 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120: # "All" for Pistoleers
                  map.d_continents[curr_country[0]][curr_country[1]].unit_counts.infantry += player.unit_counts
                  player.unit_counts = 0
                elif 175 + 295 <= curr_x <= 175 + 345 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120 and player.unit_counts > 0: # "+" for Pistoleers
                  map.d_continents[curr_country[0]][curr_country[1]].unit_counts.infantry += 1
                  player.unit_counts -= 1
                elif 175 + 345 <= curr_x <= 175 + 395 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120: # "-" for Pistoleers
                  if map.d_continents[curr_country[0]][curr_country[1]].unit_counts.infantry > temp_map.d_continents[curr_country[0]][curr_country[1]].unit_counts.infantry:
                     map.d_continents[curr_country[0]][curr_country[1]].unit_counts.infantry -= 1
                     player.unit_counts += 1
                
                #Musketeers
                if 580 + 245 <= curr_x <= 580 + 295 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120: # "All" for Musketeers
                  map.d_continents[curr_country[0]][curr_country[1]].unit_counts.archers += int(player.unit_counts / 2)
                  player.unit_counts = player.unit_counts % 2
                elif 580 + 295 <= curr_x <= 580 + 345 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120 and player.unit_counts > 1: # "+" for Musketeers
                  map.d_continents[curr_country[0]][curr_country[1]].unit_counts.archers += 1
                  player.unit_counts -= 2
                elif 580 + 345 <= curr_x <= 580 + 395 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120: # "-" for Musketeers
                  if map.d_continents[curr_country[0]][curr_country[1]].unit_counts.archers > temp_map.d_continents[curr_country[0]][curr_country[1]].unit_counts.archers:
                     map.d_continents[curr_country[0]][curr_country[1]].unit_counts.archers -= 1
                     player.unit_counts += 2
                     
                #Cannons
                if 175 + 245 <= curr_x <= 175 + 295 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175: # "All" for Cannons
                  map.d_continents[curr_country[0]][curr_country[1]].unit_counts.cannons += int(player.unit_counts / 2)
                  player.unit_counts = player.unit_counts % 2
                elif 175 + 295 <= curr_x <= 175 + 345 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175 and player.unit_counts > 1: # "+" for Cannons
                  map.d_continents[curr_country[0]][curr_country[1]].unit_counts.cannons += 1
                  player.unit_counts -= 2
                elif 175 + 345 <= curr_x <= 175 + 395 and map.HEIGHT * TILESIZE + 125 < curr_y <= map.HEIGHT * TILESIZE + 175: # "-" for Cannons
                  if map.d_continents[curr_country[0]][curr_country[1]].unit_counts.cannons > temp_map.d_continents[curr_country[0]][curr_country[1]].unit_counts.cannons:
                     map.d_continents[curr_country[0]][curr_country[1]].unit_counts.cannons -= 1
                     player.unit_counts += 2
                     
                #Airships
                if 580 + 245 <= curr_x <= 580 + 295 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175: # "All" for Airships
                  map.d_continents[curr_country[0]][curr_country[1]].unit_counts.champions += int(player.unit_counts / 5)
                  player.unit_counts = player.unit_counts % 5
                elif 580 + 295 <= curr_x <= 580 + 345 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175 and player.unit_counts > 4: # "+" for Airships
                  map.d_continents[curr_country[0]][curr_country[1]].unit_counts.champions += 1
                  player.unit_counts -= 5
                elif 580 + 345 <= curr_x <= 580 + 395 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175: # "-" for Airships
                  if map.d_continents[curr_country[0]][curr_country[1]].unit_counts.champions > temp_map.d_continents[curr_country[0]][curr_country[1]].unit_counts.champions:
                     map.d_continents[curr_country[0]][curr_country[1]].unit_counts.champions -= 1
                     player.unit_counts += 5
                     
             #Done
             if 980 <= curr_x <= 1080 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 175 and player.unit_counts == 0:
               update_map = pickle.dumps((map, player))
               try:
                  socket.sendto(update_map, host_address)
               except:
                  displayMessage(CRASH_MESSAGE, map, DISPLAYSURF, "Place Troops", l_playerNames, d_playerCountries)
                  return None
               placing = False
       
       if selectedCountry == None:
         printMap(map, DISPLAYSURF, "Place Troops", standardInfo, (l_playerNames, d_playerCountries))
       else:
         printMap(map, DISPLAYSURF, "Place Troops", selectedInfo, selectedCountry)
       
       if selectedCountry != None:
         DISPLAYSURF.blit(SELECTED_TILE, (selectedCountry[0] * TILESIZE, selectedCountry[1] * TILESIZE), special_flags=BLEND_ADD)
       
       DISPLAYSURF.blit(MONEY_SCREEN, (70, map.HEIGHT * TILESIZE + 70))
       DISPLAYSURF.blit(MONEY_FONT.render(str(player.unit_counts), True, (255, 0, 0)), (95, map.HEIGHT * TILESIZE + 103))
       DISPLAYSURF.blit(BUY_PISTOLEERS, (170, map.HEIGHT * TILESIZE + 70))
       DISPLAYSURF.blit(BUY_MUSKETEERS, (575, map.HEIGHT * TILESIZE + 70))
       DISPLAYSURF.blit(BUY_CANNONS, (170, map.HEIGHT * TILESIZE + 125))
       DISPLAYSURF.blit(BUY_AIRSHIPS, (575, map.HEIGHT * TILESIZE + 125))
       DISPLAYSURF.blit(DONE_BUTTON if player.unit_counts > 0 else DONE_BUTTON_ACTIVE, (980, map.HEIGHT * TILESIZE + 70))
       
       blitInfo(DISPLAYSURF, map, INFO_BUY_UNITS)
       DISPLAYSURF.blit(MOUSE_LIT if isOverButton(map, curr_x, curr_y) and selectedCountry != None else MOUSE_UNLIT, (curr_x, curr_y))
       
       #update the display
       newSurface = pygame.transform.scale(DISPLAYSURF,(screenInfo.current_w, screenInfo.current_h), window)
       pygame.display.update()
   return map
refreshing = True
oldMap = None

def declareAttacks(DISPLAYSURF, map, player, socket, host_address, l_playerNames, d_playerCountries):
   global refreshing
   refreshing = True
   def refresh():
      global refreshing
      global oldMap
      try:
         response = socket.recv(16384)
         socket.settimeout(0.2)
         try:
            response += socket.recv(16384)
            print("Wow, we actually got extra data")
         except:
            pass
         socket.settimeout(None)
         try:
            oldMap = pickle.loads(response)
         except:
            print("(declareAttacks) Packet was: " + str(response))
            oldMap = None
      except:
         oldMap = None
         refreshing = False
         return

      refreshing = False
      print("set refreshing to false")
      return
      
   t_updateScreen = threading.Thread(target=refresh)
   t_updateScreen.daemon = True
   t_updateScreen.start()
   
   while refreshing:
      for event in pygame.event.get():
         #if the user wants to quit
         if handleGeneral(event, map):
            return None, None, None, None
            
      printMap(map, DISPLAYSURF, "Declare Attacks", standardInfo, (l_playerNames, d_playerCountries))
      DISPLAYSURF.blit(WAITING, (70, map.HEIGHT * TILESIZE + 70))
      curr_x, curr_y = pygame.mouse.get_pos()
      curr_x *= xScale
      curr_y *= yScale
      DISPLAYSURF.blit(MOUSE_UNLIT, (curr_x, curr_y))
      #update the display
      newSurface = pygame.transform.scale(DISPLAYSURF,(screenInfo.current_w, screenInfo.current_h), window)
      pygame.display.update()
   print("Exited refreshing")
   if oldMap != None:
      map = oldMap[0]
   else:
      displayMessage(CRASH_MESSAGE, map, DISPLAYSURF, "Declare Attacks", l_playerNames, d_playerCountries)
      return None, None, None, None
   declaring = True
   if detectGameEnd(DISPLAYSURF, map, player, socket, oldMap[1], oldMap[2]):
      return None, None, None, None
   print("I have the map!")
   
   selectedCountry = None
   l_neighbors = []
   d_attacks = {}
   l_attackers = []
   l_defenders = []
   
   while declaring:
       squishyEasterEgg = False
       #get all the user events
       curr_x, curr_y = pygame.mouse.get_pos()
       curr_x *= xScale
       curr_y *= yScale
       for event in pygame.event.get():
           #if the user wants to quit
           if handleGeneral(event, map, selectedCountry=selectedCountry):
             return None, None, None, None
           
           if event.type == MOUSEBUTTONDOWN:
             if curr_x < map.WIDTH * TILESIZE and curr_y < map.HEIGHT * TILESIZE: # if the user clicked on the map
                curr_country = map.ll_map[int(curr_y / TILESIZE)][int(curr_x / TILESIZE)]

                if (curr_country != map.WATER): # if the user did not click water
                  if map.d_continents[curr_country[0]][curr_country[1]].owner == player.user_name and selectedCountry != [int(curr_x / TILESIZE), int(curr_y / TILESIZE)]: # if the user clicked his own country and not a selected country
                     l_neighbors = []
                     selectedCountry = [int(curr_x / TILESIZE), int(curr_y / TILESIZE)]
                  elif [int(curr_x / TILESIZE), int(curr_y / TILESIZE)] != selectedCountry and selectedCountry != None: # if not clicking your selected country and there is a selected country
                     if not ([selectedCountry[0], selectedCountry[1]] in l_attackers) and [int(curr_x / TILESIZE), int(curr_y / TILESIZE)] in l_neighbors: # if selected country is not attacking and clicking neighboring country
                        l_attackers.append([selectedCountry[0], selectedCountry[1]])
                        l_defenders.append([int(curr_x / TILESIZE), int(curr_y / TILESIZE)])
                        d_attacks[map.ll_map[selectedCountry[1]][selectedCountry[0]]] = [curr_country, UnitCounts(0, 0, 0, 0), False, player.user_name] #[defender, attack force]
                     elif [int(curr_x / TILESIZE), int(curr_y / TILESIZE)] in l_defenders and selectedCountry in l_attackers: # if clicking the country your selected country is attacking
                        index = l_attackers.index(selectedCountry)
                        if l_defenders[index] == [int(curr_x / TILESIZE), int(curr_y / TILESIZE)] and l_attackers[index] == selectedCountry:
                           del l_defenders[index]
                           l_attackers.remove([selectedCountry[0], selectedCountry[1]])
                           d_attacks[map.ll_map[selectedCountry[1]][selectedCountry[0]]] = None
                     else:
                        selectedCountry = None
                  else:
                     selectedCountry = None
                else:
                  selectedCountry = None
             elif selectedCountry != None:
                curr_country = map.ll_map[selectedCountry[1]][selectedCountry[0]]
                units = map.d_continents[curr_country[0]][curr_country[1]].unit_counts
                if selectedCountry in l_attackers:
                  attacker = d_attacks[map.ll_map[selectedCountry[1]][selectedCountry[0]]]
                  #Pistoleers
                  if 175 + 245 <= curr_x <= 175 + 295 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120: # "All" for Pistoleers
                     attacker[1].infantry = units.infantry
                  elif 175 + 295 <= curr_x <= 175 + 345 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120 and \
                        attacker[1].infantry < units.infantry: # "+" for Pistoleers
                     attacker[1].infantry += 1
                  elif 175 + 345 <= curr_x <= 175 + 395 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120: # "-" for Pistoleers
                     if attacker[1].infantry > 0:
                        attacker[1].infantry -= 1
                        
                  #Musketeers
                  if 580 + 245 <= curr_x <= 580 + 295 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120: # "All" for Musketeers
                     attacker[1].archers = units.archers
                  elif 580 + 295 <= curr_x <= 580 + 345 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120 and \
                        attacker[1].archers < units.archers:# "+" for Musketeers
                     attacker[1].archers += 1
                  elif 580 + 345 <= curr_x <= 580 + 395 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120: # "-" for Musketeers
                     if attacker[1].archers > 0:
                        attacker[1].archers -= 1
                        
                   #Cannons
                  if 175 + 245 <= curr_x <= 175 + 295 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175: # "All" for Cannons
                     attacker[1].cannons = units.cannons
                  elif 175 + 295 <= curr_x <= 175 + 345 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175 and \
                        attacker[1].cannons < units.cannons: # "+" for Cannons
                     attacker[1].cannons += 1
                  elif 175 + 345 <= curr_x <= 175 + 395 and map.HEIGHT * TILESIZE + 125 < curr_y <= map.HEIGHT * TILESIZE + 175: # "-" for Cannons
                     if attacker[1].cannons > 0:
                        attacker[1].cannons -= 1
                        
                  #Airships
                  if 580 + 245 <= curr_x <= 580 + 295 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175: # "All" for Airships
                     attacker[1].champions = units.champions
                  elif 580 + 295 <= curr_x <= 580 + 345 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175 and \
                        attacker[1].champions < units.champions: # "+" for Airships
                     attacker[1].champions += 1
                  elif 580 + 345 <= curr_x <= 580 + 395 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175: # "-" for Airships
                     if attacker[1].champions > 0:
                        attacker[1].champions -= 1
             #Done
             if 980 <= curr_x <= 1080 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 175 and player.unit_counts == 0:
               packet = pickle.dumps((l_attackers, l_defenders, d_attacks, player))
               try:
                  socket.sendto(packet, host_address)
               except:
                  displayMessage(CRASH_MESSAGE, map, DISPLAYSURF, "Declare Attacks", l_playerNames, d_playerCountries)
                  return None, None, None, None
               declaring = False
       
       if selectedCountry == None:
         printMap(map, DISPLAYSURF, "Declare Attacks", standardInfo, (oldMap[1], oldMap[2]))
       else:
         if [selectedCountry[0], selectedCountry[1]] in l_attackers:
            printMap(map,  DISPLAYSURF, "Declare Attacks", attackInfo, (selectedCountry, d_attacks[map.ll_map[selectedCountry[1]][selectedCountry[0]]]))
            squishyEasterEgg = True
         else:
            printMap(map, DISPLAYSURF, "Declare Attacks", selectedInfo, selectedCountry)
       
       if selectedCountry != None:
         DISPLAYSURF.blit(SELECTED_TILE, (selectedCountry[0] * TILESIZE, selectedCountry[1] * TILESIZE), special_flags=BLEND_ADD)
       
       if selectedCountry != None and not (selectedCountry in l_attackers):

         current_tile = map.ll_map[(selectedCountry[1] + 1) % map.HEIGHT][(selectedCountry[0] + 1) % map.WIDTH]
         if (False if current_tile == map.WATER else map.d_continents[current_tile[0]][current_tile[1]].owner != player.user_name):
            DISPLAYSURF.blit(ATTACK_OPTION, (((selectedCountry[0] + 1) % map.WIDTH) * TILESIZE, ((selectedCountry[1] + 1) % map.HEIGHT) * TILESIZE), special_flags=BLEND_ADD)
            l_neighbors.append([(selectedCountry[0] + 1) % map.WIDTH, (selectedCountry[1] + 1) % map.HEIGHT])
            
         current_tile = map.ll_map[(selectedCountry[1] - 1) % map.HEIGHT][(selectedCountry[0] + 1) % map.WIDTH]
         if (False if current_tile == map.WATER else map.d_continents[current_tile[0]][current_tile[1]].owner != player.user_name):
            DISPLAYSURF.blit(ATTACK_OPTION, (((selectedCountry[0] + 1) % map.WIDTH) * TILESIZE, ((selectedCountry[1] - 1) % map.HEIGHT) * TILESIZE), special_flags=BLEND_ADD)
            l_neighbors.append([(selectedCountry[0] + 1) % map.WIDTH, (selectedCountry[1] - 1) % map.HEIGHT])
            
         current_tile = map.ll_map[(selectedCountry[1]) % map.HEIGHT][(selectedCountry[0] + 1) % map.WIDTH]
         if (False if current_tile == map.WATER else map.d_continents[current_tile[0]][current_tile[1]].owner != player.user_name):
            DISPLAYSURF.blit(ATTACK_OPTION, (((selectedCountry[0] + 1) % map.WIDTH) * TILESIZE, (selectedCountry[1]) * TILESIZE), special_flags=BLEND_ADD)
            l_neighbors.append([(selectedCountry[0] + 1) % map.WIDTH, (selectedCountry[1])])
            
         current_tile = map.ll_map[(selectedCountry[1] + 1) % map.HEIGHT][(selectedCountry[0] - 1) % map.WIDTH]
         if (False if current_tile == map.WATER else map.d_continents[current_tile[0]][current_tile[1]].owner != player.user_name):
            DISPLAYSURF.blit(ATTACK_OPTION, (((selectedCountry[0] - 1) % map.WIDTH) * TILESIZE, ((selectedCountry[1] + 1) % map.HEIGHT) * TILESIZE), special_flags=BLEND_ADD)
            l_neighbors.append([(selectedCountry[0] - 1) % map.WIDTH, (selectedCountry[1] + 1) % map.HEIGHT])
            
         current_tile = map.ll_map[(selectedCountry[1] - 1) % map.HEIGHT][(selectedCountry[0] - 1) % map.WIDTH]
         if (False if current_tile == map.WATER else map.d_continents[current_tile[0]][current_tile[1]].owner != player.user_name):
            DISPLAYSURF.blit(ATTACK_OPTION, (((selectedCountry[0] - 1) % map.WIDTH) * TILESIZE, ((selectedCountry[1] - 1) % map.HEIGHT) * TILESIZE), special_flags=BLEND_ADD)
            l_neighbors.append([(selectedCountry[0] - 1) % map.WIDTH, (selectedCountry[1] - 1) % map.HEIGHT])
            
         current_tile = map.ll_map[selectedCountry[1]][(selectedCountry[0] - 1) % map.WIDTH]
         if (False if current_tile == map.WATER else map.d_continents[current_tile[0]][current_tile[1]].owner != player.user_name):
            DISPLAYSURF.blit(ATTACK_OPTION, (((selectedCountry[0] - 1) % map.WIDTH) * TILESIZE, ((selectedCountry[1]) % map.HEIGHT) * TILESIZE), special_flags=BLEND_ADD)
            l_neighbors.append([(selectedCountry[0] - 1) % map.WIDTH, (selectedCountry[1]) % map.HEIGHT])
            
         current_tile = map.ll_map[(selectedCountry[1] + 1) % map.HEIGHT][selectedCountry[0]]
         if (False if current_tile == map.WATER else map.d_continents[current_tile[0]][current_tile[1]].owner != player.user_name):
            DISPLAYSURF.blit(ATTACK_OPTION, ((selectedCountry[0]) * TILESIZE, ((selectedCountry[1] + 1) % map.HEIGHT) * TILESIZE), special_flags=BLEND_ADD)
            l_neighbors.append([(selectedCountry[0]), (selectedCountry[1] + 1) % map.HEIGHT])
            
         current_tile = map.ll_map[(selectedCountry[1] - 1) % map.HEIGHT][selectedCountry[0]]
         if (False if current_tile == map.WATER else map.d_continents[current_tile[0]][current_tile[1]].owner != player.user_name):
            DISPLAYSURF.blit(ATTACK_OPTION, ((selectedCountry[0]) * TILESIZE, ((selectedCountry[1] - 1) % map.HEIGHT) * TILESIZE), special_flags=BLEND_ADD)
            l_neighbors.append([(selectedCountry[0]), (selectedCountry[1] - 1) % map.HEIGHT])
       
       for battle in range(len(l_attackers)):
         DISPLAYSURF.blit(DEFENDER, (l_defenders[battle][0] * TILESIZE, l_defenders[battle][1] * TILESIZE), special_flags=BLEND_ADD)
         blitBattle(map, DISPLAYSURF, l_attackers[battle], l_defenders[battle])
         DISPLAYSURF.blit(ATTACKER, (l_attackers[battle][0] * TILESIZE, l_attackers[battle][1] * TILESIZE), special_flags=BLEND_ADD)
      
       DISPLAYSURF.blit(SEND_PISTOLEERS, (170, map.HEIGHT * TILESIZE + 70))
       DISPLAYSURF.blit(SEND_MUSKETEERS, (575, map.HEIGHT * TILESIZE + 70))
       DISPLAYSURF.blit(SEND_CANNONS, (170, map.HEIGHT * TILESIZE + 125))
       DISPLAYSURF.blit(SEND_AIRSHIPS, (575, map.HEIGHT * TILESIZE + 125))
       
       if squishyEasterEgg:
         DISPLAYSURF.blit(UNIT_ATTACK_HIGHLIGHT, (170, map.HEIGHT * TILESIZE + 70), special_flags=BLEND_ADD)
         DISPLAYSURF.blit(UNIT_ATTACK_HIGHLIGHT, (575, map.HEIGHT * TILESIZE + 70), special_flags=BLEND_ADD)
         DISPLAYSURF.blit(UNIT_ATTACK_HIGHLIGHT, (170, map.HEIGHT * TILESIZE + 125), special_flags=BLEND_ADD)
         DISPLAYSURF.blit(UNIT_ATTACK_HIGHLIGHT, (575, map.HEIGHT * TILESIZE + 125), special_flags=BLEND_ADD)
         printIndicator(ATTACK_INDICATOR, map, DISPLAYSURF, curr_x, curr_y)
   
       DISPLAYSURF.blit(DONE_BUTTON if player.unit_counts > 0 else DONE_BUTTON_ACTIVE, (980, map.HEIGHT * TILESIZE + 70))
       
       blitInfo(DISPLAYSURF, map, INFO_ATTACK)
       DISPLAYSURF.blit(MOUSE_LIT if isOverButton(map, curr_x, curr_y) and selectedCountry != None and selectedCountry in l_attackers else MOUSE_UNLIT, (curr_x, curr_y))
       
       #update the display
       newSurface = pygame.transform.scale(DISPLAYSURF,(screenInfo.current_w, screenInfo.current_h), window)
       pygame.display.update()
   return map, l_attackers, l_defenders, oldMap[1]

def moveTroops(DISPLAYSURF, map, player, socket, host_address, l_attackers, l_defenders, l_playerNames, d_playerCountries):
   global moving
   print("Client: inside moveTroops")
   selectedCountry = None
   d_moves = {}
   l_senders = []
   l_receivers = []
   moving = True
   
   global refreshing
   refreshing = True
   def refresh():
      global refreshing
      global oldMap
      try:
         response = socket.recv(16384)
         socket.settimeout(0.2)
         try:
            response += socket.recv(16384)
            print("Wow, we actually got extra data")
         except:
            pass
         socket.settimeout(None)
         try:
            oldMap = pickle.loads(response)
         except:
            print("(Move Troops) Packet was: " + str(response))
            oldMap = None
      except:
         oldMap = None
      refreshing = False
      #print("set refreshing to false")
      return
      
   t_updateScreen = threading.Thread(target=refresh)
   t_updateScreen.daemon = True
   t_updateScreen.start()
   #print("Length of l_attackers is: " + str(len(l_attackers)))
   while refreshing:
      for event in pygame.event.get():
         #if the user wants to quit
         if handleGeneral(event, map):
            return None, None, None, None, None

      printMap(map, DISPLAYSURF, "Move Troops", standardInfo, (l_playerNames, d_playerCountries))
      DISPLAYSURF.blit(WAITING, (70, map.HEIGHT * TILESIZE + 70))
      for battle in range(len(l_attackers)):
         DISPLAYSURF.blit(DEFENDER, (l_defenders[battle][0] * TILESIZE, l_defenders[battle][1] * TILESIZE), special_flags=BLEND_ADD)
         blitBattle(map, DISPLAYSURF, l_attackers[battle], l_defenders[battle])
         DISPLAYSURF.blit(ATTACKER, (l_attackers[battle][0] * TILESIZE, l_attackers[battle][1] * TILESIZE), special_flags=BLEND_ADD)
      curr_x, curr_y = pygame.mouse.get_pos()
      curr_x *= xScale
      curr_y *= yScale
      DISPLAYSURF.blit(MOUSE_UNLIT, (curr_x, curr_y))
      #update the display
      newSurface = pygame.transform.scale(DISPLAYSURF,(screenInfo.current_w, screenInfo.current_h), window)
      pygame.display.update()
   #print("Exited refreshing")
   if oldMap != None:
      #print("Have a map")
      map = oldMap[0]
      if len(oldMap) > 3:
         #print("length is > 3")
         displayMessage(ATTACK_RESULTS, map, DISPLAYSURF, "Move Troops", oldMap[1], oldMap[3], oldMap[2])
         #print("did not die")
   else:
      displayMessage(CRASH_MESSAGE, map, DISPLAYSURF, "Move Troops", l_playerNames, d_playerCountries)
      return None, None, None, None, None
   if len(oldMap) == 3:
      if detectGameEnd(DISPLAYSURF, map, player, socket, oldMap[1], oldMap[2]):
         return None, None, None, None, None
   elif len(oldMap) == 4:
      if detectGameEnd(DISPLAYSURF, map, player, socket, oldMap[1], oldMap[3]):
         return None, None, None, None, None
   while moving:
      squishyEasterEgg = False
      #get all the user events
      curr_x, curr_y = pygame.mouse.get_pos()
      curr_x *= xScale
      curr_y *= yScale
      for event in pygame.event.get():
         #if the user wants to quit
         if handleGeneral(event, map, selectedCountry=selectedCountry):
            return None, None, None, None, None
      
         if event.type == MOUSEBUTTONDOWN:
            if curr_x < map.WIDTH * TILESIZE and curr_y < map.HEIGHT * TILESIZE: # if the user clicked on the map
               curr_country = map.ll_map[int(curr_y / TILESIZE)][int(curr_x / TILESIZE)]
               
               if (curr_country != map.WATER): # if the user did not click water
                  if [int(curr_x / TILESIZE), int(curr_y / TILESIZE)] != selectedCountry and selectedCountry != None: # if not clicking your selected country and there is a selected country
                     index = None
                     if [selectedCountry[0], selectedCountry[1]] in l_senders:
                        index = l_senders.index([selectedCountry[0], selectedCountry[1]])
                     if not ([selectedCountry[0], selectedCountry[1]] in l_senders) and [int(curr_x / TILESIZE), int(curr_y / TILESIZE)] in l_neighbors: # if selected country is not sending and clicking neighboring country
                        l_senders.append([selectedCountry[0], selectedCountry[1]])
                        l_receivers.append([int(curr_x / TILESIZE), int(curr_y / TILESIZE)])
                        d_moves[map.ll_map[selectedCountry[1]][selectedCountry[0]]] = [curr_country, UnitCounts(0, 0, 0, 0)] #[receiver, army]
                     elif index != None and l_receivers[index] == [int(curr_x / TILESIZE), int(curr_y / TILESIZE)]: # if clicking the country your selected country is sending troops to
                        del l_receivers[index]
                        l_senders.remove([selectedCountry[0], selectedCountry[1]])
                        d_moves[map.ll_map[selectedCountry[1]][selectedCountry[0]]] = None
                     elif map.d_continents[curr_country[0]][curr_country[1]].owner == player.user_name:
                        l_neighbors = []
                        selectedCountry = [int(curr_x / TILESIZE), int(curr_y / TILESIZE)]
                     else:
                        selectedCountry = None
                  elif map.d_continents[curr_country[0]][curr_country[1]].owner == player.user_name and selectedCountry != [int(curr_x / TILESIZE), int(curr_y / TILESIZE)]: # if the user clicked his own country and not a selected country
                     l_neighbors = []
                     selectedCountry = [int(curr_x / TILESIZE), int(curr_y / TILESIZE)]
                  else:
                     selectedCountry = None
               else:
                  selectedCountry = None
            elif selectedCountry != None:
               curr_country = map.ll_map[selectedCountry[1]][selectedCountry[0]]
               units = map.d_continents[curr_country[0]][curr_country[1]].unit_counts
               if selectedCountry in l_senders:
                  sender = d_moves[map.ll_map[selectedCountry[1]][selectedCountry[0]]]
                  #Pistoleers
                  if 175 + 245 <= curr_x <= 175 + 295 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120: # "All" for Pistoleers
                     sender[1].infantry = units.infantry
                  elif 175 + 295 <= curr_x <= 175 + 345 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120 and \
                        sender[1].infantry < units.infantry: # "+" for Pistoleers
                     sender[1].infantry += 1
                  elif 175 + 345 <= curr_x <= 175 + 395 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120: # "-" for Pistoleers
                     if sender[1].infantry > 0:
                        sender[1].infantry -= 1
                        
                  #Musketeers
                  if 580 + 245 <= curr_x <= 580 + 295 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120: # "All" for Musketeers
                     sender[1].archers = units.archers
                  elif 580 + 295 <= curr_x <= 580 + 345 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120 and \
                        sender[1].archers < units.archers:# "+" for Musketeers
                     sender[1].archers += 1
                  elif 580 + 345 <= curr_x <= 580 + 395 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 120: # "-" for Musketeers
                     if sender[1].archers > 0:
                        sender[1].archers -= 1
                        
                   #Cannons
                  if 175 + 245 <= curr_x <= 175 + 295 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175: # "All" for Cannons
                     sender[1].cannons = units.cannons
                  elif 175 + 295 <= curr_x <= 175 + 345 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175 and \
                        sender[1].cannons < units.cannons: # "+" for Cannons
                     sender[1].cannons += 1
                  elif 175 + 345 <= curr_x <= 175 + 395 and map.HEIGHT * TILESIZE + 125 < curr_y <= map.HEIGHT * TILESIZE + 175: # "-" for Cannons
                     if sender[1].cannons > 0:
                        sender[1].cannons -= 1
                        
                  #Airships
                  if 580 + 245 <= curr_x <= 580 + 295 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175: # "All" for Airships
                     sender[1].champions = units.champions
                  elif 580 + 295 <= curr_x <= 580 + 345 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175 and \
                        sender[1].champions < units.champions: # "+" for Airships
                     sender[1].champions += 1
                  elif 580 + 345 <= curr_x <= 580 + 395 and map.HEIGHT * TILESIZE + 125 <= curr_y <= map.HEIGHT * TILESIZE + 175: # "-" for Airships
                     if sender[1].champions > 0:
                        sender[1].champions -= 1
            #Done
            if 980 <= curr_x <= 1080 and map.HEIGHT * TILESIZE + 70 <= curr_y <= map.HEIGHT * TILESIZE + 175 and player.unit_counts == 0:
               packet = pickle.dumps((l_senders, l_receivers, d_moves, player))
               try:
                  socket.sendto(packet, host_address)
               except:
                  displayMessage(CRASH_MESSAGE, map, DISPLAYSURF, "Move Troops", l_playerNames, d_playerCountries)
                  return None, None, None, None, None # This is kinda funny
               moving = False
               
      if selectedCountry == None:
         printMap(map, DISPLAYSURF, "Move Troops", standardInfo, (oldMap[1], oldMap[3]))
      else:
         if [selectedCountry[0], selectedCountry[1]] in l_senders:
            printMap(map,  DISPLAYSURF, "Move Troops", moveInfo, (selectedCountry, d_moves[map.ll_map[selectedCountry[1]][selectedCountry[0]]]))
            squishyEasterEgg = True
         else:
            printMap(map, DISPLAYSURF, "Move Troops", selectedInfo, selectedCountry)

      if selectedCountry != None:
         DISPLAYSURF.blit(SELECTED_TILE, (selectedCountry[0] * TILESIZE, selectedCountry[1] * TILESIZE), special_flags=BLEND_ADD)
         
      if selectedCountry != None and not (selectedCountry in l_senders):
         current_tile = map.ll_map[(selectedCountry[1] + 1) % map.HEIGHT][(selectedCountry[0] + 1) % map.WIDTH]
         if (False if current_tile == map.WATER else map.d_continents[current_tile[0]][current_tile[1]].owner == player.user_name):
            DISPLAYSURF.blit(MOVE_OPTION, (((selectedCountry[0] + 1) % map.WIDTH) * TILESIZE, ((selectedCountry[1] + 1) % map.HEIGHT) * TILESIZE), special_flags=BLEND_ADD)
            l_neighbors.append([(selectedCountry[0] + 1) % map.WIDTH, (selectedCountry[1] + 1) % map.HEIGHT])
            
         current_tile = map.ll_map[(selectedCountry[1] - 1) % map.HEIGHT][(selectedCountry[0] + 1) % map.WIDTH]
         if (False if current_tile == map.WATER else map.d_continents[current_tile[0]][current_tile[1]].owner == player.user_name):
            DISPLAYSURF.blit(MOVE_OPTION, (((selectedCountry[0] + 1) % map.WIDTH) * TILESIZE, ((selectedCountry[1] - 1) % map.HEIGHT) * TILESIZE), special_flags=BLEND_ADD)
            l_neighbors.append([(selectedCountry[0] + 1) % map.WIDTH, (selectedCountry[1] - 1) % map.HEIGHT])
            
         current_tile = map.ll_map[(selectedCountry[1]) % map.HEIGHT][(selectedCountry[0] + 1) % map.WIDTH]
         if (False if current_tile == map.WATER else map.d_continents[current_tile[0]][current_tile[1]].owner == player.user_name):
            DISPLAYSURF.blit(MOVE_OPTION, (((selectedCountry[0] + 1) % map.WIDTH) * TILESIZE, (selectedCountry[1]) * TILESIZE), special_flags=BLEND_ADD)
            l_neighbors.append([(selectedCountry[0] + 1) % map.WIDTH, (selectedCountry[1])])
            
         current_tile = map.ll_map[(selectedCountry[1] + 1) % map.HEIGHT][(selectedCountry[0] - 1) % map.WIDTH]
         if (False if current_tile == map.WATER else map.d_continents[current_tile[0]][current_tile[1]].owner == player.user_name):
            DISPLAYSURF.blit(MOVE_OPTION, (((selectedCountry[0] - 1) % map.WIDTH) * TILESIZE, ((selectedCountry[1] + 1) % map.HEIGHT) * TILESIZE), special_flags=BLEND_ADD)
            l_neighbors.append([(selectedCountry[0] - 1) % map.WIDTH, (selectedCountry[1] + 1) % map.HEIGHT])
            
         current_tile = map.ll_map[(selectedCountry[1] - 1) % map.HEIGHT][(selectedCountry[0] - 1) % map.WIDTH]
         if (False if current_tile == map.WATER else map.d_continents[current_tile[0]][current_tile[1]].owner == player.user_name):
            DISPLAYSURF.blit(MOVE_OPTION, (((selectedCountry[0] - 1) % map.WIDTH) * TILESIZE, ((selectedCountry[1] - 1) % map.HEIGHT) * TILESIZE), special_flags=BLEND_ADD)
            l_neighbors.append([(selectedCountry[0] - 1) % map.WIDTH, (selectedCountry[1] - 1) % map.HEIGHT])
            
         current_tile = map.ll_map[selectedCountry[1]][(selectedCountry[0] - 1) % map.WIDTH]
         if (False if current_tile == map.WATER else map.d_continents[current_tile[0]][current_tile[1]].owner == player.user_name):
            DISPLAYSURF.blit(MOVE_OPTION, (((selectedCountry[0] - 1) % map.WIDTH) * TILESIZE, ((selectedCountry[1]) % map.HEIGHT) * TILESIZE), special_flags=BLEND_ADD)
            l_neighbors.append([(selectedCountry[0] - 1) % map.WIDTH, (selectedCountry[1]) % map.HEIGHT])
            
         current_tile = map.ll_map[(selectedCountry[1] + 1) % map.HEIGHT][selectedCountry[0]]
         if (False if current_tile == map.WATER else map.d_continents[current_tile[0]][current_tile[1]].owner == player.user_name):
            DISPLAYSURF.blit(MOVE_OPTION, ((selectedCountry[0]) * TILESIZE, ((selectedCountry[1] + 1) % map.HEIGHT) * TILESIZE), special_flags=BLEND_ADD)
            l_neighbors.append([(selectedCountry[0]), (selectedCountry[1] + 1) % map.HEIGHT])
            
         current_tile = map.ll_map[(selectedCountry[1] - 1) % map.HEIGHT][selectedCountry[0]]
         if (False if current_tile == map.WATER else map.d_continents[current_tile[0]][current_tile[1]].owner == player.user_name):
            DISPLAYSURF.blit(MOVE_OPTION, ((selectedCountry[0]) * TILESIZE, ((selectedCountry[1] - 1) % map.HEIGHT) * TILESIZE), special_flags=BLEND_ADD)
            l_neighbors.append([(selectedCountry[0]), (selectedCountry[1] - 1) % map.HEIGHT])
            
      for army in range(len(l_senders)):
         DISPLAYSURF.blit(DESTINATION, (l_receivers[army][0] * TILESIZE, l_receivers[army][1] * TILESIZE), special_flags=BLEND_ADD)
         blitMove(map, DISPLAYSURF, l_senders[army], l_receivers[army])
         DISPLAYSURF.blit(SOURCE, (l_senders[army][0] * TILESIZE, l_senders[army][1] * TILESIZE), special_flags=BLEND_ADD)
    
      DISPLAYSURF.blit(MOVE_PISTOLEERS, (170, map.HEIGHT * TILESIZE + 70))
      DISPLAYSURF.blit(MOVE_MUSKETEERS, (575, map.HEIGHT * TILESIZE + 70))
      DISPLAYSURF.blit(MOVE_CANNONS, (170, map.HEIGHT * TILESIZE + 125))
      DISPLAYSURF.blit(MOVE_AIRSHIPS, (575, map.HEIGHT * TILESIZE + 125))
      
      if squishyEasterEgg:
         DISPLAYSURF.blit(UNIT_MOVE_HIGHLIGHT, (170, map.HEIGHT * TILESIZE + 70), special_flags=BLEND_ADD)
         DISPLAYSURF.blit(UNIT_MOVE_HIGHLIGHT, (575, map.HEIGHT * TILESIZE + 70), special_flags=BLEND_ADD)
         DISPLAYSURF.blit(UNIT_MOVE_HIGHLIGHT, (170, map.HEIGHT * TILESIZE + 125), special_flags=BLEND_ADD)
         DISPLAYSURF.blit(UNIT_MOVE_HIGHLIGHT, (575, map.HEIGHT * TILESIZE + 125), special_flags=BLEND_ADD)
         printIndicator(MOVE_INDICATOR, map, DISPLAYSURF, curr_x, curr_y)
         
      DISPLAYSURF.blit(DONE_BUTTON if player.unit_counts > 0 else DONE_BUTTON_ACTIVE, (980, map.HEIGHT * TILESIZE + 70))
    
      blitInfo(DISPLAYSURF, map, INFO_MOVE)
      DISPLAYSURF.blit(MOUSE_LIT if isOverButton(map, curr_x, curr_y) and selectedCountry != None and selectedCountry in l_senders else MOUSE_UNLIT, (curr_x, curr_y))
    
      #update the display
      newSurface = pygame.transform.scale(DISPLAYSURF,(screenInfo.current_w, screenInfo.current_h), window)
      pygame.display.update()
      #fpsClock.tick(50)
   return map, l_senders, l_receivers, oldMap[1], oldMap[3]

newMap = None
def getMoney(DISPLAYSURF, map, player, socket, host_address, l_senders, l_receivers, l_playerNames, d_playerCountries):
   global refreshing
   refreshing = True
   print("Inside getMoney")
   def refresh():
      global refreshing
      global newMap
      try:
         response = socket.recv(16384)
         socket.settimeout(0.2)
         try:
            response += socket.recv(16384)
            print("Wow, we actually got extra data")
         except:
            pass
         socket.settimeout(None)
         try:
            newMap = pickle.loads(response)
         except:
            print("(GetMoney) Packet was: " + str(newMap))
            newMap = None
      except:
         newMap = None
         
      refreshing = False
      #print("set refreshing to false")
      return
      
   t_updateScreen = threading.Thread(target=refresh)
   t_updateScreen.daemon = True
   t_updateScreen.start()
   
   while refreshing:
      for event in pygame.event.get():
         #if the user wants to quit
         if handleGeneral(event, map):
            return None
      
      printMap(map, DISPLAYSURF, "Move Troops", standardInfo, (l_playerNames, d_playerCountries))
      
      for army in range(len(l_senders)):
         DISPLAYSURF.blit(DESTINATION, (l_receivers[army][0] * TILESIZE, l_receivers[army][1] * TILESIZE), special_flags=BLEND_ADD)
         blitMove(map, DISPLAYSURF, l_senders[army], l_receivers[army])
         DISPLAYSURF.blit(SOURCE, (l_senders[army][0] * TILESIZE, l_senders[army][1] * TILESIZE), special_flags=BLEND_ADD)
      DISPLAYSURF.blit(WAITING, (70, map.HEIGHT * TILESIZE + 70))
      curr_x, curr_y = pygame.mouse.get_pos()
      curr_x *= xScale
      curr_y *= yScale
      DISPLAYSURF.blit(MOUSE_UNLIT, (curr_x, curr_y))
      #update the display
      newSurface = pygame.transform.scale(DISPLAYSURF,(screenInfo.current_w, screenInfo.current_h), window)
      pygame.display.update()
   if newMap == None:
      displayMessage(CRASH_MESSAGE, map, DISPLAYSURF, "Move Troops", l_playerNames, d_playerCountries)
   elif detectGameEnd(DISPLAYSURF, newMap[0], player, socket, newMap[2], newMap[3]):
      return None
   return newMap

deadMap = None
def detectGameEnd(DISPLAYSURF, map, player, socket, l_playerNames, d_playerCountries):
   OK_COORDS = (650,650)
   EXIT_COORDS = (70, 770)
   global deadMap
   Won = True
   Lost = True
   done = False
   died = False
   LOSS_OVERLAY = DISPLAYSURF.copy()
   LOSS_OVERLAY.fill((255, 75, 75))
   LOSS_OVERLAY.convert_alpha()
   LOSS_SPECTATOR = DISPLAYSURF.copy()
   LOSS_SPECTATOR.fill((255,200,200))
   LOSS_SPECTATOR.convert_alpha()
   WIN_OVERLAY = DISPLAYSURF.copy()
   WIN_OVERLAY.fill((50, 120, 255))
   WIN_OVERLAY.convert_alpha()
   WIN_SPECTATOR = DISPLAYSURF.copy()
   WIN_SPECTATOR.fill((200,230,255))
   WIN_SPECTATOR.convert_alpha()
   for cont_name in map.d_continents.keys():
      for country in map.d_continents[cont_name]:
         if country.owner == player.user_name:
            Lost = False
         else:
            Won = False
            
   if len(l_playerNames) == 1:
      Won = True
   
   if Lost:
      def refresh():
         global deadMap
         global map
         global died
         while True:
            try:
               response = socket.recv(16384)
               socket.settimeout(0.2)
               try:
                  response += socket.recv(16384)
               except:
                  pass
               socket.settimeout(None)
               deadMap = pickle.loads(response)
            except:
               deadMap = None
               died = True
               return
            print("I'm dead and got a new map")
      
      t_updateScreen = threading.Thread(target=refresh)
      t_updateScreen.daemon = True
      t_updateScreen.start()
      
      while True:
         curr_x, curr_y = pygame.mouse.get_pos()
         curr_x *= xScale
         curr_y *= yScale
         over_ok = OK_COORDS[0] <= curr_x <= OK_COORDS[0] + 200 and OK_COORDS[1] <= curr_y <= OK_COORDS[1] + 100
         over_exit = EXIT_COORDS[0] <= curr_x <= EXIT_COORDS[0] + 200 and EXIT_COORDS[1] <= curr_y <= EXIT_COORDS[1] + 100
         for event in pygame.event.get():
            #if the user wants to quit
            if handleGeneral(event, map):
               return True
            if not done and over_ok and event.type == MOUSEBUTTONDOWN:
               done = True
            elif over_exit and event.type == MOUSEBUTTONDOWN:
               return True
         if deadMap != None:
            map = deadMap[0]
            l_playerNames = deadMap[1]
         if died:
            return True
         printMap(map, DISPLAYSURF, "Spectating", standardInfo, (l_playerNames, d_playerCountries))
         if not done:
            DISPLAYSURF.blit(LOSS_OVERLAY, (0, 0), special_flags=BLEND_MULT)
            DISPLAYSURF.blit(LOSER, (0, 0))
            DISPLAYSURF.blit(OK_LIT if over_ok else OK_UNLIT, OK_COORDS)
         else:
            DISPLAYSURF.blit(LOSS_SPECTATOR, (0, 0), special_flags=BLEND_MULT)
            DISPLAYSURF.blit(EXIT_LIT if over_exit else EXIT_UNLIT, EXIT_COORDS)
         
         DISPLAYSURF.blit(MOUSE_UNLIT, (curr_x, curr_y))
         #update the display
         newSurface = pygame.transform.scale(DISPLAYSURF,(screenInfo.current_w, screenInfo.current_h), window)
         pygame.display.update()
   elif Won:
      OK_COORDS = (450,650)
      while True:
         curr_x, curr_y = pygame.mouse.get_pos()
         curr_x *= xScale
         curr_y *= yScale
         over_ok = OK_COORDS[0] <= curr_x <= OK_COORDS[0] + 200 and OK_COORDS[1] <= curr_y <= OK_COORDS[1] + 100
         over_exit = EXIT_COORDS[0] <= curr_x <= EXIT_COORDS[0] + 200 and EXIT_COORDS[1] <= curr_y <= EXIT_COORDS[1] + 100
         for event in pygame.event.get():
            #if the user wants to quit
            if handleGeneral(event, map):
               return True
            if not done and over_ok and event.type == MOUSEBUTTONDOWN:
               done = True
            elif over_exit and event.type == MOUSEBUTTONDOWN:
               return True
      
         printMap(map, DISPLAYSURF, "Spectating", standardInfo, (l_playerNames, d_playerCountries))
         if not done:
            DISPLAYSURF.blit(WIN_OVERLAY, (0, 0), special_flags=BLEND_MULT)
            DISPLAYSURF.blit(WINNER, (0, 0))
            DISPLAYSURF.blit(OK_LIT if over_ok else OK_UNLIT, OK_COORDS)
         else:
            DISPLAYSURF.blit(WIN_SPECTATOR, (0, 0), special_flags=BLEND_MULT)
            DISPLAYSURF.blit(EXIT_LIT if over_exit else EXIT_UNLIT, EXIT_COORDS)
         
         DISPLAYSURF.blit(MOUSE_UNLIT, (curr_x, curr_y))
         #update the display
         newSurface = pygame.transform.scale(DISPLAYSURF,(screenInfo.current_w, screenInfo.current_h), window)
         pygame.display.update()
   
def play(host_address, player_name):
   pygame.mouse.set_visible(False)
   #set up the display
   print("Enter play")

   print("here after display")

   #use list comprehension to create our tilemap
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   print("About to connect to host")
   # connection to hostname on the port.
   s.connect(host_address)                               
   print("Connected to host")
   s.sendto(player_name.encode("ascii"), host_address)
   # Receive no more than 1024 bytes
   pickledResponse = s.recv(8192)
   map, player, l_playerNames, d_playerCountries = pickle.loads(pickledResponse)
   print("Got the map")
   
   try:
      pygame.mixer.music.load(SOUND_FILE_PATH + l_songs[song_index])
      pygame.mixer.music.play(1)
   except:
      pass

   # Map continent names to tiles
   incrementor = 0
   for continent in map.l_continent_names:
      incrementor += 1
      d_continent_tiles[continent] = incrementor
   
   # Populate texture map index dictionary based on player names
   temp_index = 0
   for name in map.l_player_names:
      temp_index += 1
      d_playerLogoIndexes[name] = temp_index
   
   prepareBackground(map, DISPLAYSURF)
   
   print(player_name)
   while True:
      map.current_player = player_name
      map = placeUnits(DISPLAYSURF, map, player, s, host_address, l_playerNames, d_playerCountries)
      if map == None:
         break
      map, l_attackers, l_defenders, l_playerNames = declareAttacks(DISPLAYSURF, map, player, s, host_address, l_playerNames, d_playerCountries)
      if map == None:
         break
      print("Length of l_attackers is: " + str(len(l_attackers)))
      # detectGameEnd(DISPLAYSURF, map, player, socket)
      map, l_senders, l_receivers, l_playerNames, d_playerCountries = moveTroops(DISPLAYSURF, map, player, s, host_address, l_attackers, l_defenders, l_playerNames, d_playerCountries)
      if map == None:
         break
      info = getMoney(DISPLAYSURF, map, player, s, host_address, l_senders, l_receivers, l_playerNames, d_playerCountries)
      if info == None:
         break
      map = info[0]
      player = info[1]
      l_playerNames = info[2]
      d_playerCountries = info[3]
      #pygame.quit()
      #sys.exit()
   print("Exited properly")
   s.close()
   
   pygame.mouse.set_visible(True)
   return

if __name__ == '__main__':
   host_address = sys.argv[1]
   player_name = sys.argv[2]
   print("host address: ",str(host_address))
   print("player name: ",str(player_name))
   play(host_address, player_name)