import os
import random
import sqlite3
from typing import Iterable, Optional

INJURY_CHANCE = 0.5
DIVIDER = "-" * 50


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pause() -> None:
    input("\nAppuyez sur Entrée pour continuer...")


def header(title: str) -> None:
    clear_screen()
    print(DIVIDER)
    print(title)
    print(DIVIDER)


def ask_int(prompt: str, minimum: Optional[int] = None, maximum: Optional[int] = None) -> int:
    while True:
        value = input(prompt).strip()
        if not value.isdigit():
            print("Veuillez saisir un nombre.")
            continue
        number = int(value)
        if minimum is not None and number < minimum:
            print(f"Valeur minimale: {minimum}.")
            continue
        if maximum is not None and number > maximum:
            print(f"Valeur maximale: {maximum}.")
            continue
        return number


def list_rows(conn: sqlite3.Connection, query: str, params: tuple = ()) -> list[sqlite3.Row]:
    return conn.execute(query, params).fetchall()


def choose_from_list(rows: list[sqlite3.Row], title: str) -> Optional[int]:
    if not rows:
        print(f"Aucun élément pour {title}.")
        return None
    print(f"\n{title}:")
    for row in rows:
        print(f"[{row['id']}] {row['name']}")
    return ask_int("Choisissez un ID: ")


def create_team(conn: sqlite3.Connection) -> None:
    header("Créer une équipe")
    name = input("Nom de l'équipe: ").strip()
    if not name:
        print("Nom obligatoire.")
        pause()
        return
    try:
        conn.execute("INSERT INTO teams (name) VALUES (?)", (name,))
        conn.commit()
        print("Équipe créée.")
    except sqlite3.IntegrityError:
        print("Nom déjà utilisé.")
    pause()


def list_teams(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    header("Liste des équipes")
    teams = list_rows(conn, "SELECT id, name FROM teams ORDER BY name")
    if not teams:
        print("Aucune équipe.")
    else:
        for team in teams:
            print(f"[{team['id']}] {team['name']}")
    pause()
    return teams


def update_team(conn: sqlite3.Connection) -> None:
    header("Modifier une équipe")
    teams = list_teams(conn)
    team_id = choose_from_list(teams, "Modifier une équipe")
    if not team_id:
        return
    name = input("Nouveau nom: ").strip()
    if not name:
        print("Nom obligatoire.")
        pause()
        return
    conn.execute("UPDATE teams SET name = ? WHERE id = ?", (name, team_id))
    conn.commit()
    print("Équipe mise à jour.")
    pause()


def delete_team(conn: sqlite3.Connection) -> None:
    header("Supprimer une équipe")
    teams = list_teams(conn)
    team_id = choose_from_list(teams, "Supprimer une équipe")
    if not team_id:
        return
    conn.execute("DELETE FROM teams WHERE id = ?", (team_id,))
    conn.commit()
    print("Équipe supprimée.")
    pause()


def create_position(conn: sqlite3.Connection) -> None:
    header("Créer un poste")
    name = input("Nom du poste: ").strip()
    if not name:
        print("Nom obligatoire.")
        pause()
        return
    min_vitesse = ask_int("Min vitesse (0-100): ", 0, 100)
    min_endurance = ask_int("Min endurance (0-100): ", 0, 100)
    min_force = ask_int("Min force (0-100): ", 0, 100)
    min_technique = ask_int("Min technique (0-100): ", 0, 100)
    try:
        conn.execute(
            """
            INSERT INTO positions (name, min_vitesse, min_endurance, min_force, min_technique)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, min_vitesse, min_endurance, min_force, min_technique),
        )
        conn.commit()
        print("Poste créé.")
    except sqlite3.IntegrityError:
        print("Nom déjà utilisé.")
    pause()


def list_positions(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    header("Liste des postes")
    rows = list_rows(
        conn,
        """
        SELECT id, name, min_vitesse, min_endurance, min_force, min_technique
        FROM positions ORDER BY name
        """,
    )
    if not rows:
        print("Aucun poste.")
    else:
        for pos in rows:
            print(
                f"[{pos['id']}] {pos['name']} (V:{pos['min_vitesse']} E:{pos['min_endurance']} "
                f"F:{pos['min_force']} T:{pos['min_technique']})"
            )
    pause()
    return rows


def update_position(conn: sqlite3.Connection) -> None:
    header("Modifier un poste")
    rows = list_positions(conn)
    pos_id = choose_from_list(rows, "Modifier un poste")
    if not pos_id:
        return
    name = input("Nouveau nom: ").strip()
    if not name:
        print("Nom obligatoire.")
        pause()
        return
    min_vitesse = ask_int("Min vitesse (0-100): ", 0, 100)
    min_endurance = ask_int("Min endurance (0-100): ", 0, 100)
    min_force = ask_int("Min force (0-100): ", 0, 100)
    min_technique = ask_int("Min technique (0-100): ", 0, 100)
    conn.execute(
        """
        UPDATE positions
        SET name = ?, min_vitesse = ?, min_endurance = ?, min_force = ?, min_technique = ?
        WHERE id = ?
        """,
        (name, min_vitesse, min_endurance, min_force, min_technique, pos_id),
    )
    conn.commit()
    print("Poste mis à jour.")
    pause()


def delete_position(conn: sqlite3.Connection) -> None:
    header("Supprimer un poste")
    rows = list_positions(conn)
    pos_id = choose_from_list(rows, "Supprimer un poste")
    if not pos_id:
        return
    conn.execute("DELETE FROM positions WHERE id = ?", (pos_id,))
    conn.commit()
    print("Poste supprimé.")
    pause()


def create_player(conn: sqlite3.Connection) -> None:
    header("Créer un joueur")
    teams = list_teams(conn)
    team_id = choose_from_list(teams, "Choisir l'équipe")
    if not team_id:
        return
    name = input("Nom du joueur: ").strip()
    if not name:
        print("Nom obligatoire.")
        pause()
        return
    speed = ask_int("Vitesse (0-100): ", 0, 100)
    endurance = ask_int("Endurance (0-100): ", 0, 100)
    force = ask_int("Force (0-100): ", 0, 100)
    technique = ask_int("Technique (0-100): ", 0, 100)
    position_id = None
    positions = list_positions(conn)
    if positions:
        assign = input("Assigner un poste ? (o/n): ").strip().lower()
        if assign == "o":
            pos_id = choose_from_list(positions, "Choisir un poste")
            if pos_id:
                pos = conn.execute("SELECT * FROM positions WHERE id = ?", (pos_id,)).fetchone()
                if pos and speed >= pos["min_vitesse"] and endurance >= pos["min_endurance"] and force >= pos["min_force"] and technique >= pos["min_technique"]:
                    position_id = pos_id
                else:
                    print("Compétences insuffisantes pour ce poste.")
    conn.execute(
        """
        INSERT INTO players (team_id, name, speed, endurance, force, technique, position_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (team_id, name, speed, endurance, force, technique, position_id),
    )
    conn.commit()
    print("Joueur créé.")
    pause()


def list_players(conn: sqlite3.Connection, team_id: Optional[int] = None) -> list[sqlite3.Row]:
    header("Liste des joueurs")
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
    rows = list_rows(conn, query, params)
    if not rows:
        print("Aucun joueur.")
    else:
        for player in rows:
            pos = player["position_name"] or "Sans poste"
            bless = player["match_blessure_restants"]
            print(
                f"[{player['id']}] {player['name']} ({player['team_name']}) - {pos} "
                f"V:{player['speed']} E:{player['endurance']} F:{player['force']} "
                f"T:{player['technique']} Blessure:{bless}"
            )
    pause()
    return rows


def update_player(conn: sqlite3.Connection) -> None:
    header("Modifier un joueur")
    rows = list_players(conn)
    player_id = choose_from_list(rows, "Modifier un joueur")
    if not player_id:
        return
    player = conn.execute("SELECT * FROM players WHERE id = ?", (player_id,)).fetchone()
    if not player:
        print("Joueur introuvable.")
        pause()
        return
    name = input(f"Nom ({player['name']}): ").strip() or player["name"]
    speed = ask_int(f"Vitesse ({player['speed']}): ", 0, 100)
    endurance = ask_int(f"Endurance ({player['endurance']}): ", 0, 100)
    force = ask_int(f"Force ({player['force']}): ", 0, 100)
    technique = ask_int(f"Technique ({player['technique']}): ", 0, 100)
    positions = list_positions(conn)
    position_id = player["position_id"]
    if positions:
        assign = input("Assigner ou changer le poste ? (o/n): ").strip().lower()
        if assign == "o":
            pos_id = choose_from_list(positions, "Choisir un poste")
            if pos_id:
                pos = conn.execute("SELECT * FROM positions WHERE id = ?", (pos_id,)).fetchone()
                if pos and speed >= pos["min_vitesse"] and endurance >= pos["min_endurance"] and force >= pos["min_force"] and technique >= pos["min_technique"]:
                    position_id = pos_id
                else:
                    print("Compétences insuffisantes pour ce poste.")
    conn.execute(
        """
        UPDATE players
        SET name = ?, speed = ?, endurance = ?, force = ?, technique = ?, position_id = ?
        WHERE id = ?
        """,
        (name, speed, endurance, force, technique, position_id, player_id),
    )
    conn.commit()
    print("Joueur mis à jour.")
    pause()


def delete_player(conn: sqlite3.Connection) -> None:
    header("Supprimer un joueur")
    rows = list_players(conn)
    player_id = choose_from_list(rows, "Supprimer un joueur")
    if not player_id:
        return
    conn.execute("DELETE FROM players WHERE id = ?", (player_id,))
    conn.commit()
    print("Joueur supprimé.")
    pause()


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


def play_match(conn: sqlite3.Connection) -> None:
    header("Jouer un match")
    teams = list_teams(conn)
    if len(teams) < 2:
        print("Il faut au moins deux équipes.")
        pause()
        return
    team1_id = choose_from_list(teams, "Choisir l'équipe 1")
    if not team1_id:
        return
    team2_id = choose_from_list(teams, "Choisir l'équipe 2")
    if not team2_id or team2_id == team1_id:
        print("Choix invalide.")
        pause()
        return
    score1 = ask_int("Score équipe 1: ", 0)
    score2 = ask_int("Score équipe 2: ", 0)

    conn.execute(
        "INSERT INTO matches (team1_id, team2_id, score1, score2) VALUES (?, ?, ?, ?)",
        (team1_id, team2_id, score1, score2),
    )
    match_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    players = list_rows(
        conn,
        """
        SELECT * FROM players
        WHERE team_id IN (?, ?)
        ORDER BY team_id, name
        """,
        (team1_id, team2_id),
    )
    if not players:
        print("Aucun joueur pour ce match.")
        pause()
        return

    for player in players:
        if player["match_blessure_restants"] > 0:
            print(
                f"{player['name']} est blessé (reste {player['match_blessure_restants']} match(s))."
            )
            continue
        performance = ask_int(
            f"Performance de {player['name']} (0-10): ",
            0,
            10,
        )
        injured = 1 if random.random() < INJURY_CHANCE else 0
        if injured:
            restants = random.randint(1, 3)
            conn.execute(
                "UPDATE players SET match_blessure_restants = ? WHERE id = ?",
                (restants, player["id"]),
            )
            print(f"{player['name']} s'est blessé pour {restants} match(s).")
        conn.execute(
            """
            INSERT INTO match_players (match_id, player_id, performance, injured)
            VALUES (?, ?, ?, ?)
            """,
            (match_id, player["id"], performance, injured),
        )

    conn.commit()
    decrement_injuries(conn)
    print("Match enregistré.")
    pause()


def list_matches(conn: sqlite3.Connection) -> None:
    header("Historique des matchs")
    rows = list_rows(
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
    if not rows:
        print("Aucun match.")
        pause()
        return
    for match in rows:
        print(
            f"[{match['id']}] {match['team1']} {match['score1']} - "
            f"{match['score2']} {match['team2']} ({match['played_at']})"
        )
    pause()
