import os
import wave
import json
import time
import requests
from requests.auth import HTTPBasicAuth
from twilio.rest import Client
from vosk import Model, KaldiRecognizer
from pydub import AudioSegment
from app.utils import get_language_model_path

# Load Twilio credentials from environment variables
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
twilio_client = Client(TWILIO_SID, TWILIO_TOKEN)

def download_audio(url, filename='temp'):
    media_url = url + "?mediaFormat=mp3"  # Safer than wav
    print("Downloading from:", media_url)

    resp = requests.get(media_url, auth=HTTPBasicAuth(TWILIO_SID, TWILIO_TOKEN))
    if resp.status_code != 200:
        print(f"[ERROR] Failed to download audio: {resp.status_code} {resp.text}")
        raise Exception("Audio download failed.")

    in_path = f"{filename}.mp3"
    with open(in_path, 'wb') as f:
        f.write(resp.content)

    return in_path

def convert_to_wav(in_path, out_path="converted.wav"):
    audio = AudioSegment.from_file(in_path)
    audio = audio.set_channels(1)  # Mono channel for Vosk
    audio.export(out_path, format="wav")
    return out_path

def transcribe_audio(recording_url, language_code="hi-IN"):
    time.sleep(3)  # Wait for Twilio to finish processing the recording

    in_file = download_audio(recording_url)
    wav_file = convert_to_wav(in_file)

    try:
        wf = wave.open(wav_file, "rb")
        raw = wf.readframes(wf.getnframes())
    except wave.Error as e:
        print("[ERROR] Cannot open WAV file:", e)
        return "", language_code

    # Load model based on provided language code
    try:
        model = Model(get_language_model_path(language_code))
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}")
        return "", language_code

    rec = KaldiRecognizer(model, wf.getframerate())
    rec.AcceptWaveform(raw)
    result = json.loads(rec.Result())

    return result.get("text", ""), language_code
