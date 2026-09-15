import os
from extension import app, socketio, games
from sockets import handle_sockets
from routes.game import game


handle_sockets(socketio, games)
app.register_blueprint(game)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    socketio.run(app, host="0.0.0.0", port=port, debug=debug)
