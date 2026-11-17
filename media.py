"""Obsługa modeli OpenRouter zwracających pliki (głos i obrazy)."""

import base64
import json
from datetime import datetime
from pathlib import Path

import requests

from config import (
    API_KEY,
    DEFAULT_MEDIA_OUTPUT_DIR,
    IMAGE_API_URL,
    MEDIA_SETTINGS_FILE,
    SPEECH_API_URL,
)
from logger import get_logger

logger = get_logger(__name__)

VOICE_MODEL = "heygen/heygen-voice-1-turbo:free"
VOICE_NAME = "nadine"
VOICE_RESPONSE_FORMAT = "pcm"
IMAGE_MODEL = "recraft/recraft-v4.1-flash-v2:free"


def get_media_output_dir():
    """Zwraca zapisany katalog wyjściowy lub katalog domyślny."""
    try:
        settings = json.loads(MEDIA_SETTINGS_FILE.read_text(encoding="utf-8"))
        output_dir = settings.get("media_output_dir")
        if isinstance(output_dir, str) and output_dir.strip():
            return Path(output_dir)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    return DEFAULT_MEDIA_OUTPUT_DIR


def set_media_output_dir(directory):
    """Zapisuje katalog, w którym będą umieszczane pliki odpowiedzi modeli."""
    output_dir = Path(directory).expanduser().resolve()
    MEDIA_SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    MEDIA_SETTINGS_FILE.write_text(
        json.dumps({"media_output_dir": str(output_dir)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_dir


def _headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


def _error_message(response):
    try:
        body = response.json()
        error = body.get("error", body) if isinstance(body, dict) else body
        if isinstance(error, dict):
            error = error.get("message", error)
        return str(error)
    except ValueError:
        return response.text[:500] or f"HTTP {response.status_code}"


def _output_file(suffix):
    directory = get_media_output_dir()
    directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return directory / f"{timestamp}{suffix}"


def _post_file(url, payload, suffix, decode_base64=False):
    if not API_KEY:
        print("Brak klucza OPENROUTER_API_KEY w pliku .env lub zmiennych środowiskowych.")
        return None

    try:
        response = requests.post(url, headers=_headers(), json=payload, timeout=120)
        if not response.ok:
            message = _error_message(response)
            print(f"Błąd API: {message}")
            logger.error("Błąd API plików: %s", message)
            return None

        content = base64.b64decode(response.json()["data"][0]["b64_json"]) if decode_base64 else response.content
        if not content:
            raise ValueError("API zwróciło pusty plik.")
        output_file = _output_file(suffix)
        output_file.write_bytes(content)
        return output_file
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError, OSError) as error:
        print(f"Nie udało się utworzyć pliku: {error}")
        logger.error("Nie udało się utworzyć pliku: %s", error)
        return None


def generate_speech(text):
    """Zamienia tekst na plik PCM wskazanym modelem HeyGen."""
    return _post_file(
        SPEECH_API_URL,
        {
            "model": VOICE_MODEL,
            "input": text,
            "voice": VOICE_NAME,
            "response_format": VOICE_RESPONSE_FORMAT,
        },
        ".pcm",
    )


def generate_image(prompt):
    """Generuje pojedynczy obraz wskazanym modelem Recraft."""
    return _post_file(
        IMAGE_API_URL,
        {
            "model": IMAGE_MODEL,
            "prompt": prompt,
            "aspect_ratio": "16:9",
            "n": 1,
        },
        ".png",
        decode_base64=True,
    )
