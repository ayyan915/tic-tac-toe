from flask import request
from flask_socketio import join_room, emit

def game_ready(socketio, room_id):
    socketio.emit("ready_game", {
            "room_id": room_id
        }, to=room_id)


def handle_sockets(socketio, games):
    @socketio.on("join")
    def join_game(data):
        room_id = data.get("room_id")
        if room_id in games:
            join_room(room_id)
            print(f"Player joined room: {room_id}")

    @socketio.on("move")
    def move(data):
        room_id = data.get("room_id")
        pos = int(data.get("pos"))
        player_id = data.get("player_id") # Socket event se player_id receive ki

        if room_id not in games:
            return

        game = games[room_id]
        
        if player_id not in game.players:
            return "you are not in this game"

        player_symbol = game.players[player_id]
        
        if player_symbol != game.current_player:
            # Sirf us bande ko error dikhao jisne ghalat turn chali
            emit("update_board", {
                "board": game.board,
                "response": {"status": "wrong", "msg": "It's not your turn!"}
            }, to=request.sid)
            return

        response = game.move_position(pos)
        if not response and game.bot_enable:
            if game.current_player == "O":
                response = game.bot_move()
        # Pure room me update broadcast karo
        socketio.emit("update_board",
            {
                "board": game.board,
                "response": response,
                "current_player": game.current_player
            },
            to=room_id
        )

