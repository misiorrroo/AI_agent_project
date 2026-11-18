# AI Client

Konsolowy klient Python do korzystania z modeli dostępnych przez OpenRouter. Program obsługuje rozmowę tekstową z pamięcią historii, generowanie obrazów oraz zamianę tekstu na mowę.

## Funkcje

- rozmowa z wybranym modelem językowym OpenRouter;
- zapisywanie historii rozmowy w lokalnej bazie SQLite;
- automatyczna, jednorazowa migracja dawnej historii z `data/historia.json`;
- zmiana modelu w trakcie działania programu;
- generowanie obrazów PNG;
- generowanie mowy w formacie PCM;
- wybór i trwałe zapamiętanie katalogu dla wygenerowanych plików;
- obsługa błędów API, limitów zapytań i problemów z połączeniem;
- logowanie zdarzeń aplikacji.

## Wymagania

- Python 3;
- klucz API OpenRouter;
- zależności z pliku `requirements.txt`.

## Instalacja

```powershell
git clone <adres-repozytorium>
cd AI_agent_project
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

W systemach Linux i macOS aktywacja środowiska wygląda następująco:

```bash
source .venv/bin/activate
```

## Konfiguracja

Utwórz własny klucz w [panelu kluczy OpenRouter](https://openrouter.ai/keys).
Następnie skopiuj plik `.env.example` jako `.env` i podaj w nim klucz:

```env
OPENROUTER_API_KEY=twój_klucz_api
```

Plik `.env` zawiera sekret i nie powinien być dodawany do repozytorium.

Parametry zapytań tekstowych są ustawiane w `config.py`:

- `TEMPERATURE=1`
- `TOP_P=0.82`
- `MAX_TOKENS=5000`
- `FREQUENCY_PENALTY=0.1`
- `PRESENCE_PENALTY=0.1`

## Uruchomienie

```powershell
python main.py
```

## Docker

Ta metoda nie wymaga samodzielnej instalacji Pythona ani pakietów z
`requirements.txt` — są one instalowane wewnątrz kontenera. Potrzebny jest
jedynie Docker Desktop.

> Docker Desktop musi być uruchomiony przed wykonaniem poleceń poniżej. Na
> Windows po instalacji otwórz aplikację i zaczekaj, aż jej status będzie
> wskazywał, że silnik Docker działa.

### Pierwsze uruchomienie krok po kroku

1. Zainstaluj [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   dla swojego systemu i uruchom go.
2. Otwórz PowerShell w katalogu projektu. Jeżeli terminal jest otwarty gdzie
   indziej, przejdź do projektu poleceniem:

   ```powershell
   cd "C:\ścieżka\do\AI_agent_project"
   ```

3. Utwórz lokalny plik konfiguracyjny na podstawie szablonu:

   ```powershell
   Copy-Item .env.example .env
   ```

4. Otwórz plik `.env` w edytorze i wpisz swój klucz OpenRouter po znaku `=`:

   ```env
   OPENROUTER_API_KEY=tu_wklej_swoj_klucz
   ```

   Nie umieszczaj spacji ani cudzysłowów wokół klucza. Plik `.env` zawiera
   sekret, jest ignorowany przez Git i nie trafia do obrazu Docker.

5. Zbuduj obraz aplikacji. Przy pierwszym uruchomieniu Docker pobierze obraz
   Pythona oraz pakiety, więc może to potrwać kilka minut:

```powershell
docker compose build
```

6. Uruchom program:

```powershell
docker compose run --rm ai-client
```

Po uruchomieniu wybierz model, wpisując cyfrę, albo naciśnij Enter, aby użyć
modelu domyślnego. Aby zakończyć program, wpisz `/exit`.

### Co dzieje się z plikami?

Docker uruchamia aplikację w odizolowanym kontenerze. Dwa katalogi projektu są
jednak celowo udostępnione kontenerowi, dzięki czemu ich zawartość zostaje na
komputerze także po zamknięciu programu:

| Katalog lokalny | Zawartość |
| --- | --- |
| `data/` | historia rozmów, ustawienia oraz wygenerowane obrazy i nagrania |
| `logs/` | plik dziennika `app.log` z komunikatami aplikacji |

Parametr `--rm` usuwa tylko zakończony kontener tymczasowy; nie usuwa tych
katalogów ani zbudowanego obrazu. Aplikacja wymaga interakcji w terminalu,
dlatego uruchamiaj ją przez `docker compose run`, a nie `docker compose up`.

### Kolejne uruchomienia

Gdy kod i `requirements.txt` się nie zmieniły, wystarczy:

```powershell
docker compose run --rm ai-client
```

Po zmianie kodu Pythona nie trzeba budować obrazu ponownie — katalog projektu
jest kopiowany do obrazu w trakcie budowania, więc aby użyć zmian wykonaj:

```powershell
docker compose build
docker compose run --rm ai-client
```

### Najczęstsze problemy

| Komunikat lub sytuacja | Co zrobić |
| --- | --- |
| Komenda `docker` nie jest rozpoznawana | Zainstaluj Docker Desktop, zamknij i otwórz ponownie PowerShell. |
| Brak połączenia z Docker Engine | Uruchom Docker Desktop i zaczekaj na jego pełne uruchomienie. |
| Brak klucza API | Upewnij się, że obok `compose.yaml` istnieje plik `.env` z `OPENROUTER_API_KEY`. |
| Błąd `401` z API | Sprawdź, czy klucz w `.env` jest kompletny i aktualny. |
| Zmodyfikowano kod, ale program działa po staremu | Ponownie wykonaj `docker compose build`. |

Alternatywnie, bez Docker Compose:

```powershell
docker build -t ai-client .
docker run -it --rm --env-file .env -v "${PWD}/data:/app/data" ai-client
```

W wariancie bez Compose dodaj także `-v "${PWD}/logs:/app/logs"`, jeśli chcesz
zachowywać logi na komputerze.

Po uruchomieniu wybierz model tekstowy lub naciśnij Enter, aby użyć modelu domyślnego: **NVIDIA: Nemotron 3 Ultra (free)**.

### Modele tekstowe

| Opcja | Model |
| --- | --- |
| 1 | NVIDIA: Nemotron 3 Ultra (free) — domyślny |
| 2 | Cohere: North Mini Code (free) |
| 3 | NVIDIA: Nemotron 3 Nano Omni (free) |
| 4 | Google: Gemma 4 31B (free) |
| 5 | Dots Studio: Dots3-Note Preview (free) |

Identyfikatory modeli są zdefiniowane w `models.py`. Dostępność modeli bezpłatnych zależy od OpenRouter.

### Komendy rozmowy

| Komenda | Działanie |
| --- | --- |
| `/exit` | Kończy program. |
| `/clear` | Usuwa historię rozmowy i przywraca komunikat systemowy. |
| `/save` | Ręcznie zapisuje bieżącą historię. |
| `/model` | Wyświetla nazwę aktywnego modelu. |
| `/switch` | Otwiera wybór modelu ponownie. |

Po każdej poprawnej odpowiedzi modelu historia jest zapisywana automatycznie.

## Generowanie plików

W menu wyboru modelu wybierz opcję `6 — Inne modele niż generujące tekst`.

| Opcja | Działanie | Model | Wynik |
| --- | --- | --- | --- |
| 1 | Zamiana tekstu na mowę | `heygen/heygen-voice-1-turbo:free`, głos `nadine` | plik `.pcm` |
| 2 | Generowanie obrazu z opisu | `recraft/recraft-v4.1-flash-v2:free`, proporcje 16:9 | plik `.png` |
| 3 | Zmiana katalogu zapisu plików | — | zapis ustawienia |
| 0 | Powrót do wyboru modelu | — | — |

Domyślnie pliki trafiają do `data/wygenerowane_pliki`. Wybrany katalog jest zapisywany w `data/ustawienia_modeli_plikow.json`; nazwy plików są tworzone na podstawie daty i czasu.

## Dane lokalne

| Ścieżka | Zawartość |
| --- | --- |
| `data/historia.db` | Baza SQLite z historią wiadomości. |
| `data/historia.json` | Dawny format historii, importowany tylko przy pierwszym uruchomieniu bazy. |
| `data/ustawienia_modeli_plikow.json` | Ustawiony katalog plików multimedialnych. |
| `data/wygenerowane_pliki/` | Domyślny katalog dla obrazów i nagrań. |

## Struktura projektu

```text
main.py       interfejs konsolowy i sterowanie rozmową
api.py        wysyłanie zapytań czatowych do OpenRouter
media.py      generowanie obrazów i mowy oraz zapis plików
history.py    zapis historii w SQLite i migracja z JSON
models.py     lista modeli tekstowych
config.py     konfiguracja API, parametrów i ścieżek
prompts.py    komunikat systemowy dla rozmowy
logger.py     konfiguracja logowania
tests/        testy modułów API, historii i multimediów
```

## Testy

```powershell
python -m unittest discover -s tests
```

Testy nie wysyłają rzeczywistych zapytań do OpenRouter — używają mocków i tymczasowych plików.
