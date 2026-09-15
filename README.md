# Tic Tac Toe

A real-time multiplayer Tic Tac Toe game built with Flask and Socket.IO. Play against a friend in the browser, or against the computer.

## Features

- Real-time two-player matches over WebSockets — no page refresh needed
- Single-player mode against a bot
- Automatic matchmaking: the next player waiting becomes your opponent
- Responsive board that works on phones and desktop
- Live turn indicator, winning-line highlight, and reconnect handling

## Requirements

- Python 3.9 or newer

## Running it locally

```bash
# 1. Clone the repo
git clone git@github.com:ayyan915/tic-tac-toe.git
cd tic-tac-toe

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
python app.py
```

Then open `http://localhost:5000` in your browser.

To test two-player mode on one machine, open the site in a normal window and an incognito window — each one counts as a separate player.

## Project structure

```
.
├── app.py              # Flask routes and Socket.IO event handlers
├── requirements.txt
|
├── templates/
│   ├── home.html       # Menu: play a friend or the computer
│   ├── waiting.html    # Shown while waiting for an opponent to join
│   └── index.html      # The game board
└── README.md
```

## How it works

Each match lives in a Socket.IO room identified by a `room_id`. When a player opens the waiting screen they join that room; once two players are in, the server emits `ready_game` and both browsers navigate to the board.

Moves are sent as a `move` event containing the room, the cell position, and the player's id. The server validates the move, updates the board, and broadcasts `update_board` to everyone in the room, so both screens stay in sync.

## Roadmap

- Restart over WebSockets so both players get a fresh board at once
- Server-side turn validation
- Notify the remaining player when an opponent disconnects
- Scoreboard across multiple rounds

## License

MIT