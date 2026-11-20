from api import ask_ai  # FUNKCJA WYSYŁAJĄCA ZAPYTANIE DO MODELU
from history import clear_history, load_history, save_history
from logger import get_logger
from media import (
    generate_image,
    generate_speech,
    get_media_output_dir,
    set_media_output_dir,
)
from models import AVAILABLE_MODELS, DEFAULT_MODEL
from prompts import SYSTEM_PROMPT


def choose_model():
    """Wyświetla menu i zwraca identyfikator oraz nazwę wybranego modelu."""

    print("\nWybierz model:")
    print("1 - NVIDIA: Nemotron 3 Ultra (free)")
    print("2 - Cohere: North Mini Code (free)")
    print("3 - NVIDIA: Nemotron 3 Nano Omni (free)")
    print("4 - Google: Gemma 4 31B (free)")
    print("5 - Dots Studio: Dots3-Note Preview (free)")
    print("6 - Inne modele niż generujące tekst")

    model_choice = input("Twój wybór [1-6, Enter = domyślny]: ")

    if model_choice == "6":
        other_models_menu()
        return choose_model()

    if model_choice == "1":
        selected_model_name = "NVIDIA: Nemotron 3 Ultra (free)"
    elif model_choice == "2":
        selected_model_name = "Cohere: North Mini Code (free)"
    elif model_choice == "3":
        selected_model_name = "NVIDIA: Nemotron 3 Nano Omni (free)"
    elif model_choice == "4":
        selected_model_name = "Google: Gemma 4 31B (free)"
    elif model_choice == "5":
        selected_model_name = "Dots Studio: Dots3-Note Preview (free)"
    else:
        selected_model_name = DEFAULT_MODEL

    return AVAILABLE_MODELS[selected_model_name], selected_model_name


def other_models_menu():
    """Menu modeli tworzących pliki oraz ustawienia ich katalogu wyjściowego."""
    while True:
        print("\nInne modele niż generujące tekst:")
        print("1 - Modele tekst na głos")
        print("2 - Modele generujące obrazy")
        print("3 - Ustawienia modeli generujących pliki")
        print("0 - Powrót")
        choice = input("Twój wybór [0-3]: ").strip()

        if choice == "0":
            return
        if choice == "1":
            text = input("Tekst do zamiany na głos: ").strip()
            if text:
                output_file = generate_speech(text)
                if output_file:
                    print(f"Plik dźwiękowy zapisano w: {output_file}")
        elif choice == "2":
            prompt = input("Opis obrazu: ").strip()
            if prompt:
                output_file = generate_image(prompt)
                if output_file:
                    print(f"Obraz zapisano w: {output_file}")
        elif choice == "3":
            current_dir = get_media_output_dir()
            print(f"Aktualny katalog: {current_dir}")
            directory = input("Nowy katalog (Enter = bez zmian): ").strip()
            if directory:
                saved_dir = set_media_output_dir(directory)
                print(f"Katalog zapisu ustawiono na: {saved_dir}")
        else:
            print("Nieprawidłowy wybór.")

def main():
    """Uruchamia interaktywny interfejs konsolowy aplikacji."""
    logger = get_logger(__name__)
    logger.info("Uruchomiono program")

    messages = load_history()
    if not messages or messages[0]["role"] != "system":
        messages.insert(0, {
            "role": "system",
            "content": SYSTEM_PROMPT,
        })

    print("=" * 60)
    print("OpenRouter Python Client")

    selected_model, selected_model_name = choose_model()
    logger.info("Wybrano model: %s", selected_model)

    print("Model:", selected_model)
    print("Komendy:")
    print("/exit   - zakończenie")
    print("/clear  - wyczyszczenie historii")
    print("/save   - zapis historii")
    print("/model  - pokazuje model")
    print("/switch - zmienia model")
    print("=" * 60)

    while True:
        try:
            user_input = input("\nTy: ")
        except EOFError:
            print("\nZamknięto wejście programu.")
            break

        if user_input == "/exit":
            break

        if user_input == "/clear":
            clear_history()
            messages.clear()
            messages.append({
                "role": "system",
                "content": SYSTEM_PROMPT,
            })
            save_history(messages)
            print("Historia wyczyszczona.")
            continue

        if user_input == "/save":
            save_history(messages)
            print("Historia zapisana.")
            continue

        if user_input == "/model":
            print("Aktualny model:", selected_model_name)
            continue

        if user_input == "/switch":
            selected_model, selected_model_name = choose_model()
            logger.info("Zmieniono model: %s", selected_model)
            print("Wybrany model:", selected_model_name)
            continue

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


if __name__ == "__main__":
    main()
