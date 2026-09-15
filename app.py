from extension import app, socketio, games
from sockets import handle_sockets
from routes.game import game


handle_sockets(socketio, games)
app.register_blueprint(game)
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)







