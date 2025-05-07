
import os
import zipfile
import gdown

MODEL_IDS = {
    "hi": "1xB_9opRaQmF798gbcCKl74OXJ9uxxEuu",  
    "en": "1okniKAkVuk6weOlgHSDRNPlDDwKv9HN1",
    "te": "1G1OLVv_neB68ihNep85mXZZBJsHq5CgN",
    "gu": "1dTOimCqk5u_6gDuw1LhJ_zEQ6KY5nv7s",
}

MODELS_DIR = "models"

def download_model(lang, file_id):
    zip_path = os.path.join(MODELS_DIR, f"{lang}.zip")
    model_path = os.path.join(MODELS_DIR, f"vosk-model-{lang}")

    if os.path.exists(model_path):
        print(f"✔ Model for {lang} already exists.")
        return

    print(f"⬇ Downloading model for {lang}...")
    gdown.download(id=file_id, output=zip_path, quiet=False)

    print(f"📦 Extracting model for {lang}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(MODELS_DIR)

    os.remove(zip_path)
    print(f"✅ {lang} model ready.\n")

if __name__ == "__main__":
    os.makedirs(MODELS_DIR, exist_ok=True)
    for lang, file_id in MODEL_IDS.items():
        download_model(lang, file_id)
