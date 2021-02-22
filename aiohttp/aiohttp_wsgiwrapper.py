from aiohttp import web
from aiohttp_wsgi import WSGIHandler
from asyncio_webserver import application

wsgi_handler = WSGIHandler(application)

def init_func(argv):
    app = web.Application()
    app.router.add_route("*", "/{path_info:.*}", wsgi_handler)
    web.run_app(app)
    return app
