# import socket programming library
import socket

# import thread module
from _thread import *
import threading

import datetime

print_lock = threading.Lock()

# thread function
def threaded(c):
    while True:

        jsonString = bytearray()

        for _ in range(32):

            packet = c.recv(1024)
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
            binary_file.write(jsonString)

    # connection closed
    c.close()


def Main():
    host = ""

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 5010
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))

    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit
    while True:

        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()

    
if __name__ == '__main__':
    Main()
