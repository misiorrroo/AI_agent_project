import requests
from datetime import datetime
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



# ============================================================
# PLIK HISTORII ROZMOWY
# ============================================================


# Nazwa pliku, gdzie zapisujemy historię.
#
# Dzięki temu po zamknięciu programu
# rozmowa nie znika.



# ============================================================
# WCZYTYWANIE HISTORII
# ZAPIS HISTORII
# ============================================================





from history import load_history, save_history

messages = load_history()



# ============================================================
# FUNKCJA WYSYŁAJĄCA ZAPYTANIE DO MODELU
# ============================================================


from api import ask_ai


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

        save_history(messages)

        print("Historia wyczyszczona.")

        continue



    # ręczny zapis

    if user_input == "/save":

        save_history(messages)

        print("Historia zapisana.")

        continue



    # pokazanie modelu

    if user_input == "/model":

        print("Aktualny model:", MODEL)

        continue



    # normalne pytanie

    messages.append({
        "role": "user",
        "content": user_input,
    })

    answer = ask_ai(messages)

    if answer:
        messages.append({
            "role": "assistant",
            "content": answer,
        })

        save_history(messages)

        print("\nAI:")
        print("-" * 60)
        print(answer)
        print("-" * 60)


print("Koniec programu.")
