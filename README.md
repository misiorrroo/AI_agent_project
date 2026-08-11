# AI_Client

Klient AI napisany w Pythonie, służący do komunikacji z modelami językowymi
przez API OpenRouter.

Projekt został zaprojektowany modułowo, tak aby poszczególne elementy
odpowiadające za konfigurację, komunikację z API, historię rozmowy,
modele oraz prompty były od siebie oddzielone.

---

## 📁 Struktura projektu

    AI_Client/
    │
    ├── main.py                 # Punkt wejścia programu
    │
    ├── config.py               # Konfiguracja aplikacji
    ├── api.py                  # Komunikacja z OpenRouter API
    ├── history.py              # Obsługa historii rozmów
    ├── models.py               # Definicje dostępnych modeli
    ├── prompts.py              # Gotowe prompty
    │
    ├── data/
    │   └── historia.json       # Zapisana historia rozmów
    │
    ├── tests/
    │   ├── __init__.py
    │   └── test_history.py     # Testy modułu history.py
    │
    ├── .env                    # Klucze API i zmienne środowiskowe
    ├── .gitignore              # Pliki ignorowane przez Git
    ├── requirements.txt        # Zależności projektu
    └── README.md               # Dokumentacja projektu

---

# ⚙️ Technologie

Projekt wykorzystuje:

- Python 3
- OpenRouter API
- `requests`
- `python-dotenv`
- `pathlib`
- `json`
- `logging`
- `unittest`

---

# 🧠 Architektura

Projekt jest podzielony na kilka odpowiedzialności.

## `main.py`

Główny punkt wejścia aplikacji.

Odpowiada za:

- uruchomienie programu,
- pobieranie danych od użytkownika,
- wywoływanie odpowiednich modułów,
- sterowanie przebiegiem rozmowy.

---

## `config.py`

Centralne miejsce konfiguracji aplikacji.

Przechowuje m.in.:

- klucz API,
- URL API,
- wybrany model,
- parametry requestów,
- ścieżki do plików.

Przykład:

    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent

    HISTORY_FILE = BASE_DIR / "data" / "historia.json"

---

## `api.py`

Odpowiada za komunikację HTTP z OpenRouter.

Schemat działania:

    Python
       │
       │ HTTP request
       ▼
    OpenRouter API
       │
       │ JSON response
       ▼
    Python

Moduł może odpowiadać za:

- tworzenie requestu,
- nagłówki HTTP,
- autoryzację,
- wysyłanie wiadomości,
- odbieranie odpowiedzi,
- obsługę błędów API.

---

## `history.py`

Odpowiada za pamięć rozmowy.

Historia jest przechowywana w pliku:

    data/historia.json

Przykładowa struktura:

    [
        {
            "role": "user",
            "content": "Czym jest Python?"
        },
        {
            "role": "assistant",
            "content": "Python jest językiem programowania..."
        }
    ]

Moduł powinien umożliwiać m.in.:

    load_history()
    save_history()
    add_message()
    clear_history()

---

## `models.py`

Zawiera informacje o dostępnych modelach.

Przykład:

    MODELS = {
        "model_1": "provider/model-name",
        "model_2": "provider/another-model",
    }

Dzięki temu zmiana modelu nie wymaga modyfikowania kodu odpowiedzialnego
za komunikację z API.

---

## `prompts.py`

Zawiera gotowe prompty i instrukcje systemowe.

Przykład:

    SYSTEM_PROMPT = """
    Jesteś pomocnym asystentem programistycznym.
    Odpowiadaj konkretnie i technicznie.
    """

Pozwala to oddzielić logikę aplikacji od treści promptów.

---

# 🔐 Konfiguracja API

Klucz API nie powinien znajdować się bezpośrednio w kodzie.

Tworzymy plik:

    .env

Przykład:

    OPENROUTER_API_KEY=twój_klucz_api

Następnie możemy użyć:

    from dotenv import load_dotenv
    import os

    load_dotenv()

    API_KEY = os.getenv("OPENROUTER_API_KEY")

---

# 📦 Instalacja

## 1. Klonowanie projektu

    git clone <adres-repozytorium>
    cd AI_Client

## 2. Utworzenie środowiska wirtualnego

### Windows

    python -m venv .venv

Aktywacja:

    .venv\Scripts\activate

### Linux

    python3 -m venv .venv
    source .venv/bin/activate

---

## 3. Instalacja zależności

    pip install -r requirements.txt

---

# ▶️ Uruchomienie

Program uruchamiamy:

    python main.py

---

# 🧪 Testy

Projekt wykorzystuje moduł:

    unittest

Uruchomienie wszystkich testów:

    python -m unittest discover

Można również uruchomić konkretny plik:

    python -m unittest tests.test_history

---

# 🧪 Przykład testowania historii

Przykładowy test:

    import tempfile
    import unittest
    from pathlib import Path
    from unittest.mock import patch

    import history


    class HistoryTests(unittest.TestCase):

        def setUp(self):
            self.temp_dir = tempfile.TemporaryDirectory()

            self.history_file = (
                Path(self.temp_dir.name)
                / "data"
                / "historia.json"
            )

            self.history_file_patch = patch.object(
                history,
                "HISTORY_FILE",
                self.history_file,
            )

            self.history_file_patch.start()

        def tearDown(self):
            self.history_file_patch.stop()
            self.temp_dir.cleanup()

        def test_save_and_load_history(self):
            # test
            pass

Wykorzystanie `TemporaryDirectory` powoduje, że testy nie modyfikują
prawdziwego pliku historii projektu.

---

# 📝 Logging

Do logowania aplikacja wykorzystuje standardową bibliotekę:

    import logging

Przykład:

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

Następnie:

    logging.info("Uruchomiono aplikację")
    logging.warning("Brak historii")
    logging.error("Błąd API")

Poziomy logowania:

    DEBUG
    INFO
    WARNING
    ERROR
    CRITICAL

---

# 🌐 Komunikacja z API

Ogólny schemat requestu:

    main.py
       │
       ▼
    api.py
       │
       │ POST
       ▼
    OpenRouter
       │
       │ JSON
       ▼
    api.py
       │
       ▼
    main.py

Przykładowe dane wysyłane do API:

    {
        "model": "provider/model",
        "messages": [
            {
                "role": "system",
                "content": "Jesteś pomocnym asystentem."
            },
            {
                "role": "user",
                "content": "Czym jest Python?"
            }
        ]
    }

---

# 💬 Historia rozmowy

Historia jest przekazywana do modelu jako lista wiadomości.

Przykład:

    SYSTEM
      ↓
    USER
      ↓
    ASSISTANT
      ↓
    USER
      ↓
    ASSISTANT

Dzięki temu model może uwzględniać wcześniejszy kontekst rozmowy.

---

# 🔄 Przepływ programu

Cała aplikacja działa w przybliżeniu tak:

    START
      │
      ▼
    main.py
      │
      ▼
    wczytanie config
      │
      ▼
    wczytanie historii
      │
      ▼
    użytkownik wpisuje wiadomość
      │
      ▼
    api.py
      │
      ▼
    OpenRouter API
      │
      ▼
    odpowiedź JSON
      │
      ▼
    zapis historii
      │
      ▼
    wyświetlenie odpowiedzi
      │
      ▼
    kolejna wiadomość

---

# 🛡️ Bezpieczeństwo

Do repozytorium nie należy dodawać:

    .env

ani:

    OPENROUTER_API_KEY

Dlatego `.gitignore` powinien zawierać np.:

    .env
    .venv/
    __pycache__/
    *.pyc

---

# 📄 requirements.txt

Przykładowo:

    requests
    python-dotenv

## requests

Służy do wykonywania żądań HTTP.

    import requests

## python-dotenv

Pozwala ładować zmienne środowiskowe z `.env`.

    from dotenv import load_dotenv

Pozostałe moduły, takie jak:

- `json`
- `pathlib`
- `logging`
- `unittest`

należą do standardowej biblioteki Pythona i nie wymagają instalowania przez
`pip`.

---

# 🧩 Zasada odpowiedzialności modułów

Najważniejsza zasada projektu:

    main.py
        ↓
    STEROWANIE APLIKACJĄ

    config.py
        ↓
    KONFIGURACJA

    api.py
        ↓
    KOMUNIKACJA Z API

    history.py
        ↓
    PAMIĘĆ ROZMOWY

    models.py
        ↓
    MODELE AI

    prompts.py
        ↓
    PROMPTY

    tests/
        ↓
    TESTY

Każdy moduł powinien mieć jedną główną odpowiedzialność.

Dzięki temu projekt można rozwijać bez tworzenia jednego ogromnego pliku
z całą logiką aplikacji.

---

# 🚀 Możliwy dalszy rozwój

Projekt można później rozbudować o:

- streaming odpowiedzi,
- wybór modelu z poziomu CLI,
- obsługę wielu rozmów,
- osobne pliki historii,
- token usage,
- koszt zapytań,
- automatyczne logowanie,
- retry requestów,
- timeouty,
- obsługę różnych providerów,
- obsługę tool/function calling,
- eksport rozmowy do Markdown/JSON,
- bazę SQLite/PostgreSQL zamiast JSON,
- testy API z mockami,
- asynchroniczne requesty,
- interfejs webowy,
- FastAPI jako backend,
- frontend React.

---

# 🎯 Cel projektu

Celem projektu jest stworzenie własnego, modularnego klienta AI,
który pozwala zrozumieć nie tylko samo wywoływanie modelu językowego,
ale również cały przepływ danych:

    Python
       ↓
    HTTP
       ↓
    API
       ↓
    JSON
       ↓
    LLM
       ↓
    JSON response
       ↓
    Python
       ↓
    Historia

Projekt ma być jednocześnie praktycznym klientem AI oraz ćwiczeniem z:

- Pythona,
- programowania obiektowego/funkcyjnego,
- API REST,
- HTTP,
- JSON,
- obsługi plików,
- zmiennych środowiskowych,
- loggingu,
- testów jednostkowych,
- Git,
- architektury aplikacji.