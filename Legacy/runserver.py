from server import app

PORT = 5006;
ADDRESS = '127.0.0.1'
#ADDRESS = '0.0.0.0'

if __name__ == '__main__':
    socketio.run(app,port=5001,use_reloader=False, debug=False)
