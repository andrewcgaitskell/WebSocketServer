##This code reads 1024*32(=32768) bytes in 32 iterations from the buffer which is received from Server in socket programming-python:
##jsonString = bytearray()
import time
from datetime import datetime

while True:

  for _ in range(32):

      packet = clisocket.recv(1024)
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

      with open(filename, "wb") as binary_file: 
          # Write bytes to file 
          binary_file.write(some_bytes)
