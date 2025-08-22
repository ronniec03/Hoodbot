import os
import sys
import queue
import json
import threading
import sounddevice as sd
import vosk
import pyttsx3

# =========================
# CONFIG
# =========================
VOSK_MODEL_PATH = r"C:\Users\Justin\Documents\CompanionAI\vosk-model-small-en-us-0.15"

# =========================
# SETUP
# =========================
if not os.path.exists(VOSK_MODEL_PATH):
    print("ERROR: Vosk model not found at", VOSK_MODEL_PATH)
    sys.exit(1)

model = vosk.Model(VOSK_MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, 16000)

audio_queue = queue.Queue()
engine = pyttsx3.init()

# Configure voice
voices = engine.getProperty("voices")
for v in voices:
    if "Zira" in v.name or "female" in v.name.lower():
        engine.setProperty("voice", v.id)
        break
engine.setProperty("rate", 185)

# =========================
# TTS Function
# =========================
def speak_text(text: str):
    print(f"Carmen (speaking): {text}")
    engine.say(text)
    engine.runAndWait()

# =========================
# Placeholder LLM Response
# (swap with your actual model call)
# =========================
def get_carmen_reply(user_text: str) -> str:
    # TODO: Replace with your NSFW-3B model or local LLM call
    return f"I heard you say: '{user_text}'. I'm here with you."

# =========================
# Audio Callback
# =========================
def audio_callback(indata, frames, time, status):
    if status:
        print("Audio status:", status)
    audio_queue.put(bytes(indata))

# =========================
# Mic Listener Thread
# =========================
def mic_listener():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                           channels=1, callback=audio_callback):
        print("🎤 Microphone is live... Speak anytime.")
        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                if result.get("text"):
                    handle_input(result["text"])

# =========================
# Input Handler
# =========================
def handle_input(user_text: str):
    if not user_text.strip():
        return
    print(f"You: {user_text}")
    reply = get_carmen_reply(user_text)
    print(f"Carmen: {reply}")
    speak_text(reply)

# =========================
# Main Loop
# =========================
def main():
    # Start mic thread
    mic_thread = threading.Thread(target=mic_listener, daemon=True)
    mic_thread.start()

    # Typing option stays available
    print("✅ Carmen is ready. Type or speak to interact.\n")
    while True:
        try:
            user_text = input("You (typing): ")
            handle_input(user_text)
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
