from flask import Blueprint, render_template, session, redirect
from extension import games, socketio
from game import Game
import uuid
from sockets import game_ready
from datetime import datetime, timedelta

game = Blueprint("game", __name__)

WAITING_TIMEOUT_SECONDS = 10


def waiting_rooms():
    for room_id, game in games.items():
        if game.player_count < 2:
            return room_id
    return None


@game.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@game.route("/play")
def play():
    room_id = waiting_rooms()
    if room_id is None:
        room_id = str(uuid.uuid4())[:6]
        games[room_id] = Game()

    player_id = str(uuid.uuid4())[:8]

    if games[room_id].player_count == 0:
        # First player: becomes X and waits for an opponent.
        games[room_id].players[player_id] = "X"
        games[room_id].player_count += 1

        session["player_id"] = player_id
        session["room_id"] = room_id
        # ISO format so it can be parsed straight back into a datetime later.
        session["waiting_start_time"] = datetime.now().isoformat()
        return redirect(f"/waiting/{room_id}")

    else:
        # Second player: becomes O, game starts immediately.
        games[room_id].players[player_id] = "O"
        games[room_id].player_count += 1

        session["player_id"] = player_id
        session["room_id"] = room_id
        game_ready(socketio, room_id)
        return redirect(f"/game/{room_id}")


@game.route("/waiting/<room_id>")
def waiting(room_id):
    if room_id not in games:
        return "Game not found", 404

    # Someone already joined (human or already-added bot) — no need to wait.
    if games[room_id].player_count >= 2:
        return redirect(f"/game/{room_id}")

    start_raw = session.get("waiting_start_time")
    if start_raw:
        start_time = datetime.fromisoformat(start_raw)
        if datetime.now() >= start_time + timedelta(seconds=WAITING_TIMEOUT_SECONDS):
            games[room_id].bot_enable = True
            games[room_id].players["bot"] = "O"
            games[room_id].player_count = 2
            return redirect(f"/game/{room_id}")

    return render_template("waiting.html", room_id=room_id, timeout_seconds=WAITING_TIMEOUT_SECONDS)


@game.route("/game/<room_id>")
def join_game(room_id):
    if room_id not in games:
        return "Game not found", 404

    # Frontend par player_id bhej rahe hain taake Socket events sahi se work karein
    player_id = session.get("player_id", "")
    return render_template("index.html", board=games[room_id].board, room_id=room_id, player_id=player_id)


@game.route("/restart/<room_id>", methods=["GET", "POST"])
def restart(room_id):
    if room_id in games:
        games[room_id].reset_board()
        games[room_id].current_player = "O" if games[room_id].current_player == "X" else "X"
        socketio.emit("update_board", {"board": games[room_id].board, "response": None}, to=room_id)
        if games[room_id].current_player == "O" and games[room_id].bot_enable:
            games[room_id].bot_move()
    return redirect(f"/game/{room_id}")


@game.route("/bot/play")
def bot():
    room_id = str(uuid.uuid4())[:6]
    games[room_id] = Game()
    games[room_id].bot_enable = True

    player_id = str(uuid.uuid4())[:8]

    games[room_id].players[player_id] = "X"
    games[room_id].players["bot"] = "O"
    games[room_id].player_count = 2

    session["player_id"] = player_id
    session["room_id"] = room_id

    return redirect(f"/game/{room_id}")