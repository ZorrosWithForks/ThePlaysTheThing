from tkinter import *

def data():
    for i in range(50):
       c = Canvas(frame, width=200, height = 50, bg = "white")
       c.pack(side="top")
       text_id = c.create_text(10, 10, anchor="nw", text="LEEEE")
       #Label(CANVAS,text=i).grid(row=i,column=0)
       #Label(frame,text="my text"+str(i)).grid(row=i,column=1)
       #Label(frame,text="..........").grid(row=i,column=2)

def myfunction(event):
    canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=200)

root=Tk()
sizex = 300
sizey = 300
posx  = 100
posy  = 100
root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

myframe=Frame(root,relief=GROOVE,width=100,height=150,bd=1, background="red")
myframe.place(x=10,y=10)

canvas=Canvas(myframe, background = "blue")
frame=Frame(canvas, background = "green")
myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
canvas.configure(yscrollcommand=myscrollbar.set)

myscrollbar.pack(side="right",fill="y")
canvas.pack(side="left")
canvas.create_window((50,50),window=frame,anchor='nw')
frame.bind("<Configure>",myfunction)
data()
root.mainloop()