import sqlite3

DB_PATH = "sport_manager.db"


def connect_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            min_vitesse INTEGER NOT NULL,
            min_endurance INTEGER NOT NULL,
            min_force INTEGER NOT NULL,
            min_technique INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            speed INTEGER NOT NULL,
            endurance INTEGER NOT NULL,
            force INTEGER NOT NULL,
            technique INTEGER NOT NULL,
            position_id INTEGER,
            match_blessure_restants INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(team_id) REFERENCES teams(id) ON DELETE CASCADE,
            FOREIGN KEY(position_id) REFERENCES positions(id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team1_id INTEGER NOT NULL,
            team2_id INTEGER NOT NULL,
            score1 INTEGER NOT NULL,
            score2 INTEGER NOT NULL,
            played_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY(team1_id) REFERENCES teams(id),
            FOREIGN KEY(team2_id) REFERENCES teams(id)
        );

        CREATE TABLE IF NOT EXISTS match_players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            performance INTEGER NOT NULL,
            injured INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(match_id) REFERENCES matches(id) ON DELETE CASCADE,
            FOREIGN KEY(player_id) REFERENCES players(id) ON DELETE CASCADE
        );
        """
    )
    conn.commit()

if __name__ == "__main__":
    conn = connect_db()
    init_db(conn)