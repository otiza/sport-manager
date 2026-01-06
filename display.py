import os
import shutil
import sqlite3
from typing import Optional

DEFAULT_WIDTH = 70


def get_terminal_width() -> int:
    return shutil.get_terminal_size((DEFAULT_WIDTH, 20)).columns


def center_text(text: str, width: Optional[int] = None) -> str:
    return text.center(width or get_terminal_width())


def print_logo(width: Optional[int] = None) -> None:
    width = width or get_terminal_width()
    logo = [
        "⚽🏟️  SPORT MANAGER  🏟️⚽",
        "★☆★  Vivez le match au centre du terrain  ★☆★",
    ]
    for line in logo:
        print(center_text(line, width))


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pause() -> None:
    input("\nAppuyez sur Entrée pour continuer...")


def header(title: str) -> None:
    clear_screen()
    width = get_terminal_width()
    divider = "═" * width
    print(divider)
    print_logo(width)
    print(center_text(title.upper(), width))
    print(divider)


def section_banner(title: str, icon: str) -> None:
    width = get_terminal_width()
    banner = f"{icon}  {title}  {icon}"
    print(center_text(banner, width))
    print(center_text("·" * len(banner), width))


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


def choose_from_list(rows: list[sqlite3.Row], title: str) -> Optional[int]:
    if not rows:
        print(f"Aucun élément pour {title}.")
        return None
    print(f"\n{title}:")
    for row in rows:
        print(f"[{row['id']}] {row['name']}")
    return ask_int("Choisissez un ID: ")
