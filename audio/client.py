import socket
import time
import pickle


HEADERSIZE = 10

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("acgtest.info", 5010))
    d = {1:"hi", 2: "there"}
    msg = pickle.dumps(d)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8')+msg
    print(msg)
    s.send(msg)
