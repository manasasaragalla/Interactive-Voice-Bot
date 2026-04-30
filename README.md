# Hindi + Telugu Interactive Voice Bot 🎙️🤖

A modern, futuristic voice-based chatbot that can understand and respond in mixed Hindi and Telugu (Hinglish/Tenglish). This project was built to satisfy all requirements for the Interactive Voice Bot assignment, including premium design and AI-based smart replies.

## ✨ Key Features

- **🎙️ Advanced STT (Speech-to-Text)**: Uses the Web Speech API configured for `hi-IN` to accurately capture mixed Hindi and Telugu speech.
- **🧠 Hybrid Intelligence**:
    - **AI-Based (Gemini 1.5 Flash)**: Generates smart, natural, multi-turn responses with memory.
    - **Rule-Based Fallback**: Ensures the bot works even without an internet connection or API key.
- **🔊 High-Quality TTS (Text-to-Speech)**: Uses `gTTS` on the backend to generate clear audio with proper Indian phonetics.
- **🎨 Futuristic UI**: A premium "Cyberpunk-Glass" aesthetic featuring a central glowing sphere that visualizes voice activity.
- **💬 Multi-Modal Input**: Support for both **Voice** and **Text** chatting.
- **📄 Conversation Logs**: Automatically saves all interactions to `logs/chat_log.json`.

---

## 🛠️ Tech Stack

- **Backend**: Python Flask, `google-genai` (Gemini API), `gTTS`
- **Frontend**: Vanilla HTML5, CSS3 (Modern Flex/Grid, Glassmorphism), JavaScript (ES6+)
- **Hosting/Tunneling**: ngrok

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8+
- [Google AI Studio API Key](https://aistudio.google.com/app/apikey) (Optional but recommended for Smart Replies)

### 2. Installation
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Create or update the `.env` file in the root directory:
```env
GEMINI_API_KEY=your_api_key_here
```

### 4. Running the Project
Start the Flask server:
```bash
python app.py
```
The app will be available at `http://127.0.0.1:5000`.

### 5. Hosting with ngrok
To expose the project for evaluation:
```bash
ngrok http 5000
```
Share the generated `https://...ngrok-free.app` URL.

---

## 📂 Project Structure

```
voice-bot/
├── app.py              # Flask Backend & AI Logic
├── requirements.txt    # Python Dependencies
├── .env                # API Key Storage
├── logs/
│   └── chat_log.json   # Conversation History
├── static/
│   ├── audio/          # Generated TTS Audio files
│   ├── style.css       # Futuristic UI Styles
│   └── script.js       # STT/TTS & Frontend Logic
└── templates/
    └── index.html      # Main UI Structure
```

---

## 🎯 Assignment Compliance

| Requirement | Implementation Status |
|---|---|
| Hindi + Telugu Mix | ✅ (Via Gemini Prompt & Rules) |
| STT & TTS | ✅ (Web Speech API + gTTS) |
| Frontend UI | ✅ (Futuristic Design) |
| Conversation Logs | ✅ (JSON Logging) |
| Smart Replies (Bonus) | ✅ (Gemini 1.5 Flash) |
| Multi-turn Memory (Bonus) | ✅ (Context-aware prompting) |

Developed with ❤️ by **Manasa Saragalla** for the ML/AI Assessment.
