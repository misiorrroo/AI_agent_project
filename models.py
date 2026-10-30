AVAILABLE_MODELS = {
    "NVIDIA: Nemotron 3 Ultra (free)": "nvidia/nemotron-3-ultra-550b-a55b:free",
    "Cohere: North Mini Code (free)": "cohere/north-mini-code:free",
    "NVIDIA: Nemotron 3 Nano Omni (free)": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "Google: Gemma 4 31B (free)": "google/gemma-4-31b-it:free",
    "Dots Studio: Dots3-Note Preview (free)": "dots-studio/dots-3-note-preview:free",
}

DEFAULT_MODEL = "NVIDIA: Nemotron 3 Ultra (free)"


def get_model(model_name):
    return AVAILABLE_MODELS[model_name]