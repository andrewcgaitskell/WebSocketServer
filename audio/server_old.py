import socket               # Import socket module
import threading
addr = ''

def on_new_client(clientsocket,addr):
    while True:
        msg = clientsocket.recv(1024)
        #do some checks and if msg == someWeirdSignal: break:
        print(addr, ' >> ', msg)
        msg = raw_input('SERVER >> ')
        #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
        clientsocket.send(msg)
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
