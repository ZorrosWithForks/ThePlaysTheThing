#UDP server responds to broadcast packets
#you can have more than one instance of these running
import socket
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.messagebox as tkmb
from tkinter import *
import socket
import threading
from threading import Thread
import _thread

address = ('', 54545)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_socket.bind(address)
l_players = []

class Application(tk.Frame):
   def __init__(self, master=None):
      tk.Frame.__init__(self, master)
      self.pack()
      f = Canvas(self)
      f.place(x=10, y=30, width="150", height="160")
      self.createWidgets(l_players, f)
      t = threading.Thread(target=self.listener)
      t.daemon = True # thread dies when main thread (only non-daemon thread) exits.
      t.start()
      
   def createWidgets(self, l_players, f):
      l_players = []
      players_label = Label(root, text="Players")
      players_label.place(x=10, y=10)
      players_scrollbar = Scrollbar(f, orient="vertical", command=f.yview)
      players_scrollbar.place(x=330, y=30, height=164)
      for line in range(10):
         c = Canvas(f, width=200, height = 25)
         c.pack(side="top")
         text_id = c.create_text(10, 10, anchor="nw")
         c.itemconfig(text_id, text="Line " + str(line))
         c.insert(text_id, 12,  "new ")
         l_players.append(c)
      
      password_label = Label(root, text="Password:")
      password_label.place(x=10, y=220)
      password_entry = Entry(root)
      password_entry.place(x=70, y=220)
      #self.hi_there = tk.Button(self)
      #self.hi_there["text"] = "Refresh"
      #self.hi_there["command"] = self.find_servers(l_players)
      #self.hi_there.place(x=200, y=250)

   def find_servers(self, l_players):
      print("Clicked refresh")
      l_players = []

   def listener(self):
      while True:
         print("Listening")
         recv_data, addr = server_socket.recvfrom(4096)
         print (recv_data)



server_name = input("The name of the server is: ")

root = tk.Tk()
root.geometry("350x280+300+300")
app = Application(master=root)
app.mainloop()
