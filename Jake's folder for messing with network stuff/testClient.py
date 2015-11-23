#UDP client broadcasts to server(s)
import socket
import pygame
import Image, ImageTk
'''
address = ('<broadcast>', 54545)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

data = "Request"
client_socket.sendto(data.encode('ascii'), address)
while True:
   recv_data, addr = client_socket.recvfrom(4096)
   print (recv_data)
   print (addr)
'''
   
# client.py 
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.messagebox as tkmb
from tkinter import *
import socket
import threading
from threading import Thread
import _thread
from pygame import font
pygame.init()
pygame.font.init()


#SURFACE = pygame.display.set_mode((640, 400))
#FONT = pygame.font.SysFont("couriernew", 40, bold=True)

class Application(tk.Frame):

   def __init__(self, master=None):
      tk.Frame.__init__(self, master)
      self.pack()
      self.createWidgets()
      t = threading.Thread(target=self.listener)
      t.daemon = True # thread dies when main thread (only non-daemon thread) exits.
      t.start()

   def createWidgets(self):
      #SURFACE.blit(pygame.image.load('games_background.png'),(0,0))
      #SURFACE.blit(pygame.image.load('games_background2.png'),(0,0))
      self.find_servers

   def find_servers(self):
      self.text_box.delete('1.0', tk.END)
      client_socket.sendto(data.encode('ascii'), address)


   def listener(self):
      print("Back in again")
      new_game_pos_x = 50
      new_game_pos_y = 50
      game_number    = 1
      try:
         while True:
            recv_data, addr = client_socket.recvfrom(4096)
            if (addr != None):
               CANVAS.create_image(new_game_pos_x, new_game_pos_y, anchor=NW, image=game_banner)
               CANVAS.create_text(new_game_pos_x + 5, new_game_pos_y + 5, anchor=NW, text="Game " + str(game_number))
               #SURFACE.blit(pygame.image.load('game.png'), (new_game_pos_x,new_game_pos_y))
               #SURFACE.blit(FONT.render("GAME: " + str(game_number), True, (0,0,0)), (new_game_pos_x, new_game_pos_y))
               new_game_pos_y += 50
               game_number += 1
               #pygame.display.update()
            
      finally:
         print("It broke")

# create a socket object
address = ('<broadcast>', 54545)
data = "Request"
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_socket.sendto(data.encode('ascii'), address)

# get local machine name
host = socket.gethostname()
port = 54545

# connection to hostname on the port.
#s.connect((host, port))

#print("The time got from the server is %s" % tm.decode('ascii'))

root = tk.Tk()
CANVAS = Canvas(root, width = 640, height = 400)
CANVAS.pack()
background = PhotoImage(file="games_background.png")
background2 = PhotoImage(file="games_background2.png")
game_banner = PhotoImage(file="game.png")
image = Image.open(r'\\csmain\Classes\SE_Project\Developement\16-DiningPhilosophers\Caleb\Jake''s folder for messing with network stuff\games_background2.png')
#photo image object
tkimage = ImageTk.PhotoImage(background2)
players_label = Label(root, text="Players")
players_label.pack(side=LEFT)
CANVAS.create_image(0,0, anchor=NW, image=background)
CANVAS.create_image(0,0, anchor=NW, image=background2)
Tkinter.Label(root, image=tkimage, text="Players", compound=Tkinter.CENTER).pack()

password_label = Label(root, text="Password")
password_label.pack(side = LEFT)
password = password_entry = Entry(root)
password_entry.pack(side = LEFT)
app = Application(master=root)
app.mainloop()


#pygame.display.update()
s.close()