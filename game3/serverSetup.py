from tkinter import *
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.messagebox as tkmb
import socket
import threading
from threading import Thread
import _thread
import pickle

def data():

    for i in range(42):
       c = Canvas(frame, width=200, height = 25)
       c.pack(side="top")
       l = Label(c,text="Rodrick")
       c.create_window (0,0, anchor=NW, window = l)
       bootButton = tk.Button(c, anchor=NW)
       bootButton["text"] = "Boot"
       c.create_window (150, 0, anchor=NW, window=bootButton)

def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=200)
    
def broadcast():
   while True:
      print("Listening")
      recv_data, addr = server_socket.recvfrom(4096)
      print (recv_data)
      sendData = (addr[0], addr[1], server_name)
      packet = pickle.dumps(sendData) 
      server_socket.sendto(packet, addr)

address = ('', 54545)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_socket.bind(address)
server_name = input("The name of the server is: ")
t = threading.Thread(target=broadcast)
t.daemon = True
t.start()

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
password_label.place(x=10, y=260)
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
data()
root.mainloop()