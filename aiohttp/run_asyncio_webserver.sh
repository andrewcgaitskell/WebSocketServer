#gunicorn asyncio_webserver:app --bind 0.0.0.0:5010 --worker-class aiohttp.worker.GunicornWebWorker

gunicorn asyncio_webserver:app --worker-class aiohttp.worker.GunicornWebWorker
