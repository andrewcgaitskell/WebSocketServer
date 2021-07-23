import socket
import time
import pickle


HEADERSIZE = 10

HOST = ''
PORT = 5010

#d = {1:"hi", 2: "there"}
#msg = pickle.dumps(d)
#msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
#print(msg)
#clientsocket.send(msg)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    clientsocket, address = s.accept()
    print('Connected by', address)
    
    full_msg = b''
    new_msg = True
    while True:
        msg = s.recv(16)
        if new_msg:
            print("new msg len:",msg[:HEADERSIZE])
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        print(f"full message length: {msglen}")

        full_msg += msg

        print(len(full_msg))

        if len(full_msg)-HEADERSIZE == msglen:
            print("full msg recvd")
            print(full_msg[HEADERSIZE:])
            print(pickle.loads(full_msg[HEADERSIZE:]))
            new_msg = True
            full_msg = b""
