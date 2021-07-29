import socket
import struct
import sys
import time

Port=5010

#assume a socket disconnect (data returned is empty string) means  all data was #done being sent.
def recv_basic(the_socket):
    total_data=bytearray()
    while True:
        data = the_socket.recv(8192)
        if not data: break
        total_data.append(data)
    total_len=sum([len(i) for i in total_data])
    return total_len
    
def recv_timeout(the_socket,timeout=2):
    the_socket.setblocking(0)
    total_data=bytearray();data=bytearray();begin=time.time()
    while 1:
        #if you got some data, then break after wait sec
        if total_data and time.time()-begin>timeout:
            break
        #if you got no data at all, wait a little longer
        elif time.time()-begin>timeout*2:
            break
        try:
            data=the_socket.recv(8192)
            if data:
                total_data.append(data)
                begin=time.time()
            else:
                time.sleep(0.1)
        except:
            pass
    return ''.join(total_data)

def recv_size(the_socket):
    #data length is packed into 4 bytes
    total_len=0;total_data=bytearray();size=sys.maxsize
    size_data=bytearray()
    sock_data='';recv_size=8192
    while total_len<size:
        sock_data=the_socket.recv(recv_size)
        if not total_data:
            if len(sock_data)>4:
                size_data.append(sock_data)
                size=struct.unpack('>i', size_data[:4])[0]
                recv_size=size
                if recv_size>524288:recv_size=524288
                total_data.append(size_data[4:])
            else:
                size_data+=sock_data
        else:
            total_data.append(sock_data)
        total_len=sum([len(i) for i in total_data ])
    return total_len


##############
def start_server(recv_type=''):
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('',Port))
    
    sock.listen(5)
    print('started on',Port)
    while True:
        newsock,address=sock.accept()
        print('connected')
        if recv_type=='size': result=recv_size(newsock)
        elif recv_type=='end': result=recv_end(newsock)
        elif recv_type=='timeout': result=recv_timeout(newsock)
        else: result=newsock.recv(8192) 
        print('got',result)


if __name__=='__main__':
    #start_server()
    start_server(recv_type='size')
    #start_server(recv_type='timeout')
    #start_server(recv_type='end')

##def send_size(data):
##    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
##    sock.connect(('',Port))
##    sock.sendall(struct.pack('>i', len(data))+data)
##    sock.close()

##def send_end(data):
##    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
##    sock.connect(('localhost',Port))
##    sock.sendall(data+End)
##    sock.close()
