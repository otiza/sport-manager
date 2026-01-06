#!/usr/bin/env python3
from operations import (
    DIVIDER,
    clear_screen,
    create_player,
    create_position,
    create_team,
    delete_player,
    delete_position,
    delete_team,
    list_matches,
    list_players,
    list_positions,
    list_teams,
    play_match,
    update_player,
    update_position,
    update_team,
)
from schema import connect_db, init_db
from seed import seed_data


def main_menu() -> None:
    conn = connect_db()
    init_db(conn)
    menu = {
        "1": ("Créer une équipe", create_team),
        "2": ("Lister les équipes", list_teams),
        "3": ("Modifier une équipe", update_team),
        "4": ("Supprimer une équipe", delete_team),
        "5": ("Créer un poste", create_position),
        "6": ("Lister les postes", list_positions),
        "7": ("Modifier un poste", update_position),
        "8": ("Supprimer un poste", delete_position),
        "9": ("Créer un joueur", create_player),
        "10": ("Lister les joueurs", list_players),
        "11": ("Modifier un joueur", update_player),
        "12": ("Supprimer un joueur", delete_player),
        "13": ("Jouer un match", play_match),
        "14": ("Lister les matchs", list_matches),
        "15": ("Charger des données de test", seed_data),
        "0": ("Quitter", None),
    }
    while True:
        clear_screen()
        print(DIVIDER)
        print("Sport Manager CLI")
        print(DIVIDER)
        for key, (label, _) in menu.items():
            print(f"{key}. {label}")
        choice = input("Choix: ").strip()
        action = menu.get(choice)
        if not action:
            print("Choix invalide.")
            continue
        if choice == "0":
            print("Au revoir.")
            break
        func = action[1]
        if func:
            func(conn)


if __name__ == "__main__":
    main_menu()
