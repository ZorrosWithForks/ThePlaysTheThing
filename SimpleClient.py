#client.py
import socket
import os
import threading
from threading import Thread
import _thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = socket.gethostname()                           
print("test1")
port = 9999

# connection to hostname on the port.
s.connect((host, port))                               
print("test2")
# Receive no more than 1024 bytes                                    

#print("The time got from the server is %s" % tm.decode('ascii'))

#root = tk.Tk()


s.close()