# RoyalTest — Claude Code Guide

## Project Overview
A local-network poker game (Texas Hold'em) where one screen acts as the shared game table and each player uses their phone as a personal controller. No app install needed — pure browser-based via local WiFi.

## Tech Stack
- **Backend**: Python (Flask + Flask-SocketIO)
- **Frontend**: Vanilla HTML/CSS/JavaScript (no build tools)
- **Database**: SQLite (via Python's built-in `sqlite3` module)
- **Real-time**: Socket.IO (WebSockets over local LAN)
- **QR Code**: `qrcode` Python package (generate join URL on host screen)

## Architecture
- **Server** (`server/`) — runs on the host machine, manages all game logic (Single Source of Truth)
- **Host page** (`/host`) — displayed on TV/laptop, shows the table, community cards, pot, all players
- **Player page** (`/join`) — mobile-optimized, shows only the player's own cards + action buttons
- **Database** (`game.db`) — SQLite file auto-created on first run

## Folder Structure
```
server/
  app.py           ← Flask + Socket.IO server entry point
  game_engine.py   ← Poker logic (deal, validate, winners)
  bot_player.py    ← Bot AI classes (Rock, Maniac, Calculator)
  db.py            ← SQLite setup and queries
public/
  host/index.html  ← Host/TV display
  player/index.html← Mobile controller UI
  shared.css
game.db            ← SQLite file (auto-created, do not commit)
present.md         ← Original project brief (Hebrew)
```

## Key Design Decisions
- **Server validates every action** before applying — never trust the client
- **Polymorphic Player model**: `Player` base → `HumanPlayer` (waits for socket) / `BotPlayer` (instant algorithm)
- **No frontend framework** — plain HTML/JS to keep zero-install philosophy consistent
- **SQLite only** — no external DB server; the file lives next to the app
- **Mid-game join queue**: players who join while a game is active go into `join_queue` (server global); they are promoted into `current_game.players` at the start of the next hand via `_flush_queue()` called in `on_next_hand`

## Games
- Texas Hold'em Poker (primary)

## Bot Personalities (BotPlayer subclasses)
- **The Rock** — folds unless hand is very strong
- **The Maniac** — raises aggressively even with weak hands
- **The Calculator** — plays by hand-strength probability

## Database Schema (planned)
- `players` — nickname, games_played, wins, total_chips_won
- `game_logs` — game_id, winner, pot_size, timestamp, highlight data

## Development Phases
1. Flask server + Socket.IO basics — two browsers talking in real time ✅
2. Core poker game loop (deal, turns, validation, winner calculation) ✅
3. Host UI + Player UI ✅
3a. Mid-game join queue (players join next hand) ✅
4. QR code on host screen
5. SQLite persistence + name conflict resolution flow
6. Bots
7. End-of-session analytics/awards screen

## Running the Project
```bash
pip install flask flask-socketio qrcode pillow
python server/app.py
# Host opens: http://localhost:5000/host
# Players open: http://<host-ip>:5000/join  (or scan QR)
```

## Do Not
- Do not use a frontend framework (React, Vue, etc.)
- Do not use an external database server (PostgreSQL, MySQL)
- Do not add authentication — this is a trusted local LAN game
- Do not commit `game.db`
