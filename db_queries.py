import sqlite3
from typing import Optional


def list_rows(conn: sqlite3.Connection, query: str, params: tuple = ()) -> list[sqlite3.Row]:
    return conn.execute(query, params).fetchall()


def insert_team(conn: sqlite3.Connection, name: str) -> None:
    conn.execute("INSERT INTO teams (name) VALUES (?)", (name,))
    conn.commit()


def get_teams(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return list_rows(conn, "SELECT id, name FROM teams ORDER BY name")


def update_team(conn: sqlite3.Connection, team_id: int, name: str) -> None:
    conn.execute("UPDATE teams SET name = ? WHERE id = ?", (name, team_id))
    conn.commit()


def delete_team(conn: sqlite3.Connection, team_id: int) -> None:
    conn.execute("DELETE FROM teams WHERE id = ?", (team_id,))
    conn.commit()


def insert_position(
    conn: sqlite3.Connection,
    name: str,
    min_vitesse: int,
    min_endurance: int,
    min_force: int,
    min_technique: int,
) -> None:
    conn.execute(
        """
        INSERT INTO positions (name, min_vitesse, min_endurance, min_force, min_technique)
        VALUES (?, ?, ?, ?, ?)
        """,
        (name, min_vitesse, min_endurance, min_force, min_technique),
    )
    conn.commit()


def get_positions(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return list_rows(
        conn,
        """
        SELECT id, name, min_vitesse, min_endurance, min_force, min_technique
        FROM positions ORDER BY name
        """,
    )


def get_position(conn: sqlite3.Connection, position_id: int) -> Optional[sqlite3.Row]:
    return conn.execute("SELECT * FROM positions WHERE id = ?", (position_id,)).fetchone()


def update_position(
    conn: sqlite3.Connection,
    position_id: int,
    name: str,
    min_vitesse: int,
    min_endurance: int,
    min_force: int,
    min_technique: int,
) -> None:
    conn.execute(
        """
        UPDATE positions
        SET name = ?, min_vitesse = ?, min_endurance = ?, min_force = ?, min_technique = ?
        WHERE id = ?
        """,
        (name, min_vitesse, min_endurance, min_force, min_technique, position_id),
    )
    conn.commit()


def delete_position(conn: sqlite3.Connection, position_id: int) -> None:
    conn.execute("DELETE FROM positions WHERE id = ?", (position_id,))
    conn.commit()


def insert_player(
    conn: sqlite3.Connection,
    team_id: int,
    name: str,
    speed: int,
    endurance: int,
    force: int,
    technique: int,
    position_id: Optional[int],
) -> None:
    conn.execute(
        """
        INSERT INTO players (team_id, name, speed, endurance, force, technique, position_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (team_id, name, speed, endurance, force, technique, position_id),
    )
    conn.commit()


def get_players(conn: sqlite3.Connection, team_id: Optional[int] = None) -> list[sqlite3.Row]:
    query = (
        """
        SELECT players.id, players.name, teams.name AS team_name, players.speed, players.endurance,
               players.force, players.technique, players.match_blessure_restants,
               positions.name AS position_name
        FROM players
        JOIN teams ON teams.id = players.team_id
        LEFT JOIN positions ON positions.id = players.position_id
        """
    )
    params: tuple = ()
    if team_id:
        query += " WHERE players.team_id = ?"
        params = (team_id,)
    query += " ORDER BY teams.name, players.name"
    return list_rows(conn, query, params)


def get_player(conn: sqlite3.Connection, player_id: int) -> Optional[sqlite3.Row]:
    return conn.execute("SELECT * FROM players WHERE id = ?", (player_id,)).fetchone()


def update_player(
    conn: sqlite3.Connection,
    player_id: int,
    name: str,
    speed: int,
    endurance: int,
    force: int,
    technique: int,
    position_id: Optional[int],
) -> None:
    conn.execute(
        """
        UPDATE players
        SET name = ?, speed = ?, endurance = ?, force = ?, technique = ?, position_id = ?
        WHERE id = ?
        """,
        (name, speed, endurance, force, technique, position_id, player_id),
    )
    conn.commit()


def delete_player(conn: sqlite3.Connection, player_id: int) -> None:
    conn.execute("DELETE FROM players WHERE id = ?", (player_id,))
    conn.commit()


def insert_match(
    conn: sqlite3.Connection,
    team1_id: int,
    team2_id: int,
    score1: int,
    score2: int,
) -> int:
    conn.execute(
        "INSERT INTO matches (team1_id, team2_id, score1, score2) VALUES (?, ?, ?, ?)",
        (team1_id, team2_id, score1, score2),
    )
    return conn.execute("SELECT last_insert_rowid()").fetchone()[0]


def get_players_for_match(
    conn: sqlite3.Connection,
    team1_id: int,
    team2_id: int,
) -> list[sqlite3.Row]:
    return list_rows(
        conn,
        """
        SELECT * FROM players
        WHERE team_id IN (?, ?)
        ORDER BY team_id, name
        """,
        (team1_id, team2_id),
    )


def update_player_injury(conn: sqlite3.Connection, player_id: int, restants: int) -> None:
    conn.execute(
        "UPDATE players SET match_blessure_restants = ? WHERE id = ?",
        (restants, player_id),
    )


def insert_match_player(
    conn: sqlite3.Connection,
    match_id: int,
    player_id: int,
    performance: int,
    injured: int,
) -> None:
    conn.execute(
        """
        INSERT INTO match_players (match_id, player_id, performance, injured)
        VALUES (?, ?, ?, ?)
        """,
        (match_id, player_id, performance, injured),
    )


def decrement_injuries(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        UPDATE players
        SET match_blessure_restants = CASE
            WHEN match_blessure_restants > 0 THEN match_blessure_restants - 1
            ELSE 0
        END
        """
    )
    conn.commit()


def get_matches(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return list_rows(
        conn,
        """
        SELECT matches.id, t1.name AS team1, t2.name AS team2,
               matches.score1, matches.score2, matches.played_at
        FROM matches
        JOIN teams t1 ON t1.id = matches.team1_id
        JOIN teams t2 ON t2.id = matches.team2_id
        ORDER BY matches.played_at DESC
        """,
    )
