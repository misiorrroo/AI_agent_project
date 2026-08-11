import requests
import json
import os
from datetime import datetime


# ============================================================
# KONFIGURACJA API
# ============================================================

# Klucz API OpenRouter.
# Jest to "hasło", które pozwala Twojemu programowi
# wykonywać zapytania do modeli AI.
#
# Nie udostępniaj tego klucza publicznie.
API_KEY = os.getenv("OPENROUTER_API_KEY")


# Adres API OpenRouter.
# Wszystkie zapytania typu chat/completions wysyłamy tutaj.
API_URL = "https://openrouter.ai/api/v1/chat/completions"


# Nazwa modelu, który będzie wykonywał zadania.
#
# Możesz zmienić np.:
# openai/gpt-oss-20b:free
# deepseek/deepseek-chat-v3-0324:free
# openrouter/free
#MODEL = "openai/gpt-oss-20b:free"
MODEL = "openai/gpt-oss-20b:free"
#nvidia/nemotron-3-ultra-550b-a55b:free



# ============================================================
# PARAMETRY GENEROWANIA ODPOWIEDZI
# ============================================================


# Temperature:
# Kontroluje losowość odpowiedzi.
#
# 0.0  - bardzo dokładnie, mało kreatywnie
# 0.5  - balans
# 1.0+ - bardziej kreatywnie
#
# Do nauki/programowania zwykle 0.2-0.5
TEMPERATURE = 0.3


# Top_p:
# Alternatywna metoda kontroli losowości.
#
# Model bierze pod uwagę tylko najbardziej prawdopodobne
# fragmenty tekstu.
#
# 0.9 jest dobrym ustawieniem ogólnym.
TOP_P = 0.9


# Maksymalna liczba tokenów odpowiedzi.
#
# Token nie jest dokładnie słowem.
# Przykładowo:
# 1000 tokenów ≈ kilkaset słów.
#
# Większa wartość pozwala na dłuższe odpowiedzi.
MAX_TOKENS = 2000


# Frequency penalty:
# Kara za powtarzanie tych samych słów/fraz.
#
# 0 = brak kary
# większa wartość = mniej powtórzeń
FREQUENCY_PENALTY = 0.1


# Presence penalty:
# Zachęca model do wprowadzania nowych tematów.
#
# Przydatne przy kreatywnym pisaniu.
PRESENCE_PENALTY = 0.1



# ============================================================
# PLIK HISTORII ROZMOWY
# ============================================================


# Nazwa pliku, gdzie zapisujemy historię.
#
# Dzięki temu po zamknięciu programu
# rozmowa nie znika.
HISTORY_FILE = "historia.json"



# ============================================================
# WCZYTYWANIE HISTORII
# ============================================================


def load_history():

    # Jeżeli plik istnieje:
    # otwieramy go i odczytujemy zapisane wiadomości.

    if os.path.exists(HISTORY_FILE):

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    # Jeżeli pliku nie ma,
    # zaczynamy pustą rozmowę.

    return []



# ============================================================
# ZAPIS HISTORII
# ============================================================


def save_history():

    # Zapisuje aktualną listę messages
    # do pliku JSON.

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            messages,
            file,
            indent=4,
            ensure_ascii=False
        )



# ============================================================
# HISTORIA WIADOMOŚCI
# ============================================================


# messages przechowuje całą rozmowę.
#
# Każdy element ma:
#
# role:
#   user      -> użytkownik
#   assistant -> odpowiedź modelu
#
# content:
#   właściwa treść wiadomości

messages = load_history()



# ============================================================
# FUNKCJA WYSYŁAJĄCA ZAPYTANIE DO MODELU
# ============================================================


def ask_ai(text):


    # Dodajemy pytanie użytkownika
    # do historii rozmowy.

    messages.append(
        {
            "role": "user",
            "content": text
        }
    )



    # Nagłówki HTTP.
    #
    # Authorization:
    # przekazuje klucz API.
    #
    # Content-Type:
    # mówi serwerowi, że wysyłamy JSON.

    headers = {

        "Authorization": f"Bearer {API_KEY}",

        "Content-Type": "application/json"

    }



    # Dane wysyłane do modelu.

    data = {

        # wybór modelu
        "model": MODEL,


        # cała historia rozmowy
        "messages": messages,


        # parametry generowania

        "temperature": TEMPERATURE,

        "top_p": TOP_P,

        "max_tokens": MAX_TOKENS,

        "frequency_penalty": FREQUENCY_PENALTY,

        "presence_penalty": PRESENCE_PENALTY

    }



    try:


        # Wysyłamy żądanie HTTP POST.

        response = requests.post(

            API_URL,

            headers=headers,

            json=data,

            timeout=400

        )



        # Jeżeli API zwróci błąd,
        # pokazujemy informacje.

        if response.status_code != 200:

            print(
                "Błąd API:",
                response.status_code
            )

            print(response.text)

            return None



        # Zamieniamy odpowiedź JSON
        # na obiekt Python.

        result = response.json()



        # Wyciągamy sam tekst odpowiedzi.

        answer = (
            result["choices"][0]
            ["message"]["content"]
        )



        # Dodajemy odpowiedź modelu
        # do historii.

        messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )



        # zapisujemy historię po każdej odpowiedzi

        save_history()



        return answer



    except Exception as error:


        print(
            "Błąd połączenia:",
            error
        )

        return None



# ============================================================
# PROGRAM GŁÓWNY
# ============================================================


print("=" * 60)

print("OpenRouter Python Client")

print("Model:", MODEL)

print("Komendy:")

print("/exit   - zakończenie")

print("/clear  - wyczyszczenie historii")

print("/save   - zapis historii")

print("/model  - pokazuje model")

print("=" * 60)



while True:


    user_input = input("\nTy: ")



    # zakończenie programu

    if user_input == "/exit":

        break



    # czyszczenie historii

    if user_input == "/clear":

        messages.clear()

        save_history()

        print("Historia wyczyszczona.")

        continue



    # ręczny zapis

    if user_input == "/save":

        save_history()

        print("Historia zapisana.")

        continue



    # pokazanie modelu

    if user_input == "/model":

        print("Aktualny model:", MODEL)

        continue



    # normalne pytanie

    answer = ask_ai(user_input)



    if answer:

        print("\nAI:")

        print("-" * 60)

        print(answer)

        print("-" * 60)



print("Koniec programu.")
