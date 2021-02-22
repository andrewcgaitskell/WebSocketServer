import asyncio
import socketio

sio = socketio.AsyncClient()


@sio.event
async def connect():
    print('connected to server')
    await sio.emit('my event', {'data': 'foobar'})
    await sio.emit('message',"this is my first message")
    

@sio.event
async def disconnect():
    print('disconnected from server')


@sio.event
def hello(a, b, c):
    print(a, b, c)


async def start_server():
    await sio.connect('http://player2.acgtest.info:5006')
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(start_server())
    
