# AI Client — OpenRouter CLI

Prosta aplikacja konsolowa w Pythonie do rozmowy z modelami AI przez API OpenRouter.

Użytkownik wybiera model przy starcie aplikacji, prowadzi rozmowę w terminalu, może zmienić model w trakcie działania oraz zapisuje historię rozmowy lokalnie.

## Funkcje

- komunikacja z API OpenRouter,
- wybór jednego z dostępnych modeli AI,
- zmiana modelu podczas rozmowy przez `/switch`,
- pamięć rozmowy zapisywana lokalnie w `data/historia.json`,
- prompt systemowy definiowany w `prompts.py`,
- logi aplikacji w `logs/app.log`,
- klucz API przechowywany w `.env`,
- testy modułu historii.

## Struktura projektu

```text
main.py          # uruchomienie aplikacji i obsługa komend
api.py           # komunikacja z OpenRouter
config.py        # konfiguracja API i parametrów modelu
models.py        # lista dostępnych modeli
history.py       # zapis i odczyt historii rozmowy
prompts.py       # instrukcja systemowa dla AI
logger.py        # konfiguracja logów
tests/           # testy automatyczne
data/            # lokalna historia rozmowy
logs/            # lokalne logi aplikacji

## Struktura projektu

1. Sklonuj repozytorium.

2. Utwórz i aktywuj środowisko wirtualne:
python -m venv .venv
.\.venv\Scripts\Activate.ps1

3. Zainstaluj zależności:
pip install -r requirements.txt

4. Utwórz plik .env na podstawie .env.example:
.\.venv\Scripts\python.exe main.py

Komendy
/exit — kończy program,
/clear — czyści rozmowę, zachowując prompt systemowy,
/save — ręcznie zapisuje historię,
/model — pokazuje aktualny model,
/switch — pozwala wybrać inny model.

Testy:
.\.venv\Scripts\python.exe -m unittest discover -s tests -v

Bezpieczeństwo
Nie umieszczaj klucza OpenRouter w kodzie ani w repozytorium. Plik .env powinien pozostać lokalny i jest ignorowany przez Git.