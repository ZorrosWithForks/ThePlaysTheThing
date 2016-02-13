import socket
import threading
from threading import Thread
import _thread
import pickle
import time
import select

username = input("enter username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('172.16.211.107', 9999))
pickled_username = pickle.dumps(username) #dump pickles onto the username to prepare for sending
client_socket.send(data_string) # send the pickled username to the server
data_from_server = client_socket.recv(4096)
data_from_server_value = pickle.loads(data_from_server)
client_socket.close()
