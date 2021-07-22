import pickle
import socket
import struct

HEADER_SIZE = 4
HOST = ""
PORT = 5010


def receive(nb_bytes, conn):
    # Ensure that exactly the desired amount of bytes is received
    received = bytearray()
    while len(received) < nb_bytes:
        received += conn.recv(nb_bytes - len(received))

    return received

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
connection, address = s.accept()

while True:

    # receive header
    header = receive(HEADER_SIZE, connection)
    data_size = struct.unpack(">i", header)[0] # <-- TypeError

    # receive data
    data = receive(data_size, connection)
    print(pickle.loads(data))
