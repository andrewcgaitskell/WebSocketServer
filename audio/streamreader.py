##This code reads 1024*32(=32768) bytes in 32 iterations from the buffer which is received from Server in socket programming-python:
##jsonString = bytearray()
import time
from datetime import datetime
###################################################################################

import socket               # Import socket module
import threading
addr = ''

def on_new_client(clientsocket,addr):
    while True:
        jsonString = bytearray()

        for _ in range(32):

            packet = clientsocket.recv(1024)
            if not packet:
               break
            jsonString.extend(packet)

            ##Data resides in jsonString variable


            ##some_bytes = b'\xC3\xA9'


            # Open in "wb" mode to 
            # write a new file, or  
            # "ab" mode to append 
            my_date = datetime.now()
            filename = my_date.isoformat()
            folder = '~/data/audio/'

            with open(filename, "wb") as binary_file: 
                # Write bytes to file 
                binary_file.write(some_bytes)
                
    clientsocket.close()

s = socket.socket()         # Create a socket object
host = '' # Get local machine name
port = 5010                # Reserve a port for your service.

print('Server started!')
print('Waiting for clients...')

s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.

print('Got connection from', addr)
while True:
   c, addr = s.accept()     # Establish connection with client.
   threading.Thread(target=on_new_client,args=(c,addr))
   #Note it's (addr,) not (addr) because second parameter is a tuple
   #Edit: (c,addr)
   #that's how you pass arguments to functions when creating new threads using thread module.
s.close()

