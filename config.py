import os
from pathlib import Path
from models import DEFAULT_MODEL, get_model
from dotenv import load_dotenv

load_dotenv()

# OpenRouter
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Model
MODEL = get_model(DEFAULT_MODEL)

# Parametry generowania
TEMPERATURE = 0.3
TOP_P = 0.9
MAX_TOKENS = 2000
FREQUENCY_PENALTY = 0.1
PRESENCE_PENALTY = 0.1

# Ścieżki projektu
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
HISTORY_FILE = DATA_DIR / "historia.json"