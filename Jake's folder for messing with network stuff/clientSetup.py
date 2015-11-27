import socket
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.messagebox as tkmb
from tkinter import *
import socket
import threading
from threading import Thread
import _thread

l_servers = []

def displayServerList(CANVAS, l_servers):
   CANVAS.create_image(0,0, anchor=NW, image=background)
   new_game_pos_y = 50
   new_game_pos_x = 50
   for server in l_servers:
      CANVAS.create_image(new_game_pos_x, new_game_pos_y, anchor=NW, image=game_banner)
      CANVAS.create_text(new_game_pos_x + 5, new_game_pos_y + 5, anchor=NW, text=str(server[0]))
      new_game_pos_y += 50

class Application(tk.Frame):

   def __init__(self, master=None):
      tk.Frame.__init__(self, master)
      self.pack()
      self.createWidgets(l_servers)
      t = threading.Thread(target=self.listener)
      t.daemon = True # thread dies when main thread (only non-daemon thread) exits.
      t.start()
      password_label = Label(root, text="Password")
      password_label.pack()
      password_entry = Entry(root)
      password_entry.pack()
      
   def createWidgets(self, l_servers):
   
      self.text_box = tkst.ScrolledText(self, height = 3, width = 20)
      self.text_box.pack(side="top")

      self.hi_there = tk.Button(self)
      self.hi_there["text"] = "Refresh"
      self.hi_there["command"] = self.find_servers(l_servers)
      self.hi_there.pack(side="right")
      

      


# create a socket object
address = ('<broadcast>', 54545)
data = "Request"
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_socket.sendto(data.encode('ascii'), address)

# get local machine name
host = socket.gethostname()
port = 54545

# Make the canvas
root = tk.Tk()
CANVAS = Canvas(root, width = 640, height = 400)
CANVAS.pack()
background = PhotoImage(file="games_background.png")
background2 = PhotoImage(file="games_background2.png")
game_banner = PhotoImage(file="game.png")

app = Application (master=root)
app.mainloop()