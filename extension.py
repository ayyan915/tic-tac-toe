import os
from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
games = {}