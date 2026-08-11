from api import ask_ai  # FUNKCJA WYSYŁAJĄCA ZAPYTANIE DO MODELU
from history import load_history, save_history
from models import AVAILABLE_MODELS, DEFAULT_MODEL
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

print("\nWybierz model:")
print("1 - GPT-OSS (free)")
print("2 - DeepSeek (free)")
print("3 - NVIDIA: Nemotron 3.5 Content Safety (free)")
print("4 - Google: Gemma 4 31B (free)")
print("5 - Cohere: North Mini Code (free)")
model_choice = input("Twój wybór [1,2.... Enter = domyślny]: ")

if model_choice == "1":
    selected_model_name = "gpt-oss (free)"
    selected_model = AVAILABLE_MODELS[selected_model_name]
elif model_choice == "2":
    selected_model_name = "deepseek (free)"
    selected_model = AVAILABLE_MODELS[selected_model_name]
elif model_choice == "3":
    selected_model_name = "NVIDIA: Nemotron 3.5 Content Safety (free)"
    selected_model = AVAILABLE_MODELS[selected_model_name]
elif model_choice == "4":
    selected_model_name = "Google: Gemma 4 31B (free)"
    selected_model = AVAILABLE_MODELS[selected_model_name]
elif model_choice == "5":
    selected_model_name = "Cohere: North Mini Code (free)"
    selected_model = AVAILABLE_MODELS[selected_model_name]
else:
    selected_model_name = DEFAULT_MODEL
    selected_model = AVAILABLE_MODELS[selected_model_name]

logger.info("Wybrano model: %s", selected_model)

print("Model:", selected_model)

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

        print("Aktualny model:", selected_model)

        continue



    # normalne pytanie

    messages.append({
        "role": "user",
        "content": user_input,
    })

    answer = ask_ai(messages, selected_model)

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
