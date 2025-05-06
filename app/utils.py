import json
import os

# Get the absolute path to the base directory where models are stored
def get_language_model_path(lang_code):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models"))

    # Load supported languages from config
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "languages.json")
    try:
        with open(config_path, "r") as f:
            langs = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load language config: {e}")
        # Default to Hindi model in case of error
        return os.path.join(base_dir, "vosk-model-small-hi-0.22")

    # Try to get the model folder for the requested lang_code, fallback to Hindi
    model_folder = langs.get(lang_code)
    if not model_folder:
        print(f"[WARNING] Language code '{lang_code}' not found. Falling back to Hindi.")
        model_folder = langs.get("hi-IN", "vosk-model-small-hi-0.22")

    return os.path.join(base_dir, model_folder)

# Map language codes to human-readable names
def get_language_name(lang_code):
    lang_map = {
        "hi-IN": "Hindi",
        "en-IN": "English",
        "gu-IN": "Gujarati",
        "te-IN": "Telugu"
    }
    return lang_map.get(lang_code, "Hindi")  # Default to Hindi
