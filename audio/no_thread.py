# import socket programming library
import socket

import os

# import thread module
from _thread import *
import threading

from datetime import datetime, timezone

print_lock = threading.Lock()

chunk = bytearray()
fragments = bytearray()
bytes_recd = 0


def Main():
    host = ""
    start_date = datetime.now(timezone.utc).isoformat()
    end_date = datetime.now(timezone.utc).isoformat()
    
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
    s.listen(1)
    print("socket is listening")
    
    main_loop = 0
    c, addr = s.accept()
    print_lock.acquire()
    print('Connected to :', addr[0], ':', addr[1])
    end_date = datetime.now(timezone.utc).isoformat()
    # a forever loop until client wants to exit
    while True:
        main_loop = main_loop + 1
        ##print("main loop",main_loop)
        
        MSGLEN = 2048
        fragments = bytearray()
        chunk = bytearray()

        while True: 
            chunk = c.recv(1024)
            #chunk_byte = bytes(chunk)
            if not chunk: 
                break
            #fragments += chunk_byte
            fragments += chunk
            bytes_recd = len(fragments)
            if bytes_recd > 65536:
                print(bytes_recd)
                #break

                #data_recd += fragments

                #bytes_recd = len(data_recd)

                end_date = datetime.now(timezone.utc).isoformat()
                filename = start_date + '_' + end_date + '.bytes'
                folder = '~/data/audio/'
                myfolder = '/home/andrew_gaitskell/data/audio/'
                fullfilename = myfolder + filename
                with open(fullfilename, "wb") as binary_file: 
                    # Write bytes to file 
                    binary_file.write(fragments)
                #with open(fullfilename, "w") as filehandle:
                #    for listitem in fragments:
                #        filehandle.write('%s\n' % listitem)
                start_date = datetime.now(timezone.utc).isoformat()
                bytes_recd = 0
                fragments = bytearray()
    c.slose()
    s.close()

    
if __name__ == '__main__':
    Main()
