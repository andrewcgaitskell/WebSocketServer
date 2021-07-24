import SocketServer

class EchoHandler( SocketServer.StreamRequestHandler ):
    def handle(self):
        input= self.request.recv(1024)
        print "Input: %r" % ( input, )
        self.request.send("Heard: %r\n" % ( input, ) )

server= SocketServer.TCPServer( ("",5010), EchoHandler )
print "Starting Server"
server.serve_forever()
