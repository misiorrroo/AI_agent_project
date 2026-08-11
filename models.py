AVAILABLE_MODELS = {
    "gpt-oss (free)": "openai/gpt-oss-20b:free",
    "deepseek (free)": "deepseek/deepseek-chat-v3-0324:free",
    "NVIDIA: Nemotron 3.5 Content Safety (free)": "nvidia/nemotron-3.5-content-safety:free",
    "Google: Gemma 4 31B (free)": "google/gemma-4-31b-it:free",
    "Cohere: North Mini Code (free)": "cohere/north-mini-code:free",
}

DEFAULT_MODEL = "gpt-oss (free)"


def get_model(model_name):
    return AVAILABLE_MODELS[model_name]