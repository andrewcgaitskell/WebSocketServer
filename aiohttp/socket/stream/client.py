import socket
import pickle
import math

den = 20 
rad = 100
theta = math.tau / den

HOST = "acgtest.info" 
PORT = 5010

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT)) #connect to server
        
    for i in range(1000):
        i = i%den
        x = math.cos(i*theta) * rad
        y = math.sin(i*theta) * rad
        data = pickle.dumps((x, y), protocol=2) #protocol needs to be between 0 and 2 for Python 2
        sock.send(data) #send data
