import random
import sqlite3

from operations import header, pause
from schema import connect_db


def seed_data(conn: sqlite3.Connection) -> None:
    header("Charger des données de test")
    if conn.execute("SELECT COUNT(*) FROM teams").fetchone()[0] > 0:
        print("Des données existent déjà.")
        pause()
        return
    teams = ["Lions", "Tigres", "Panthères"]
    positions = [
        ("Attaquant", 60, 50, 40, 70),
        ("Défenseur", 40, 60, 70, 50),
        ("Milieu", 55, 65, 50, 60),
    ]
    conn.executemany("INSERT INTO teams (name) VALUES (?)", [(team,) for team in teams])
    conn.executemany(
        """
        INSERT INTO positions (name, min_vitesse, min_endurance, min_force, min_technique)
        VALUES (?, ?, ?, ?, ?)
        """,
        positions,
    )
    team_rows = conn.execute("SELECT id FROM teams ORDER BY id").fetchall()
    for team in team_rows:
        for index in range(1, 6):
            conn.execute(
                """
                INSERT INTO players (team_id, name, speed, endurance, force, technique)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    team["id"],
                    f"Joueur {team['id']}-{index}",
                    random.randint(40, 90),
                    random.randint(40, 90),
                    random.randint(40, 90),
                    random.randint(40, 90),
                ),
            )
    conn.commit()
    print("Données de démonstration ajoutées.")
    pause()

if __name__ == "__main__":
    conn = connect_db()
    seed_data(conn)