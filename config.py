import os
from pathlib import Path

from dotenv import load_dotenv

from models import DEFAULT_MODEL, get_model

load_dotenv()

# OpenRouter
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Model
MODEL = get_model(DEFAULT_MODEL)

# Parametry generowania
TEMPERATURE = 1
TOP_P = 0.82
MAX_TOKENS = 5000
FREQUENCY_PENALTY = 0.1
PRESENCE_PENALTY = 0.1

# Ścieżki projektu
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
HISTORY_DB_FILE = DATA_DIR / "historia.db"

# Stara historia jest importowana przy pierwszym uruchomieniu po zmianie na SQLite.
HISTORY_FILE = DATA_DIR / "historia.json"
