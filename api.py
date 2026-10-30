import requests

from config import (
    API_KEY,
    API_URL,
    TEMPERATURE,
    TOP_P,
    MAX_TOKENS,
    FREQUENCY_PENALTY,
    PRESENCE_PENALTY,
)
from logger import get_logger

logger = get_logger(__name__)


def _api_error_details(response):
    """Zwraca krótki opis błędu udostępniony przez API, jeśli jest dostępny."""

    try:
        body = response.json()
    except ValueError:
        return None

    if not isinstance(body, dict):
        return None

    error = body.get("error")
    if isinstance(error, dict):
        message = error.get("message")
    elif isinstance(error, str):
        message = error
    else:
        message = body.get("message")

    if isinstance(message, str) and message.strip():
        return message.strip()[:500]
    return None


def _http_error_message(error):
    response = error.response
    status_code = response.status_code if response is not None else None
    details = _api_error_details(response) if response is not None else None

    messages = {
        401: "Nieprawidłowy lub wygasły klucz API. (HTTP response 401)",
        403: "Brak uprawnień do korzystania z API lub wybranego modelu. (HTTP response 403)",
        404: "Nie znaleziono endpointu API lub wybranego modelu. (HTTP response 404)",
        408: "Przekroczono czas oczekiwania na odpowiedź API. (HTTP response 408)",
        429: "Przekroczono limit zapytań lub środków API. (HTTP response 429)",
    }

    if status_code in messages:
        message = messages[status_code]
    elif status_code is not None and status_code >= 500:
        message = "Usługa API jest chwilowo niedostępna."
    else:
        message = "API odrzuciło zapytanie."

    if details:
        message = f"{message} Szczegóły: {details}"
    elif status_code is not None:
        message = f"{message} (HTTP {status_code})"

    return message


def ask_ai(messages, model):
    """Wysyła historię rozmowy do modelu i zwraca tekst odpowiedzi."""

    if not API_KEY:
        message = "Brak klucza OPENROUTER_API_KEY w pliku .env lub zmiennych środowiskowych."
        print(message)
        logger.error(message)
        return None

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": model,
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
            timeout=60,
        )
        response.raise_for_status()

        result = response.json()
        content = result["choices"][0]["message"]["content"]
        if not isinstance(content, str):
            raise ValueError("Pole z treścią odpowiedzi nie jest tekstem.")
        return content

    except requests.HTTPError as error:
        message = _http_error_message(error)
        print(f"Błąd API: {message}")
        logger.error("Błąd API: %s", message)
        return None

    except requests.Timeout as error:
        message = "Przekroczono czas oczekiwania na odpowiedź API."
        print(message)
        logger.error("%s %s", message, error)
        return None

    except requests.RequestException as error:
        print(f"Błąd połączenia z API: {error}")
        logger.error("Błąd połączenia z API: %s", error)
        return None

    except (KeyError, IndexError, TypeError, ValueError) as error:
        message = "Nieprawidłowa odpowiedź API."
        print(message)
        logger.error("Nieprawidłowa odpowiedź API: %s", error)
        return None
