# server.py 
import socket
import os
import threading
from threading import Thread
import _thread
import pygame, sys, random
from pygame.locals import *
import pickle
from Maps import *

#import time

def listener(client, address):
   print("Accepted connection from: ", address)
   with clients_lock:
      clients.add(client)#Array of clients
   
   try:
      while True:
         data = client.recv(1024).decode() #block waiting for data from a client
         if not data:
            break
         else:
            print(repr(data))
            #with clients_lock:
               #for c in clients:
						#do something for every client
                      #c.sendall(data.encode('ascii'))
   finally:
      with clients_lock:
         clients.remove(client)
         client.close()

def serve():
   clients = set()
   clients_lock = threading.Lock()
   th = []


   #assemble the map
   player_count = int(input("Just for sake of argument, enter the number of players: "))
   map = Map(player_count)

   # create a socket object

   serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

   # get local machine name
   host = socket.gethostname()                           

   port = 9998                                          

   addr = (host, port)

   # bind to the port
   serversocket.bind((host, port))

   # queue up to 5 requests
   serversocket.listen(5)

   while True:
      print("Server is listening for connections...")
      client, address = serversocket.accept()
      packet = pickle.dumps(map)
      client.sendto(packet, addr)
      th.append(Thread(target=listener, args = (client,address)).start()) #spin another thread for the new client
      
   serversocket.close()