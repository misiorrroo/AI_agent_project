import json
import os
from json import JSONDecodeError
from typing import Any

from config import HISTORY_FILE


def load_history() -> list[dict[str, Any]]:
    """Zwraca zapisaną historię lub pustą listę, jeśli nie można jej odczytać."""
    if not HISTORY_FILE.exists():
        return []

    try:
        with HISTORY_FILE.open("r", encoding="utf-8") as file:
            messages = json.load(file)
    except (OSError, JSONDecodeError):
        return []

    if not isinstance(messages, list):
        return []

    return [
        message
        for message in messages
        if isinstance(message, dict)
        and isinstance(message.get("role"), str)
        and isinstance(message.get("content"), str)
    ]


def save_history(messages: list[dict[str, Any]]) -> None:
    """Zapisuje historię atomowo, aby przerwany zapis nie uszkodził pliku."""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary_file = HISTORY_FILE.with_suffix(".tmp")

    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(
            messages,
            file,
            indent=4,
            ensure_ascii=False,
        )
        file.write("\n")

    os.replace(temporary_file, HISTORY_FILE)


def clear_history() -> None:
    """Usuwa zapis rozmowy, zachowując pusty, prawidłowy plik JSON."""
    save_history([])
