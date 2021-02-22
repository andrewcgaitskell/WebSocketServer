import asyncio
import aiohttp
from aiohttp import web

async def hello(request):
    return web.Response(body=b"Hello, world")

async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    while not ws.closed:
        msg = await ws.receive()

        if msg.type == aiohttp.WSMsgType.text:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.close:
            print('websocket connection closed')
        elif msg.type == aiohttp.WSMsgType.error:
            print('ws connection closed with exception %s' %
                  ws.exception())

    return ws
##


app = web.Application()
app.router.add_route('GET', '/', hello)
app.router.add_route('GET', '/ws/', websocket_handler)

loop = asyncio.get_event_loop()
handler = app.make_handler()
####


f = loop.create_server(handler, '0.0.0.0', 5010)
srv = loop.run_until_complete(f)
print('serving on', srv.sockets[0].getsockname())

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.run_until_complete(handler.finish_connections(1.0))
    srv.close()
    loop.run_until_complete(srv.wait_closed())
    loop.run_until_complete(app.finish())
loop.close()
