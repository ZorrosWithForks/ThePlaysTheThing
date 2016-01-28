# client.py 
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.messagebox as tkmb
import socket
import threading
from threading import Thread
import _thread

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        t = threading.Thread(target=self.listener)
        t.daemon = True # thread dies when main thread (only non-daemon thread) exits.
        t.start()

    def createWidgets(self):
        self.text_box = tkst.ScrolledText(self, height = 20, width = 50)
        self.text_box.pack(side="top")
    
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Send"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="right")

        self.message = tk.Text(self, height = 3, width = 30)
        self.message.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")
        send_text = "Jake: " + self.message.get('1.0', tk.END)
        s.send(send_text.encode())
        self.message.delete('1.0', tk.END)

    def listener(self):
        print("Back in again")
        try:
            while True:
                tm = s.recv(1024)
                if tm:
                    print("Something to do")
                    self.text_box.insert(tk.END, tm.decode('ascii'))
                    self.text_box.mark_set(tk.INSERT, '1.0')
                    self.text_box.focus()
                else:
                    print("Nothing to do")
        finally:
            print("It broke")

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = "169.254.80.80"
print("test1")
port = 9999

# connection to hostname on the port.
s.connect((host, port))
print("test2")
# Receive no more than 1024 bytes

#print("The time got from the server is %s" % tm.decode('ascii'))

root = tk.Tk()
app = Application(master=root)
app.mainloop()

s.close()