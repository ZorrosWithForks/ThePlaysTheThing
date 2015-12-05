from tkinter import *
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.messagebox as tkmb
import socket
import threading
from threading import Thread
import _thread
import time
import SimpleClient
import pickle
   
def joinGame(ip):
   print("attempting to join " + ip)
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   addr = (ip, 9999)
   
   s.connect(addr)
   s.sendto(player_name.encode('ascii'), addr)
   print("joined")
   new_server = (s.recv(1024).decode(), 9998)
   s.close()
   root.destroy()
   SimpleClient.play(new_server, player_name)
   
def display_servers(l_servers, frame, canvas):
   for widget in frame.winfo_children():
      widget.destroy()
   for server in l_servers:
      print("have a server from " + server[0])
      c = Canvas(frame, width=300, height = 30)
      c.pack(side="top")
      lbl_server_name = Label(c,text=server[2])
      c.create_window (5,5, anchor=NW, window = lbl_server_name)
      txt_password = Entry(c)
      c.create_window (100,8, anchor=NW, window = txt_password)
      joinButton = tk.Button(c, anchor=NW, command=lambda server=server: joinGame(server[0])) #Without server=server, each button passes the same argument, the last one in the iteration
      joinButton["text"] = "Join"
      c.create_window (250, 5, anchor=NW, window=joinButton)

def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=300,height=200)

def search(l_servers, frame, canvas):
   while True:
      recv_data, addr = client_socket.recvfrom(4096)
      packet = pickle.loads(recv_data)
      l_servers.append(packet)
      print("added a server: " + packet[0])
      display_servers(l_servers, frame, canvas)
      print("done displaying servers")
      
def request(l_servers, frame, canvas):
   print("looping requesting servers")
   del l_servers[:]
   display_servers(l_servers, frame, canvas)
   client_socket.sendto(data.encode('ascii'), address)

player_name = input("Enter username: ")
   
l_servers = []
address = ('<broadcast>', 54545)
data = "Request"
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_socket.sendto(data.encode('ascii'), address)

root=Tk()
sizex = 450
sizey = 350
posx  = 100
posy  = 100
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

myframe=Frame(root,relief=GROOVE,width=400,height=150,bd=1)
myframe.place(x=10,y=40)
games_label = Label(root, text="Servers")
games_label.place(x=10, y=10)
canvas=Canvas(myframe)
frame=Frame(canvas)
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left")
canvas.create_window((0,0),window=frame,anchor='nw')
frame.bind("<Configure>",myfunction)
refresh_button = tk.Button(root, text="Refresh", command= lambda: request(l_servers, frame, canvas))
refresh_button.place(x=200, y=260)
print("Made it")
t_search = threading.Thread(target=search, args=(l_servers, frame, canvas))
t_search.daemon = True
t_search.start()
print("Am I here?")
root.wm_title(player_name)
root.resizable(width=FALSE, height=FALSE)
root.mainloop()