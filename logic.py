import random
import sqlite3
from typing import Optional

import db_queries
from display import ask_int, choose_from_list, header, pause, section_banner

INJURY_CHANCE = 0.5


def create_team(conn: sqlite3.Connection) -> None:
    header("Créer une équipe")
    name = input("Nom de l'équipe: ").strip()
    if not name:
        print("Nom obligatoire.")
        pause()
        return
    try:
        db_queries.insert_team(conn, name)
        print("Équipe créée.")
    except sqlite3.IntegrityError:
        print("Nom déjà utilisé.")
    pause()


def list_teams(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    header("Liste des équipes")
    section_banner("ÉQUIPES", "🏆")
    teams = db_queries.get_teams(conn)
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
    db_queries.update_team(conn, team_id, name)
    print("Équipe mise à jour.")
    pause()


def delete_team(conn: sqlite3.Connection) -> None:
    header("Supprimer une équipe")
    teams = list_teams(conn)
    team_id = choose_from_list(teams, "Supprimer une équipe")
    if not team_id:
        return
    db_queries.delete_team(conn, team_id)
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
        db_queries.insert_position(conn, name, min_vitesse, min_endurance, min_force, min_technique)
        print("Poste créé.")
    except sqlite3.IntegrityError:
        print("Nom déjà utilisé.")
    pause()


def list_positions(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    header("Liste des postes")
    section_banner("POSTES", "🧭")
    rows = db_queries.get_positions(conn)
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
    db_queries.update_position(
        conn,
        pos_id,
        name,
        min_vitesse,
        min_endurance,
        min_force,
        min_technique,
    )
    print("Poste mis à jour.")
    pause()


def delete_position(conn: sqlite3.Connection) -> None:
    header("Supprimer un poste")
    rows = list_positions(conn)
    pos_id = choose_from_list(rows, "Supprimer un poste")
    if not pos_id:
        return
    db_queries.delete_position(conn, pos_id)
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
                pos = db_queries.get_position(conn, pos_id)
                if (
                    pos
                    and speed >= pos["min_vitesse"]
                    and endurance >= pos["min_endurance"]
                    and force >= pos["min_force"]
                    and technique >= pos["min_technique"]
                ):
                    position_id = pos_id
                else:
                    print("Compétences insuffisantes pour ce poste.")
    db_queries.insert_player(
        conn,
        team_id,
        name,
        speed,
        endurance,
        force,
        technique,
        position_id,
    )
    print("Joueur créé.")
    pause()


def list_players(conn: sqlite3.Connection, team_id: Optional[int] = None) -> list[sqlite3.Row]:
    header("Liste des joueurs")
    section_banner("JOUEURS", "👟")
    rows = db_queries.get_players(conn, team_id)
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
    player = db_queries.get_player(conn, player_id)
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
                pos = db_queries.get_position(conn, pos_id)
                if (
                    pos
                    and speed >= pos["min_vitesse"]
                    and endurance >= pos["min_endurance"]
                    and force >= pos["min_force"]
                    and technique >= pos["min_technique"]
                ):
                    position_id = pos_id
                else:
                    print("Compétences insuffisantes pour ce poste.")
    db_queries.update_player(
        conn,
        player_id,
        name,
        speed,
        endurance,
        force,
        technique,
        position_id,
    )
    print("Joueur mis à jour.")
    pause()


def delete_player(conn: sqlite3.Connection) -> None:
    header("Supprimer un joueur")
    rows = list_players(conn)
    player_id = choose_from_list(rows, "Supprimer un joueur")
    if not player_id:
        return
    db_queries.delete_player(conn, player_id)
    print("Joueur supprimé.")
    pause()


def play_match(conn: sqlite3.Connection) -> None:
    header("Jouer un match")
    section_banner("CENTRE DU MATCH", "🎯")
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

    match_id = db_queries.insert_match(conn, team1_id, team2_id, score1, score2)

    players = db_queries.get_players_for_match(conn, team1_id, team2_id)
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
            db_queries.update_player_injury(conn, player["id"], restants)
            print(f"{player['name']} s'est blessé pour {restants} match(s).")
        db_queries.insert_match_player(conn, match_id, player["id"], performance, injured)

    conn.commit()
    db_queries.decrement_injuries(conn)
    print("Match enregistré.")
    pause()


def list_matches(conn: sqlite3.Connection) -> None:
    header("Historique des matchs")
    section_banner("MATCHS", "📊")
    rows = db_queries.get_matches(conn)
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
