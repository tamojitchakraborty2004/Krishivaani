import os
import google.generativeai as genai
from dotenv import load_dotenv
from app.utils import get_language_name

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

def get_ai_reply(transcript, lang_code):
    language = get_language_name(lang_code)
    
    prompt = (
        f"You are an expert agricultural assistant. "
        f"A farmer just asked the following question in {language}:\n"
        f"{transcript}\n"
        f"Give a simple, clear,and useful answer in {language}. "
        f"The answer length should not exceed 30 words."
    )

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini API Error:", e)
        return "AI service is currently unavailable. Please try again later."
