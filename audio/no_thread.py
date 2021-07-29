# import socket programming library
import socket

import os

# import thread module
from _thread import *
import threading

from datetime import datetime, timezone

print_lock = threading.Lock()

chunk = bytearray()
chunk_byte = bytearray()
fragments = bytearray()
bytes_recd = 0
data_recd = bytearray()
start_date = datetime.now(timezone.utc).isoformat()
end_date = datetime.now(timezone.utc).isoformat()




def Main():
    host = ""

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 5010
   
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    ##s.settimeout(2) 
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

        data_recd = bytearray()
        while True:
            MSGLEN = 2048
            fragments = b''
            chunk = b''

            while True: 
                chunk = c.recv(1024)
                chunk_byte = bytes(chunk)
                if not chunk: 
                    break
                fragments += chunk_byte


            data_recd += fragments


            bytes_recd = len(data_recd)

            print(bytes_recd)

            if bytes_recd >= 131072:
                end_date = datetime.now(timezone.utc).isoformat()
                filename = start_date + '_' + end_date + '.bytes'
                folder = '~/data/audio/'
                myfolder = '/home/andrew_gaitskell/data/audio/'
                fullfilename = myfolder + filename
                with open(fullfilename, "wb") as binary_file: 
                    # Write bytes to file 
                    binary_file.write(data_recd)
                data_recd = bytearray()
                start_date = datetime.now(timezone.utc).isoformat()
                bytes_recd = 0

    s.close()

    
if __name__ == '__main__':
    Main()
