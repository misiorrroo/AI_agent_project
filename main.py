from api import ask_ai  # FUNKCJA WYSYŁAJĄCA ZAPYTANIE DO MODELU
from config import MODEL
from history import load_history, save_history
from prompts import SYSTEM_PROMPT
from logger import get_logger


logger = get_logger(__name__)
logger.info("Uruchomiono program")



messages = load_history()
if not messages or messages[0]["role"] != "system":
    messages.insert(0, {
        "role": "system",
        "content": SYSTEM_PROMPT,
    })


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


logger.info("Zakończono program")

print("Koniec programu.")
