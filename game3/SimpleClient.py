#client.py
import socket
import os
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

pygame.font.init()

pygame.init()

fpsClock = pygame.time.Clock()
   
#constants representing the different resources
IMAGE_FILE_PATH = "ImageFiles\\"
CONTINENT_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 40)
COUNTRY_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 25)
UNIT_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 35)
MONEY_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 22)
COUNT_FONT = pygame.font.Font("OldNewspaperTypes.ttf", 20)
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
INFO_BUY_UNITS = pygame.image.load(IMAGE_FILE_PATH + "InfoBuyUnits.png")
INFO_ATTACK = pygame.image.load(IMAGE_FILE_PATH + "InfoAttack.png")
INFO_RESOLVE = pygame.image.load(IMAGE_FILE_PATH + "InfoBattle.png")
INFO_MOVE = pygame.image.load(IMAGE_FILE_PATH + "InfoMove.png")
INFO_PISTOLEERS = pygame.image.load(IMAGE_FILE_PATH + "InfoPistoleers.png")
INFO_MUSKETEERS = pygame.image.load(IMAGE_FILE_PATH + "InfoMusketeers.png")
INFO_CANNONS = pygame.image.load(IMAGE_FILE_PATH + "InfoCannons.png")
INFO_AIRSHIPS = pygame.image.load(IMAGE_FILE_PATH + "InfoAirships.png")
INFO_BUTTON_OFF = pygame.image.load(IMAGE_FILE_PATH + "HelpButton.png")
INFO_BUTTON_ON = pygame.image.load(IMAGE_FILE_PATH + "HelpButtonActive.png")

ATK_LEFT_EDGE = pygame.image.load(IMAGE_FILE_PATH + 'BattleGears_Edge_Left.png')
ATK_RIGHT_EDGE = pygame.image.load(IMAGE_FILE_PATH + 'BattleGears_Edge_Right.png')
ATK_TOP_EDGE = pygame.image.load(IMAGE_FILE_PATH + 'BattleGears_Edge_Top.png')
ATK_BOTTOM_EDGE = pygame.image.load(IMAGE_FILE_PATH + 'BattleGears_Edge_Bottom.png')
ATK_LEFT_RIGHT = pygame.image.load(IMAGE_FILE_PATH + 'BattleGears_L_R.png')
ATK_TOP_BOTTOM = pygame.image.load(IMAGE_FILE_PATH + 'BattleGears_T_B.png')
ATK_UPLEFT_DOWNRIGHT = pygame.image.load(IMAGE_FILE_PATH + 'BattleGears_UL_BR.png')
ATK_DOWNLEFT_UPRIGHT = pygame.image.load(IMAGE_FILE_PATH + 'BattleGears_UR_BL.png')

MOVE_LEFT_EDGE = pygame.image.load(IMAGE_FILE_PATH + 'BattleGears_Edge_Left.png')
MOVE_RIGHT_EDGE = pygame.image.load(IMAGE_FILE_PATH + 'MoveGears_Edge_Right.png')
MOVE_TOP_EDGE = pygame.image.load(IMAGE_FILE_PATH + 'BattleGears_Edge_Top.png')
MOVE_BOTTOM_EDGE = pygame.image.load(IMAGE_FILE_PATH + 'MoveGears_Edge_Bottom.png')
MOVE_LEFT_RIGHT = pygame.image.load(IMAGE_FILE_PATH + 'MoveGears_L_R.png')
MOVE_TOP_BOTTOM = pygame.image.load(IMAGE_FILE_PATH + 'MoveGears_T_B.png')
MOVE_UPLEFT_DOWNRIGHT = pygame.image.load(IMAGE_FILE_PATH + 'MoveGears_UL_BR.png')
MOVE_DOWNLEFT_UPRIGHT = pygame.image.load(IMAGE_FILE_PATH + 'MoveGears_UR_BL.png')

MOUSE_OVER = pygame.image.load(IMAGE_FILE_PATH + 'MouseOver.png')
MOUSE_OVER_UNKNOWN = pygame.image.load(IMAGE_FILE_PATH + 'MouseOverUnknown.png')
ATTACK_COUNTS = pygame.image.load(IMAGE_FILE_PATH + 'BattleCounts.png')
HIGHLIGHT_ATTACK = pygame.image.load(IMAGE_FILE_PATH + 'BattleCountsHighlight.png')
INFO_MARQUEE = pygame.image.load(IMAGE_FILE_PATH + "InfoMarque.png")
INFO_OVERLAY = pygame.image.load(IMAGE_FILE_PATH + "InfoMarqueOverlay.png")
MAP_FRAME = pygame.image.load(IMAGE_FILE_PATH + "MapFrame.png")
MAP_LIGHT = pygame.image.load(IMAGE_FILE_PATH + "MapLighting.png")
SELECTED_TILE = pygame.image.load(IMAGE_FILE_PATH + "Selected.png")
ATTACK_OPTION = pygame.image.load(IMAGE_FILE_PATH + "AttackOption.png")
MOVE_OPTION = pygame.image.load(IMAGE_FILE_PATH + "MoveOption.png")
ATTACKER = pygame.image.load(IMAGE_FILE_PATH + "Attacker.png")
DEFENDER = pygame.image.load(IMAGE_FILE_PATH + "Defender.png")
SOURCE = pygame.image.load(IMAGE_FILE_PATH + "MoveSource.png")
DESTINATION = pygame.image.load(IMAGE_FILE_PATH + "MoveDestination.png")
WAITING = pygame.image.load(IMAGE_FILE_PATH + "Waiting.png")

SEND_PISTOLEERS = pygame.image.load(IMAGE_FILE_PATH + "SendPistoleers.png")
SEND_MUSKETEERS = pygame.image.load(IMAGE_FILE_PATH + "SendMusketeers.png")
SEND_CANNONS = pygame.image.load(IMAGE_FILE_PATH + "SendCannons.png")
SEND_AIRSHIPS = pygame.image.load(IMAGE_FILE_PATH + "SendAirships.png")
DONE_BUTTON = pygame.image.load(IMAGE_FILE_PATH + "DoneButton.png")
DONE_BUTTON_ACTIVE = pygame.image.load(IMAGE_FILE_PATH + "DoneButtonActive.png")

MOVE_PISTOLEERS = pygame.image.load(IMAGE_FILE_PATH + "MovePistoleers.png")
MOVE_MUSKETEERS = pygame.image.load(IMAGE_FILE_PATH + "MoveMusketeers.png")
MOVE_CANNONS    = pygame.image.load(IMAGE_FILE_PATH + "MoveCannons.png")
MOVE_AIRSHIPS   = pygame.image.load(IMAGE_FILE_PATH + "MoveAirships.png")


def blitInfo(DISPLAYSURF, map, phase_info, displayUnitThings=True):
   curr_x, curr_y = pygame.mouse.get_pos()
   
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
   if min(attack_coords[0], defend_coords[0]) == 0 and max(attack_coords[0], defend_coords[0]) == map.WIDTH - 1:
      DISPLAYSURF.blit(ATK_LEFT_EDGE, (0, (attack_coords[1] if attack_coords[0] == 0 else defend_coords[1]) * TILESIZE))
      DISPLAYSURF.blit(ATK_RIGHT_EDGE, ((map.WIDTH - 1) * TILESIZE, (attack_coords[1] if defend_coords[0] == 0 else defend_coords[1]) * TILESIZE))
   elif min(attack_coords[1], defend_coords[1]) == 0 and max(attack_coords[1], defend_coords[1]) == map.HEIGHT - 1:
      DISPLAYSURF.blit(ATK_TOP_EDGE, ((attack_coords[0] if attack_coords[1] == 0 else defend_coords[0]) * TILESIZE, 0))
      DISPLAYSURF.blit(ATK_BOTTOM_EDGE, ((attack_coords[0] if defend_coords[1] == 0 else defend_coords[0]) * TILESIZE, (map.HEIGHT - 1) * TILESIZE))
   elif attack_coords[0] == defend_coords[0]:
      DISPLAYSURF.blit(ATK_TOP_BOTTOM, (attack_coords[0] * TILESIZE, min(attack_coords[1], defend_coords[1]) * TILESIZE))
   elif attack_coords[1] == defend_coords[1]:
      DISPLAYSURF.blit(ATK_LEFT_RIGHT, (min(attack_coords[0], defend_coords[0]) * TILESIZE, attack_coords[1] * TILESIZE))
   elif attack_coords[0] < defend_coords[0] and attack_coords[1] < defend_coords[1]:
      DISPLAYSURF.blit(ATK_UPLEFT_DOWNRIGHT, (attack_coords[0] * TILESIZE, attack_coords[1] * TILESIZE))
   elif attack_coords[0] > defend_coords[0] and attack_coords[1] > defend_coords[1]:
      DISPLAYSURF.blit(ATK_UPLEFT_DOWNRIGHT, (defend_coords[0] * TILESIZE, defend_coords[1] * TILESIZE))
   else:
      DISPLAYSURF.blit(ATK_DOWNLEFT_UPRIGHT, (min(attack_coords[0], defend_coords[0]) * TILESIZE, min(attack_coords[1], defend_coords[1]) * TILESIZE))

def blitMove(map, DISPLAYSURF, source_coords, dest_coords):
   if min(source_coords[0], dest_coords[0]) == 0 and max(source_coords[0], dest_coords[0]) == map.WIDTH - 1:
      DISPLAYSURF.blit(MOVE_LEFT_EDGE, (0, (source_coords[1] if source_coords[0] == 0 else dest_coords[1]) * TILESIZE))
      DISPLAYSURF.blit(MOVE_RIGHT_EDGE, ((map.WIDTH - 1) * TILESIZE, (source_coords[1] if dest_coords[0] == 0 else dest_coords[1]) * TILESIZE))
   elif min(source_coords[1], dest_coords[1]) == 0 and max(source_coords[1], dest_coords[1]) == map.HEIGHT - 1:
      DISPLAYSURF.blit(MOVE_TOP_EDGE, ((source_coords[0] if source_coords[1] == 0 else dest_coords[0]) * TILESIZE, 0))
      DISPLAYSURF.blit(MOVE_BOTTOM_EDGE, ((source_coords[0] if dest_coords[1] == 0 else dest_coords[0]) * TILESIZE, (map.HEIGHT - 1) * TILESIZE))
   elif source_coords[0] == dest_coords[0]:
      DISPLAYSURF.blit(MOVE_TOP_BOTTOM, (source_coords[0] * TILESIZE, min(source_coords[1], dest_coords[1]) * TILESIZE))
   elif source_coords[1] == dest_coords[1]:
      DISPLAYSURF.blit(MOVE_LEFT_RIGHT, (min(source_coords[0], dest_coords[0]) * TILESIZE, source_coords[1] * TILESIZE))
   elif source_coords[0] < dest_coords[0] and source_coords[1] < dest_coords[1]:
      DISPLAYSURF.blit(MOVE_UPLEFT_DOWNRIGHT, (source_coords[0] * TILESIZE, source_coords[1] * TILESIZE))
   elif source_coords[0] > dest_coords[0] and source_coords[1] > dest_coords[1]:
      DISPLAYSURF.blit(MOVE_UPLEFT_DOWNRIGHT, (dest_coords[0] * TILESIZE, dest_coords[1] * TILESIZE))
   else:
      DISPLAYSURF.blit(MOVE_DOWNLEFT_UPRIGHT, (min(source_coords[0], dest_coords[0]) * TILESIZE, min(source_coords[1], dest_coords[1]) * TILESIZE))

#a dictionary linking resources to textures
textures =   {
                WATER  : pygame.image.load(IMAGE_FILE_PATH + 'water.png'),
                DEEP_WATER : pygame.image.load(IMAGE_FILE_PATH + 'deep_water.png'),
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

d_playerLogoIndexes = { UNOCCUPIED: 0 }

#useful game dimensions
MARGIN = 50
TILESIZE  = 100
BOTTOM_HALF_START = 15

map_X_offset = 0
map_Y_offset = 0

d_continent_tiles = {}

def standardInfo(map, DISPLAYSURF, params):
    #Highlight country mouse is over and display country info
    curr_x, curr_y = pygame.mouse.get_pos()
    if (curr_x < map.WIDTH * TILESIZE and curr_y < map.HEIGHT * TILESIZE and map.ll_map[int(curr_y / TILESIZE)][int(curr_x / TILESIZE)] != map.WATER):
      curr_country = map.ll_map[int(curr_y / TILESIZE)][int(curr_x / TILESIZE)]
      DISPLAYSURF.blit(MOUSE_OVER if map.d_continents[curr_country[0]][curr_country[1]].owner != None else MOUSE_OVER_UNKNOWN, (int(curr_x / TILESIZE) * TILESIZE - MARGIN, int(curr_y / TILESIZE) * TILESIZE - MARGIN), special_flags=BLEND_ADD)
      current_tile = map.ll_map[int(curr_y / TILESIZE)][int(curr_x / TILESIZE)]
      DISPLAYSURF.blit(CONTINENT_FONT.render("Continent: " + current_tile[0], True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 120))
      DISPLAYSURF.blit(COUNTRY_FONT.render("Country: " + map.d_continents[current_tile[0]][current_tile[1]].name, True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 170))
      
      country_known = map.d_continents[current_tile[0]][current_tile[1]].owner != None 
      # Unit counts by type
      DISPLAYSURF.blit(COUNTRY_FONT.render("Pistoleers: " + (str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.infantry) if country_known else "?"), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 225))
      DISPLAYSURF.blit(COUNTRY_FONT.render("Musketeers: " + (str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.archers) if country_known else "?"), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 250))
      DISPLAYSURF.blit(COUNTRY_FONT.render("Cannons: " + (str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.cannons) if country_known else "?"), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 275))
      DISPLAYSURF.blit(COUNTRY_FONT.render("Airships: " + (str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.champions) if country_known else "?"), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 300))
      
      # Country bonuses
      DISPLAYSURF.blit(COUNTRY_FONT.render("Attack Bonus: " + (str(map.d_continents[current_tile[0]][current_tile[1]].attack_bonus) + "%" if country_known else "?"), True, ATTACK_COLOR), (map.WIDTH * TILESIZE + 100, 350))
      DISPLAYSURF.blit(COUNTRY_FONT.render("Defense Bonus: " + (str(map.d_continents[current_tile[0]][current_tile[1]].defense_bonus) + "%" if country_known else "?"), True, DEFEND_COLOR), (map.WIDTH * TILESIZE + 100, 375))
      
      # Owner
      DISPLAYSURF.blit(COUNTRY_FONT.render("Owner: " + (str(map.d_continents[current_tile[0]][current_tile[1]].owner) if country_known else "?"), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 425))
         
      DISPLAYSURF.blit(CONTINENT_FONT.render("Continent Bonus: " + str(map.d_bonuses[current_tile[0]]), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 500))
    else:
      x_offset = 120
      y_offset = 180
      DISPLAYSURF.blit(CONTINENT_FONT.render("Players:", True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 130))
      for name in map.l_player_names:
         DISPLAYSURF.blit(COUNTRY_FONT.render(name, True, (0,0,0)), (map.WIDTH * TILESIZE + x_offset, y_offset))
         y_offset += 25
      y_offset += 25
      DISPLAYSURF.blit(CONTINENT_FONT.render("Continent Bonuses:", True, (0,0,0)), (map.WIDTH * TILESIZE + 100, y_offset))
      y_offset += 20
      for continent_name in map.l_continent_names:
         y_offset += 25
         DISPLAYSURF.blit(COUNTRY_FONT.render(continent_name + ": " + str(map.d_bonuses[continent_name]), True, (0,0,0)), (map.WIDTH * TILESIZE + x_offset, y_offset))

def selectedInfo(map, DISPLAYSURF, params):
   current_tile = map.ll_map[params[1]][params[0]]
    
   DISPLAYSURF.blit(CONTINENT_FONT.render("Continent: " + current_tile[0], True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 120))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Country: " + map.d_continents[current_tile[0]][current_tile[1]].name, True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 170))

   # Unit counts by type
   DISPLAYSURF.blit(COUNTRY_FONT.render("Pistoleers: " + str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.infantry), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 225))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Musketeers: " + str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.archers), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 250))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Cannons: " + str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.cannons), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 275))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Airships: " + str(map.d_continents[current_tile[0]][current_tile[1]].unit_counts.champions), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 300))
    
   # Country bonuses
   DISPLAYSURF.blit(COUNTRY_FONT.render("Attack Bonus: " + str(map.d_continents[current_tile[0]][current_tile[1]].attack_bonus) + "%" , True, ATTACK_COLOR), (map.WIDTH * TILESIZE + 100, 350))
   DISPLAYSURF.blit(COUNTRY_FONT.render("Defense Bonus: " + str(map.d_continents[current_tile[0]][current_tile[1]].defense_bonus) + "%", True, DEFEND_COLOR), (map.WIDTH * TILESIZE + 100, 375))
    
   # Owner
   DISPLAYSURF.blit(COUNTRY_FONT.render("Owner: " + str(map.d_continents[current_tile[0]][current_tile[1]].owner if map.d_continents[current_tile[0]][current_tile[1]].owner != None else "Neutral"), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 425))
    
   DISPLAYSURF.blit(CONTINENT_FONT.render("Continent Bonus: " + str(map.d_bonuses[current_tile[0]]), True, (0,0,0)), (map.WIDTH * TILESIZE + 100, 500))
    
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
    
def printMap(map, DISPLAYSURF, infoDisplay, params=None):
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
               DISPLAYSURF.blit(textures[WATER], (((column) % map.WIDTH) * TILESIZE - MARGIN, ((row) % map.HEIGHT) * TILESIZE - MARGIN))
          
    #loop through each row
    for row in range(map.HEIGHT):
        #loop through each column in the row
        for column in range(map.WIDTH):
            #draw the resource at that position in the tilemap, using the correct colour
            if (map.ll_map[row][column] == WATER):
               DISPLAYSURF.blit(textures[DEEP_WATER], (((column) % map.WIDTH) * TILESIZE - MARGIN, ((row) % map.HEIGHT) * TILESIZE - MARGIN))

    DISPLAYSURF.blit(source=textures[OVERLAY], dest=(0,0), special_flags=BLEND_MULT)
    DISPLAYSURF.blit(MAP_FRAME, dest=(0,0))
    DISPLAYSURF.blit(MAP_LIGHT, dest=(0,0), special_flags=BLEND_ADD)
			   
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

    DISPLAYSURF.blit(source=INFO_MARQUEE, dest=(map.WIDTH * TILESIZE, 0))
    DISPLAYSURF.blit(source=pygame.image.load(IMAGE_FILE_PATH + "BaseBoard.png"), dest=(0, map.HEIGHT * TILESIZE))
    
    infoDisplay(map, DISPLAYSURF, params)

    DISPLAYSURF.blit(source=INFO_OVERLAY, dest=(map.WIDTH * TILESIZE, 0), special_flags=BLEND_RGBA_ADD)

def handleGeneral(event, map, temp_map=None, selectedCountry=None):
  global map_X_offset
  global map_Y_offset
  if event.type == QUIT:
      #and the game and close the window
      pygame.quit()
      sys.exit()
  pygame.mouse.set_visible(True)
  # if a key is pressed
  if event.type == KEYDOWN:
      if event.key == K_ESCAPE:
         # and the game and close the window
         pygame.quit()
         sys.exit()

         

def placeUnits(DISPLAYSURF, map, player, socket, host_address):
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
       for event in pygame.event.get():
           #if the user wants to quit
           #if selectedCountry == None:
           handleGeneral(event, map, temp_map, selectedCountry)
           
           if event.type == MOUSEBUTTONDOWN:
             if curr_x < map.WIDTH * TILESIZE and curr_y < map.HEIGHT * TILESIZE:
                curr_country = map.ll_map[int(curr_y / TILESIZE)][int(curr_x / TILESIZE)] #Continent name and country index
                if (curr_country != map.WATER and map.d_continents[curr_country[0]][curr_country[1]].owner == map.current_player):
                  if map.d_continents[curr_country[0]][curr_country[1]].owner == player.user_name and selectedCountry != [int(curr_x / TILESIZE), int(curr_y / TILESIZE)]:
                     selectedCountry = [int(curr_x / TILESIZE), int(curr_y / TILESIZE)] #Coordinates of the current selected country
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
               socket.sendto(update_map, host_address)
               placing = False
       
       if selectedCountry == None:
         printMap(map, DISPLAYSURF, standardInfo)
       else:
         printMap(map, DISPLAYSURF, selectedInfo, selectedCountry)
       
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
       
       #update the display
       pygame.display.update()
   return map
refreshing = True
oldMap = None

def declareAttacks(DISPLAYSURF, map, player, socket, host_address):
   global refreshing
   refreshing = True
   def refresh():
      global refreshing
      global oldMap
      response = socket.recv(8192)
      oldMap = pickle.loads(response)
      refreshing = False
      print("set refreshing to false")
      return
      
   t_updateScreen = threading.Thread(target=refresh)
   t_updateScreen.daemon = True
   t_updateScreen.start()
   
   while refreshing:
      for event in pygame.event.get():
         #if the user wants to quit
         handleGeneral(event, map)
      
      printMap(map, DISPLAYSURF, standardInfo)
      DISPLAYSURF.blit(WAITING, (70, map.HEIGHT * TILESIZE + 70))
      #update the display
      pygame.display.update()
   print("Exited refreshing")
   map = oldMap
   declaring = True
   refreshing = False

   print("I have the map!")
   
   selectedCountry = None
   l_neighbors = []
   d_attacks = {}
   l_attackers = []
   l_defenders = []
   
   while declaring:
       #get all the user events
       curr_x, curr_y = pygame.mouse.get_pos()
       for event in pygame.event.get():
           #if the user wants to quit
           handleGeneral(event, map, selectedCountry=selectedCountry)
           
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
                     elif [int(curr_x / TILESIZE), int(curr_y / TILESIZE)] in l_defenders: # if clicking the country your selected country is attacking
                        if l_defenders.index([int(curr_x / TILESIZE), int(curr_y / TILESIZE)]) == l_attackers.index(selectedCountry):
                           l_defenders.remove([int(curr_x / TILESIZE), int(curr_y / TILESIZE)])
                           l_attackers.remove([selectedCountry[0], selectedCountry[1]])
                           d_attacks[map.ll_map[selectedCountry[1]][selectedCountry[0]]] = None
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
               socket.sendto(packet, host_address)
               declaring = False
       
       
       
       if selectedCountry == None:
         printMap(map, DISPLAYSURF, standardInfo)
       else:
         if [selectedCountry[0], selectedCountry[1]] in l_attackers:
            printMap(map,  DISPLAYSURF, attackInfo, (selectedCountry, d_attacks[map.ll_map[selectedCountry[1]][selectedCountry[0]]]))
         else:
            printMap(map, DISPLAYSURF, selectedInfo, selectedCountry)
       
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
       DISPLAYSURF.blit(DONE_BUTTON if player.unit_counts > 0 else DONE_BUTTON_ACTIVE, (980, map.HEIGHT * TILESIZE + 70))
       
       blitInfo(DISPLAYSURF, map, INFO_ATTACK)
         
       #update the display
       pygame.display.update()
   return map, l_attackers, l_defenders

def moveTroops(DISPLAYSURF, map, player, socket, host_address, l_attackers, l_defenders):
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
      response = socket.recv(8192)
      oldMap = pickle.loads(response)
      refreshing = False
      print("set refreshing to false")
      return
      
   t_updateScreen = threading.Thread(target=refresh)
   t_updateScreen.daemon = True
   t_updateScreen.start()
   print("Length of l_attackers is: " + str(len(l_attackers)))
   while refreshing:
      for event in pygame.event.get():
         #if the user wants to quit
         handleGeneral(event, map)

      printMap(map, DISPLAYSURF, standardInfo)
      DISPLAYSURF.blit(WAITING, (70, map.HEIGHT * TILESIZE + 70))
      for battle in range(len(l_attackers)):
         DISPLAYSURF.blit(DEFENDER, (l_defenders[battle][0] * TILESIZE, l_defenders[battle][1] * TILESIZE), special_flags=BLEND_ADD)
         blitBattle(map, DISPLAYSURF, l_attackers[battle], l_defenders[battle])
         DISPLAYSURF.blit(ATTACKER, (l_attackers[battle][0] * TILESIZE, l_attackers[battle][1] * TILESIZE), special_flags=BLEND_ADD)
      #update the display
      pygame.display.update()
   print("Exited refreshing")
   map = oldMap
   detectGameEnd(DISPLAYSURF, map, player, socket)
   
   while moving:
      #get all the user events
      curr_x, curr_y = pygame.mouse.get_pos()
      for event in pygame.event.get():
         #if the user wants to quit
         handleGeneral(event, map, selectedCountry=selectedCountry)
      
         if event.type == MOUSEBUTTONDOWN:
            if curr_x < map.WIDTH * TILESIZE and curr_y < map.HEIGHT * TILESIZE: # if the user clicked on the map
               curr_country = map.ll_map[int(curr_y / TILESIZE)][int(curr_x / TILESIZE)]
               
               if (curr_country != map.WATER): # if the user did not click water
                  if [int(curr_x / TILESIZE), int(curr_y / TILESIZE)] != selectedCountry and selectedCountry != None: # if not clicking your selected country and there is a selected country
                     if not ([selectedCountry[0], selectedCountry[1]] in l_senders) and [int(curr_x / TILESIZE), int(curr_y / TILESIZE)] in l_neighbors: # if selected country is not sending and clicking neighboring country
                        l_senders.append([selectedCountry[0], selectedCountry[1]])
                        l_receivers.append([int(curr_x / TILESIZE), int(curr_y / TILESIZE)])
                        d_moves[map.ll_map[selectedCountry[1]][selectedCountry[0]]] = [curr_country, UnitCounts(0, 0, 0, 0)] #[receiver, army]
                     elif [int(curr_x / TILESIZE), int(curr_y / TILESIZE)] in l_receivers and [selectedCountry[0], selectedCountry[1]] in l_senders and \
                     l_receivers.index([int(curr_x / TILESIZE), int(curr_y / TILESIZE)]) == l_senders.index([selectedCountry[0], selectedCountry[1]]): # if clicking the country your selected country is sending troops to
                        l_receivers.remove([int(curr_x / TILESIZE), int(curr_y / TILESIZE)])
                        if [selectedCountry[0], selectedCountry[1]] in l_senders:
                           l_senders.remove([selectedCountry[0], selectedCountry[1]])
                        d_moves[map.ll_map[selectedCountry[1]][selectedCountry[0]]] = None
                     elif [selectedCountry[0], selectedCountry[1]] in l_senders and map.d_continents[curr_country[0]][curr_country[1]].owner == player.user_name and selectedCountry:
                        l_neighbors = []
                        selectedCountry = [int(curr_x / TILESIZE), int(curr_y / TILESIZE)]
                  elif map.d_continents[curr_country[0]][curr_country[1]].owner == player.user_name and selectedCountry != [int(curr_x / TILESIZE), int(curr_y / TILESIZE)]: # if the user clicked his own country and not a selected country
                     l_neighbors = []
                     selectedCountry = [int(curr_x / TILESIZE), int(curr_y / TILESIZE)]
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
               socket.sendto(packet, host_address)
               moving = False
               
      if selectedCountry == None:
         printMap(map, DISPLAYSURF, standardInfo)
      else:
         if [selectedCountry[0], selectedCountry[1]] in l_senders:
            printMap(map,  DISPLAYSURF, moveInfo, (selectedCountry, d_moves[map.ll_map[selectedCountry[1]][selectedCountry[0]]]))
         else:
            printMap(map, DISPLAYSURF, selectedInfo, selectedCountry)

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
      DISPLAYSURF.blit(DONE_BUTTON if player.unit_counts > 0 else DONE_BUTTON_ACTIVE, (980, map.HEIGHT * TILESIZE + 70))
    
      blitInfo(DISPLAYSURF, map, INFO_MOVE)
    
      #update the display
      pygame.display.update()
      #fpsClock.tick(50)
   return map, l_senders, l_receivers

newMap = None
def getMoney(DISPLAYSURF, map, player, socket, host_address, l_senders, l_receivers):
   global refreshing
   refreshing = True
   print("Inside getMoney")
   def refresh():
      global refreshing
      global newMap
      response = socket.recv(8192)
      newMap = pickle.loads(response)
      refreshing = False
      print("set refreshing to false")
      return
      
   t_updateScreen = threading.Thread(target=refresh)
   t_updateScreen.daemon = True
   t_updateScreen.start()
   
   while refreshing:
      for event in pygame.event.get():
         #if the user wants to quit
         handleGeneral(event, map)
      
      printMap(map, DISPLAYSURF, standardInfo)
      
      for army in range(len(l_senders)):
         DISPLAYSURF.blit(DESTINATION, (l_receivers[army][0] * TILESIZE, l_receivers[army][1] * TILESIZE), special_flags=BLEND_ADD)
         blitMove(map, DISPLAYSURF, l_senders[army], l_receivers[army])
         DISPLAYSURF.blit(SOURCE, (l_senders[army][0] * TILESIZE, l_senders[army][1] * TILESIZE), special_flags=BLEND_ADD)
      DISPLAYSURF.blit(WAITING, (70, map.HEIGHT * TILESIZE + 70))
      #update the display
      pygame.display.update()
      
   return newMap

deadMap = None
def detectGameEnd(DISPLAYSURF, map, player, socket):
   Won = True
   Lost = True
   deadMap = map
   for cont_name in map.d_continents.keys():
      for country in map.d_continents[cont_name]:
         if country.owner == player.user_name:
            Lost = False
         else:
            Won = False
   
   if Lost:
      LOSER = pygame.image.load(IMAGE_FILE_PATH + "InfoDefeat.png")
      def refresh():
         global deadMap
         global map
         while True:
            response = socket.recv(8192)
            map = pickle.loads(response)
            print("I'm dead and got a new map")
      
      t_updateScreen = threading.Thread(target=refresh)
      t_updateScreen.daemon = True
      t_updateScreen.start()
      
      while True:
         for event in pygame.event.get():
            #if the user wants to quit
            handleGeneral(event, map)
         map = deadMap
         printMap(map, DISPLAYSURF, standardInfo)
         DISPLAYSURF.fill((255, 75, 75), special_flags=BLEND_MULT)
         DISPLAYSURF.blit(LOSER, (0, 0))
         #update the display
         pygame.display.update()
   elif Won:
      WINNER = pygame.image.load(IMAGE_FILE_PATH + "InfoVictory.png")
      while True:
         for event in pygame.event.get():
            #if the user wants to quit
            handleGeneral(event, map)
         
         printMap(map, DISPLAYSURF, standardInfo)
         DISPLAYSURF.fill((50, 120, 255), special_flags=BLEND_MULT)
         DISPLAYSURF.blit(WINNER, (0, 0))
         #update the display
         pygame.display.update()
   
def play(host_address, player_name):
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
   map, player = pickle.loads(pickledResponse)
   print("Got the map")
   
   #s.sendto(player_name.encode("ascii"), host_address)

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
   
   print(player_name)
   DISPLAYSURF = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
   while True:
      map.current_player = player_name
      map = placeUnits(DISPLAYSURF, map, player, s, host_address)
      map, l_attackers, l_defenders = declareAttacks(DISPLAYSURF, map, player, s, host_address)
      print("Length of l_attackers is: " + str(len(l_attackers)))
      # detectGameEnd(DISPLAYSURF, map, player, socket)
      map, l_senders, l_receivers = moveTroops(DISPLAYSURF, map, player, s, host_address, l_attackers, l_defenders)
      info = getMoney(DISPLAYSURF, map, player, s, host_address, l_senders, l_receivers)
      map = info[0]
      player = info[1]
      print("Exited properly")
      #pygame.quit()
      #sys.exit()

   s.close()

if __name__ == '__main__':
   host_address = sys.argv[1]
   player_name = sys.argv[2]
   print("host address: ",str(host_address))
   print("player name: ",str(player_name))
   play(host_address, player_name)