from tkinter import *
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.messagebox as tkmb
import socket
import threading
from threading import Thread
import _thread

def data():

    for i in range(50):
       c = Canvas(frame, width=200, height = 50, bg = "white")
       c.pack(side="top")
       text_id = c.create_text(10, 10, anchor="nw", text="LEEEE " + str(i))
       #Label(CANVAS,text=i).grid(row=i,column=0)
       #Label(frame,text="my text"+str(i)).grid(row=i,column=1)
       #Label(frame,text="..........").grid(row=i,column=2)

def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=200)

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