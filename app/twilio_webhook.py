from flask import Flask, request, Response, session
from twilio.twiml.voice_response import VoiceResponse, Gather
from app.speech_to_text import transcribe_audio
from app.ai_service import get_ai_reply
from app.messaging import send_sms

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Needed for session management

# Language map for code-to-name
LANGUAGE_MAP = {
    "1": "hi",  # Hindi
    "2": "gu",  # Gujarati
    "3": "te"   # Telugu
}

@app.route('/')
def index():
    return "✅ KrishiVaani API is running!", 200


@app.route('/health')
def health():
    return "OK", 200



@app.route("/voice", methods=['POST'], strict_slashes=False)
def voice():
    resp = VoiceResponse()
    gather = Gather(num_digits=1, action="/language", method="POST", timeout=5)

    # Language selection message (spoken in each language)
    gather.say("Hindi ke liye 1 dabaiye.", language="hi-IN")
    gather.pause(length=1)
    gather.say("Gujarati maate 2 dabavo.", language="gu-IN")
    gather.pause(length=1)
    gather.say("Telugu kosam 3 ni andinchu.", language="te-IN")
    gather.pause(length=1)

    resp.append(gather)
    resp.redirect('/voice')  # If no input, ask again
    return Response(str(resp), mimetype='text/xml')


@app.route("/language", methods=['POST'], strict_slashes=False)
def language():
    selected_digit = request.form.get('Digits')
    language_code = LANGUAGE_MAP.get(selected_digit, "hi")  # default to Hindi

    resp = VoiceResponse()
    # Prompt in selected language
    if language_code == "hi":
        resp.say("Kripya beep ke baad apni samasya batayein.", language="hi-IN")
    elif language_code == "gu":
        resp.say("Kripya beep pachi tamari samasya kahjo.", language="gu-IN")
    elif language_code == "te":
        resp.say("Beep tarvata mee samasya cheppandi.", language="te-IN")

    # Pass language code to /transcribe via URL query param
    resp.record(maxLength=20, action=f"/transcribe?lang={language_code}", method="POST", playBeep=True)
    return Response(str(resp), mimetype='text/xml')


@app.route("/transcribe", methods=['POST'], strict_slashes=False)
def transcribe():
    recording_url = request.form['RecordingUrl'] + ".wav"
    phone_number = request.form['From']
    language_code = request.args.get('lang', 'hi')  # default to Hindi

    transcript, _ = transcribe_audio(recording_url, language_code)
    ai_reply = get_ai_reply(transcript, language_code)
    send_sms(phone_number, ai_reply)
    return ("", 204)