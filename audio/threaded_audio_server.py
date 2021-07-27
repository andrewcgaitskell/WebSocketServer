# import socket programming library
import socket

# import thread module
from _thread import *
import threading

print_lock = threading.Lock()

# thread function
def threaded(c):
	while True:

		jsonString = bytearray()

		for _ in range(32):

			packet = c.recv(1024)
		if not packet:
			break
		jsonString.extend(packet)

		##Data resides in jsonString variable


		##some_bytes = b'\xC3\xA9'


		# Open in "wb" mode to 
		# write a new file, or  
		# "ab" mode to append 
		my_date = datetime.now()
		filename = my_date.isoformat()
		folder = '~/data/audio/'

		with open(filename, "wb") as binary_file: 
			# Write bytes to file 
			binary_file.write(jsonString)

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
