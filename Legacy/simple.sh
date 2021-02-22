#gunicorn -b 127.0.0.1:5002 --worker-class eventlet -w 1 server:app

gunicorn -b 0.0.0.0:5006 --worker-class eventlet -w 1 server:app
