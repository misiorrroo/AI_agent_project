# AI Client

Pythonowy klient CLI do komunikacji z modelami językowymi przez OpenRouter API.

Projekt został zaprojektowany jako praktyczna aplikacja do nauki pracy z API, obsługi konfiguracji, zarządzania historią rozmów, logowania oraz organizacji większego projektu Pythonowego.

---

## 📌 Spis treści

- [Opis projektu](#-opis-projektu)
- [Funkcje](#-funkcje)
- [Technologie](#-technologie)
- [Struktura projektu](#-struktura-projektu)
- [Wymagania](#-wymagania)
- [Instalacja](#-instalacja)
- [Konfiguracja](#-konfiguracja)
- [Uruchomienie](#-uruchomienie)
- [Przykładowe użycie](#-przykładowe-użycie)
- [Historia rozmów](#-historia-rozmów)
- [Modele](#-modele)
- [Logowanie](#-logowanie)
- [Architektura](#-architektura)
- [Rozwój projektu](#-rozwój-projektu)
- [Testy](#-testy)
- [Bezpieczeństwo](#-bezpieczeństwo)
- [Licencja](#-licencja)

---

# 🤖 Opis projektu

**AI Client** to aplikacja napisana w Pythonie umożliwiająca komunikację z modelami LLM za pośrednictwem OpenRouter API.

Projekt działa z poziomu terminala i pozwala między innymi na:

- wysyłanie promptów do modeli AI,
- wybór modelu,
- przechowywanie historii rozmów,
- odczytywanie poprzednich rozmów,
- zarządzanie konfiguracją,
- obsługę odpowiedzi API,
- logowanie działania aplikacji,
- obsługę błędów,
- testowanie poszczególnych modułów.

Projekt ma również charakter edukacyjny — jego celem jest praktyczne poznanie budowy aplikacji Pythonowej korzystającej z zewnętrznego REST API.

---

# ✨ Funkcje

## 💬 Komunikacja z LLM

Aplikacja umożliwia wysyłanie wiadomości do modeli językowych poprzez OpenRouter API.

Obsługiwane są między innymi:

- wiadomości użytkownika,
- wiadomości systemowe,
- odpowiedzi modelu,
- parametry generowania,
- wybór modelu,
- historia konwersacji.

---

## 🧠 Historia rozmów

Aplikacja przechowuje historię rozmów lokalnie.

Historia może zawierać:

- wiadomości użytkownika,
- odpowiedzi modelu,
- wybrany model,
- informacje o rozmowie,
- znaczniki czasu.

Domyślne dane historii są przechowywane w:

```text
data/historia.json