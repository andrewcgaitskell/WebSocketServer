# python3

import socket

# Create server socket.
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)

# Bind server socket to loopback network interface.
serv_sock.bind(('', 5010))

# Turn server socket into listening mode.
serv_sock.listen(10)

while True:
    # Accept new connections in an infinite loop.
    client_sock, client_addr = serv_sock.accept()
    print('New connection from', client_addr)

    chunks = []
    while True:
        content = client_sock.recv(32)
        print(type(content))
        if len(content) ==0:
           break
 
        else:
            print(content)
            sensorcontet = content[0:1]
            sensorvalue = int.from_bytes(sensorcontet, byteorder='big')
    #print(chunks)
    #client_sock.sendall(b''.join(chunks))
    client_sock.close()
