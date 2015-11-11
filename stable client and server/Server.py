# server.py 
import socket
import os
import threading
from threading import Thread
import _thread
#import time

def listener(client, address):
   print("Accepted connection from: ", address)
   with clients_lock:
      clients.add(client) #Array of clients
   try:
      while True:
         data = client.recv(1024).decode() #block waiting for data from a client
         if not data:
            break
         else:
            print(repr(data))
            with clients_lock:
               for c in clients:
						#do something for every client
                  c.sendall(data.encode('ascii'))
   finally:
      with clients_lock:
         clients.remove(client)
         client.close()

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

port = 9999                                           

# bind to the port
serversocket.bind((host, port))                                  

# queue up to 5 requests
serversocket.listen(5)                                           

clients = set()
clients_lock = threading.Lock()
th = []

while True:
   print("Server is listening for connections...")
   client, address = serversocket.accept()
   th.append(Thread(target=listener, args = (client,address)).start()) #spin another thread for the new client

serversocket.close()