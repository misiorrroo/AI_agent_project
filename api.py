import requests

from config import (
    API_KEY,
    API_URL,
    MODEL,
    TEMPERATURE,
    TOP_P,
    MAX_TOKENS,
    FREQUENCY_PENALTY,
    PRESENCE_PENALTY,
)
from logger import get_logger

logger = get_logger(__name__)

def ask_ai(messages):
    """Wysyła historię rozmowy do modelu i zwraca tekst odpowiedzi."""

    if not API_KEY:
        print("Brak klucza OPENROUTER_API_KEY w pliku .env lub zmiennych środowiskowych.")
        return None

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": MAX_TOKENS,
        "frequency_penalty": FREQUENCY_PENALTY,
        "presence_penalty": PRESENCE_PENALTY,
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=data,
            timeout=400,
        )
        response.raise_for_status()

        result = response.json()
        return result["choices"][0]["message"]["content"]

    except requests.RequestException as error:
        print(f"Błąd połączenia z API: {error}")
        logger.error("Błąd połączenia z API: %s", error)
        return None

    except (KeyError, IndexError, ValueError) as error:
        print(f"Nieprawidłowa odpowiedź API: {error}")
        logger.error("Nieprawidłowa odpowiedź API: %s", error)
        return None