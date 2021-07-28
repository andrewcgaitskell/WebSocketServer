# import socket programming library
import socket

import os

# import thread module
from _thread import *
import threading

from datetime import datetime, timezone

print_lock = threading.Lock()

# thread function
def threaded(c):
    while True:

        #jsonString = bytearray()

        #for _ in range(42):
        #    packet = c.recv(1024)
        #    if not packet:
        #        break
        #    jsonString.extend(packet)

        ##Data resides in jsonString variable
        chunks = []
        bytes_recd = 0
        MSGLEN = 1024
        while bytes_recd < MSGLEN:
            chunk = c.recv(MSGLEN - bytes_recd)
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
            print("bytes received")
            print(bytes_recd)
        
        data = ''.join(chunks)

        ##some_bytes = b'\xC3\xA9'


        # Open in "wb" mode to 
        # write a new file, or  
        # "ab" mode to append 
        start_date = datetime.now(timezone.utc).isoformat()
        filename = start_date
        folder = '~/data/audio/'
        myfolder = '/home/andrew_gaitskell/data/audio/'
        fullfilename = myfolder + filename
        
        with open(fullfilename, "wb") as binary_file: 
            # Write bytes to file 
            binary_file.write(chunk)

        end_date = datetime.now(timezone.utc).isoformat()
        
        newfilename = fullfilename + '_' + end_date + '.bytes'
        
        os.rename(fullfilename, newfilename)
        
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
