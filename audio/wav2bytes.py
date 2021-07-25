## https://gist.github.com/hadware/8882b980907901426266cb07bfbfcd20

from scipy.io.wavfile import read, write
import io

## This may look a bit intricate/useless, considering the fact that scipy's read() and write() function already return a
## numpy ndarray, but the BytesIO "hack" may be useful in case you get the wav not through a file, but trough some websocket or
## HTTP Post request. This should obviously work with any other sound format, as long as you have the proper decoding function

with open("input_wav.wav", "rb") as wavfile:
    input_wav = wavfile.read()

# here, input_wav is a bytes object representing the wav object
rate, data = read(io.BytesIO(input_wav))

# data is a numpy ND array representing the audio data. Let's do some stuff with it
reversed_data = data[::-1] #reversing it

#then, let's save it to a BytesIO object, which is a buffer for bytes object
bytes_wav = bytes()
byte_io = io.BytesIO(bytes_wav)
write(byte_io, rate, reversed_data)

output_wav = byte_io.read() # and back to bytes, tadaaa
# output_wav can be written to a file, of sent over the network as a binary
