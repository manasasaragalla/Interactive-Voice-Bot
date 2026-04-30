import os
import json
import uuid
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from google import genai
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

app = Flask(__name__)
CORS(app)

# Ensure directories exist
os.makedirs('logs', exist_ok=True)
os.makedirs('static/audio', exist_ok=True)

LOG_FILE = 'logs/chat_log.json'
AUDIO_DIR = 'static/audio'

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

# Initialize Gemini client
gemini_api_key = os.environ.get("GEMINI_API_KEY")
client = None

if gemini_api_key and gemini_api_key != "YOUR_GEMINI_API_KEY_HERE":
    try:
        client = genai.Client(api_key=gemini_api_key)
    except Exception as e:
        print(f"Failed to initialize Gemini Client: {e}")

# Rule-based Engine Fallback (Supports Hindi/Telugu/English keywords)
RULES = {
    "namaste": "Namaste! Ela unnaru? (How are you?)",
    "hello": "Hello! Nenu meku ela help cheyagalanu?",
    "peru": "Naa peru AI Voice Assistant. Meeku ela help kavali?",
    "name": "My name is Voice Assistant. Aapko kaise help chahiye?",
    "help": "Sure, meeku demo schedule chestanu or general help kavala?",
    "sahayam": "Tappakunda, nenu meeku help chestanu.",
    "chahiye": "Theek hai, nenu meeku help chestanu. Em kavali?",
    "demo": "Sure, meeku demo schedule chestanu. Ye time convenient ga untundi?",
    "kavali": "Sure, nenu adi arrange chestanu. Can you provide more details?",
    "price": "Pricing details gurinchi cheppala? Maaku basic and premium plans unnay.",
    "dhanyavad": "Dhanyavadamulu! (Thank you!)",
    "thanks": "You're welcome! Malli kaludham.",
    "shukriya": "Shukriya! Aapko aur kuch help chahiye?"
}

DEFAULT_RESPONSE = "Nenu inka nerchukuntunnanu. Can you please repeat that? (Meeku help kavala?)"

SYSTEM_PROMPT = """You are a helpful voice assistant. 
Reply in natural Hindi-Telugu mixed language (Hinglish + Tenglish).
Keep replies short (1-2 sentences). 
Mix both languages naturally like: "Sure, meeku demo schedule chestanu" """

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_text = data.get('text', '').lower()

    if not user_text:
        return jsonify({'error': 'No text provided'}), 400

    bot_reply = None

    try:
        # Load existing chat history
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            chat_log = json.load(f)

        # Try Gemini if configured
        if client:
            try:
                context = ""
                for msg in chat_log[-6:]:
                    role = "User" if msg['role'] == 'user' else "Assistant"
                    context += f"{role}: {msg['text']}\n"
                
                full_prompt = f"{SYSTEM_PROMPT}\n\n{context}User: {data.get('text')}\nAssistant:"
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=full_prompt
                )
                bot_reply = response.text.strip()
            except Exception as e:
                print(f"Gemini Error: {str(e)}. Falling back to rules.")

        # Fallback to Rules
        if not bot_reply:
            for keyword, response in RULES.items():
                if keyword in user_text:
                    bot_reply = response
                    break
            if not bot_reply:
                bot_reply = DEFAULT_RESPONSE

        # --- Generate TTS Audio (gTTS) ---
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join(AUDIO_DIR, audio_filename)
        
        # We use 'hi' (Hindi) as it handles Hinglish/Tenglish best
        tts = gTTS(text=bot_reply, lang='hi')
        tts.save(audio_path)

        # Append to logs
        chat_log.append({"role": "user", "text": data.get('text')})
        chat_log.append({"role": "bot", "text": bot_reply})

        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(chat_log, f, ensure_ascii=False, indent=2)

        return jsonify({
            'reply': bot_reply,
            'audio_url': f'/static/audio/{audio_filename}'
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Cleanup old audio files on startup
    for f in os.listdir(AUDIO_DIR):
        if f.endswith(".mp3"):
            try: os.remove(os.path.join(AUDIO_DIR, f))
            except: pass
            
    app.run(debug=True, port=5000)
