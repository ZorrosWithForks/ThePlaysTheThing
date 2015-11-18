#UDP client broadcasts to server(s)
import socket

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
      self.hi_there["text"] = "Refresh"
      self.hi_there["command"] = self.find_servers
      self.hi_there.pack(side="right")

   def find_servers(self):
     
      self.text_box.delete('1.0', tk.END)
      client_socket.sendto(data.encode('ascii'), address)

   def listener(self):
      print("Back in again")
      try:
         while True:
            recv_data, addr = client_socket.recvfrom(4096)
            self.text_box.insert(tk.END, addr[0] + "\n")
            self.text_box.mark_set(tk.INSERT, '1.0')
            self.text_box.focus()
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
app = Application(master=root)
app.mainloop()

s.close()