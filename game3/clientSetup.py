from tkinter import *
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.messagebox as tkmb
import socket
import threading
from threading import Thread
import _thread
import time

def display_servers(l_servers):
    for server in l_servers:
      c = Canvas(frame, width=300, height = 30)
      c.pack(side="top")
      lbl_server_name = Label(c,text="Rodrick")
      c.create_window (5,5, anchor=NW, window = lbl_server_name)
      txt_password = Entry(c)
      c.create_window (100,8, anchor=NW, window = txt_password)
      bootButton = tk.Button(c, anchor=NW)
      bootButton["text"] = "Join"
      c.create_window (250, 5, anchor=NW, window=bootButton)

def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=300,height=200)

def search(l_servers):
   while True:
      recv_data, addr = client_socket.recvfrom(4096)
      l_servers.append(addr)
      print("added a server")
      display_servers(l_servers)
      print("done displaying servers")
      
def request(l_servers):
   while True:
      print("looping requesting servers")
      l_servers = []
      client_socket.sendto(data.encode('ascii'), address)
      time.sleep(3)
      
l_servers = []
address = ('<broadcast>', 54545)
data = "Request"
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client_socket.sendto(data.encode('ascii'), address)

root=Tk()
sizex = 800
sizey = 600
posx  = 100
posy  = 100
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

myframe=Frame(root,relief=GROOVE,width=300,height=150,bd=1)
myframe.place(x=10,y=40)
games_label = Label(root, text="Servers")
games_label.place(x=10, y=10)
password_label = Label(root, text="Password:")
password_label.place(x=100, y=10)
password_entry = Entry(root)
password_entry.place(x=70, y=260)
canvas=Canvas(myframe)
frame=Frame(canvas)
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left")
canvas.create_window((0,0),window=frame,anchor='nw')
frame.bind("<Configure>",myfunction)
t_request = threading.Thread(target=request, args=(l_servers,))
t_request.daemon = True
t_request.start()
print("Made it")
t_search = threading.Thread(target=search, args=(l_servers,))
t_search.daemon = True
t_search.start()

root.mainloop()