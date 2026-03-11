"""
db.py — Phase 4
SQLite persistence: player profiles, game logs, analytics.
"""
import os
import sqlite3

DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'game.db',
)
DB_PATH = os.getenv('ROYALTEST_DB_PATH', DEFAULT_DB_PATH)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    with get_connection() as conn:
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS players (
                nickname        TEXT PRIMARY KEY,
                games_played    INTEGER DEFAULT 0,
                wins            INTEGER DEFAULT 0,
                total_chips_won INTEGER DEFAULT 0,
                last_seen       TEXT
            );

            CREATE TABLE IF NOT EXISTS game_logs (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                played_at       TEXT DEFAULT (datetime('now')),
                winner          TEXT,
                pot_size        INTEGER,
                biggest_pot     INTEGER,
                rarest_hand     TEXT
            );
        ''')
    print('[db] Database ready.')


# ── Player queries ─────────────────────────────────────────────────────────────

def get_player(nickname: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            'SELECT * FROM players WHERE nickname = ?', (nickname,)
        ).fetchone()
        return dict(row) if row else None


def upsert_player(nickname: str):
    with get_connection() as conn:
        conn.execute('''
            INSERT INTO players (nickname, last_seen)
            VALUES (?, datetime('now'))
            ON CONFLICT(nickname) DO UPDATE SET last_seen = datetime('now')
        ''', (nickname,))


def record_win(nickname: str, chips_won: int):
    with get_connection() as conn:
        conn.execute('''
            UPDATE players
            SET wins = wins + 1,
                games_played = games_played + 1,
                total_chips_won = total_chips_won + ?
            WHERE nickname = ?
        ''', (chips_won, nickname))


def record_game_played(nickname: str):
    with get_connection() as conn:
        conn.execute('''
            UPDATE players SET games_played = games_played + 1 WHERE nickname = ?
        ''', (nickname,))


# ── Game log queries ───────────────────────────────────────────────────────────

def log_game(winner: str, pot_size: int, biggest_pot: int, rarest_hand: str | None = None):
    with get_connection() as conn:
        conn.execute('''
            INSERT INTO game_logs (winner, pot_size, biggest_pot, rarest_hand)
            VALUES (?, ?, ?, ?)
        ''', (winner, pot_size, biggest_pot, rarest_hand))
