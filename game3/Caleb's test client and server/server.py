import socket
import threading
from threading import Thread
import _thread
import pickle
import time
import select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port          = 9999
server_socket.bind(('172.16.211.107', port))
server_socket.listen(5)
print("server is listening")
while True:
   client, address = server_socket.accept() #block here
   data = client.recv(4096) #get the data
   data_value = pickle.loads(data)
   print("Got connection from", address, data_value)
   client.send(data)
   client.close()