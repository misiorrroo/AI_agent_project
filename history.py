import json
import sqlite3
from json import JSONDecodeError
from typing import Any

from config import HISTORY_DB_FILE, HISTORY_FILE


def _connect() -> sqlite3.Connection:
    """Otwiera lokalną bazę i tworzy tabelę historii, jeśli jeszcze nie istnieje."""
    HISTORY_DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(HISTORY_DB_FILE)
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            position INTEGER NOT NULL UNIQUE,
            role TEXT NOT NULL,
            content TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS app_metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )
    return connection


def _valid_messages(messages: object) -> list[dict[str, str]]:
    """Zwraca tylko wiadomości zgodne z formatem API czatu."""
    if not isinstance(messages, list):
        return []

    return [
        {"role": message["role"], "content": message["content"]}
        for message in messages
        if isinstance(message, dict)
        and isinstance(message.get("role"), str)
        and isinstance(message.get("content"), str)
    ]


def _load_legacy_history() -> list[dict[str, str]]:
    """Odczytuje dawny plik JSON wyłącznie na potrzeby pierwszej migracji."""
    if not HISTORY_FILE.exists():
        return []

    try:
        with HISTORY_FILE.open("r", encoding="utf-8") as file:
            return _valid_messages(json.load(file))
    except (OSError, JSONDecodeError):
        return []


def _migrate_legacy_history(connection: sqlite3.Connection) -> None:
    """Przenosi dawną historię JSON tylko raz."""
    migrated = connection.execute(
        "SELECT 1 FROM app_metadata WHERE key = 'json_history_migrated'"
    ).fetchone()
    if migrated:
        return

    messages = _load_legacy_history()
    if messages:
        connection.executemany(
            "INSERT INTO messages (position, role, content) VALUES (?, ?, ?)",
            [
                (index, message["role"], message["content"])
                for index, message in enumerate(messages)
            ],
        )
    connection.execute(
        "INSERT INTO app_metadata (key, value) VALUES ('json_history_migrated', '1')"
    )
    connection.commit()


def load_history() -> list[dict[str, str]]:
    """Zwraca historię zapisaną w lokalnej bazie SQLite."""
    try:
        connection = _connect()
        try:
            _migrate_legacy_history(connection)
            rows = connection.execute(
                "SELECT role, content FROM messages ORDER BY position"
            ).fetchall()
        finally:
            connection.close()
    except sqlite3.Error:
        return []

    return [{"role": role, "content": content} for role, content in rows]


def save_history(messages: list[dict[str, Any]]) -> None:
    """Zastępuje historię nową listą wiadomości w jednej transakcji SQLite."""
    valid_messages = _valid_messages(messages)
    connection = _connect()
    try:
        connection.execute("DELETE FROM messages")
        connection.executemany(
            "INSERT INTO messages (position, role, content) VALUES (?, ?, ?)",
            [
                (index, message["role"], message["content"])
                for index, message in enumerate(valid_messages)
            ],
        )
        connection.commit()
    finally:
        connection.close()


def clear_history() -> None:
    """Usuwa wszystkie wiadomości z lokalnej historii."""
    connection = _connect()
    try:
        connection.execute("DELETE FROM messages")
        connection.commit()
    finally:
        connection.close()
