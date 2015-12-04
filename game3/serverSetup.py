from tkinter import *
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.messagebox as tkmb
import socket
import threading
from threading import Thread
import _thread
import pickle
import time
import select
import subprocess
import sys
import SimpleServer

def refresh_frame(frame, canvas):
   frame.destroy()
   frame=Frame(canvas)
   canvas.create_window((0,0),window=frame,anchor='nw')
   frame.bind("<Configure>",myfunction)
   return frame

def display_players(frame, canvas, clients):
   while True:
      frame = refresh_frame(frame, canvas)
      print("Number of clients: " + str(len(clients)))
      for i in clients:
         c = Canvas(frame, width=300, height = 25)
         c.pack(side="top")
         l = Label(c,text=i[1])
         c.create_window (0,0, anchor=NW, window = l)
         bootButton = tk.Button(c, anchor=NW)
         bootButton["text"] = "Boot"
         c.create_window (250, 0, anchor=NW, window=bootButton)
      time.sleep(3)

def start_game():
   cmd = ['SimpleServer.py']
   root.destroy()
   process = subprocess.Popen([sys.executable, cmd])
   process.communicate()
      
def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=300,height=200)
    
def broadcast():
   while True:
      print("Listening")
      recv_data, addr = server_socket.recvfrom(4096)
      host = socket.gethostname()
      print (recv_data)
      sendData = (host, addr[1], server_name)
      packet = pickle.dumps(sendData) 
      server_socket.sendto(packet, addr)

def listener(client, address, clients, serversocket, player_name):
   print("Accepted connection from: ", address)
   with clients_lock:
      l_temp = (client, player_name)
      clients.add(l_temp)#Array of clients
      
      print(str(len(clients)))
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
      
def acceptPlayers():
   serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   host = socket.gethostname()
   port = 9999                                           
   addr = (host, port)
   serversocket.bind((host, port))
   serversocket.listen(5)
   while True:
      client, address = serversocket.accept()
      player_name = client.recv(4096).decode()
      th.append(Thread(target=listener, args = (client,address, clients, serversocket, player_name)).start())

th = []
clients = set()
clients_lock = threading.Lock()

address = ('', 54545)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_socket.bind(address)
server_name = input("The name of the server is: ")

t_broadcast = threading.Thread(target=broadcast)
t_broadcast.daemon = True
t_broadcast.start()

t_accept_players = threading.Thread(target=acceptPlayers)
t_accept_players.daemon = True
t_accept_players.start()

root=Tk()
sizex = 800
sizey = 600
posx  = 100
posy  = 100
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

myframe=Frame(root,relief=GROOVE,width=100,height=150,bd=1)
myframe.place(x=10,y=40)
players_label = Label(root, text="Players")
players_label.place(x=10, y=10)
password_label = Label(root, text="Password:")
password_label.place(x=10, y=320)
password_entry = Entry(root)
password_entry.place(x=70, y=320)
play_button = tk.Button(root, text="Play", command = start_game)
play_button.place(x=360, y=320)
canvas=Canvas(myframe)
frame=Frame(canvas)
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left")
canvas.create_window((0,0),window=frame,anchor='nw')
frame.bind("<Configure>",myfunction)
t_display_players = threading.Thread(target=display_players, args=(frame, canvas, clients))
t_display_players.daemon = True
t_display_players.start()

root.mainloop()