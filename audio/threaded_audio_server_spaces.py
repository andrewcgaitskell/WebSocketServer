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
    chunk = bytearray()
    chunk_byte = bytearray()
    fragments = bytearray()
    bytes_recd = 0
    data_recd = bytearray()
    start_date = datetime.now(timezone.utc).isoformat()
    end_date = datetime.now(timezone.utc).isoformat()
    while True:

        #jsonString = bytearray()

        #for _ in range(42):
        #    packet = c.recv(1024)
        #    if not packet:
        #        break
        #    jsonString.extend(packet)

        ##Data resides in jsonString variable
        MSGLEN = 2048
        #while bytes_recd < MSGLEN:
        #    ##chunk = c.recv(MSGLEN - bytes_recd)
        #    chunk = c.recv(1024)
        #    #if chunk == '':
        #    #    raise RuntimeError("socket connection broken")
        #    chunks.append(chunk)
        #    bytes_recd = bytes_recd + len(chunk)
        #    ##print("bytes received")
        #    print(bytes_recd)
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
        #arr = bytearray(MSGLEN)
        #max_msg_size = 2048
        #pos = 0
        #while pos < msg_len:
        #    arr[pos:pos+max_msg_size] = sock.recv(max_msg_size)
        #    pos += max_msg_size
        #    print('receiving :',pos)
        #print('message size :', len(arr))
        
        ##data = ''.join(fragments)
        ##print("total bytes received :" + bytes_recd)
        ##some_bytes = b'\xC3\xA9'


        # Open in "wb" mode to 
        # write a new file, or  
        # "ab" mode to append 
        ##start_date = datetime.now(timezone.utc).isoformat()
        ##filename = start_date
        ##folder = '~/data/audio/'
        ##myfolder = '/home/andrew_gaitskell/data/audio/'
        ##fullfilename = myfolder + filename
        
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

        ##end_date = datetime.now(timezone.utc).isoformat()
        
        ##newfilename = fullfilename + '_' + end_date + '.bytes'
        
        #os.rename(fullfilename, newfilename)
        
    # connection closed
    c.close()


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

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()

    
if __name__ == '__main__':
    Main()
