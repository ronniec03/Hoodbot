
import tkinter as tk
from tkinter import ttk
import json
import os
import threading
import pyttsx3
from llm_runner import GGUFModelRunner

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

CONFIG_PATH = 'config/enhanced_companion_config.json'
AVATAR_DIR = 'assets/avatars/'
MEMORY_PATH = 'data/chat_history/current_chat.json'
MOOD_STATE_PATH = 'config/ui_config.json'

DEFAULT_MOODS = {
    "Supportive": {"prompt": "You're sweet, caring, gentle.", "emoji": "💖", "voice": {"rate": 175}},
    "Flirty": {"prompt": "You're playful, a little flirty, charming.", "emoji": "😘", "voice": {"rate": 190}},
    "Intellectual": {"prompt": "You're thoughtful, insightful, and articulate.", "emoji": "🧠", "voice": {"rate": 165}},
    "Chaotic": {"prompt": "You're unpredictable, random, and a bit wild.", "emoji": "🤪", "voice": {"rate": 210}}
}

class CarmenAICompanion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Carmen v4 • Local AI Companion")
        self.root.geometry("900x750")
        self.root.configure(bg="#ffe6f0")
        self.font = ("Segoe UI", 11)

        self.llm = GGUFModelRunner()
        self.tts = pyttsx3.init()
        self.memory = []
        self.avatar_photo = None

        self.mood = self._load_last_mood()
        self._build_gui()
        self._load_memory()

    def _build_gui(self):
        top = tk.Frame(self.root, bg="#ffe6f0")
        top.pack(fill="both", expand=True, padx=12, pady=12)

        self.avatar_label = tk.Label(top, bg="#ffe6f0")
        self.avatar_label.pack(side="left", padx=(0, 12), anchor="n")
        self._update_avatar()

        self.chat_display = tk.Text(top, wrap="word", state="disabled", bg="white", fg="black", font=self.font)
        self.chat_display.pack(fill="both", expand=True, side="left")

        bottom = tk.Frame(self.root, bg="#ffe6f0")
        bottom.pack(fill="x", padx=12, pady=(0, 6))

        tk.Label(bottom, text="Mood:", font=("Segoe UI", 10), bg="#ffe6f0").pack(side="left")
        self.mood_var = tk.StringVar(value=self.mood)
        mood_menu = ttk.Combobox(bottom, textvariable=self.mood_var, values=list(DEFAULT_MOODS.keys()), state="readonly", width=15)
        mood_menu.pack(side="left", padx=(6, 12))
        mood_menu.bind("<<ComboboxSelected>>", self._update_mood)

        input_frame = tk.Frame(self.root, bg="#ffe6f0")
        input_frame.pack(fill="x", padx=12, pady=(0, 12))

        self.message_entry = tk.Text(input_frame, height=3, font=self.font, wrap="word", bg="white", fg="gray")
        self.message_entry.pack(fill="x", side="left", expand=True, padx=(0, 6))
        self.message_entry.insert("1.0", "💖 Type your message here...")
        self.message_entry.bind("<FocusIn>", self._clear_placeholder)
        self.message_entry.bind("<FocusOut>", self._restore_placeholder)

        send_button = tk.Button(input_frame, text="Send 💌", command=self._on_send, bg="#ffb6c1", fg="black")
        send_button.pack(side="right")

    def _clear_placeholder(self, event):
        if self.message_entry.get("1.0", tk.END).strip() == "💖 Type your message here...":
            self.message_entry.delete("1.0", tk.END)
            self.message_entry.config(fg="black")

    def _restore_placeholder(self, event):
        if not self.message_entry.get("1.0", tk.END).strip():
            self.message_entry.insert("1.0", "💖 Type your message here...")
            self.message_entry.config(fg="gray")

    def _update_mood(self, event=None):
        self.mood = self.mood_var.get()
        self._update_avatar()
        self._save_last_mood()

    def _update_avatar(self):
        mood_file = f"{AVATAR_DIR}avatar_carmen_{self.mood.lower()}.png"
        if PIL_AVAILABLE and os.path.exists(mood_file):
            avatar_img = Image.open(mood_file).resize((128, 128))
            self.avatar_photo = ImageTk.PhotoImage(avatar_img)
            self.avatar_label.config(image=self.avatar_photo)

    def _on_send(self):
        message = self.message_entry.get("1.0", tk.END).strip()
        if not message or message == "💖 Type your message here...":
            return
        self._append_message("You", message, user=True)
        self.memory.append({"role": "user", "content": message})
        self._save_memory()
        self.message_entry.delete("1.0", tk.END)
        threading.Thread(target=self._query_model, args=(message,), daemon=True).start()

    def _append_message(self, sender, message, user=False):
        self.chat_display.config(state="normal")
        prefix = "🧍 You:" if user else f"{DEFAULT_MOODS[self.mood]['emoji']} Carmen:"
        self.chat_display.insert(tk.END, f"{prefix} {message}\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def _query_model(self, prompt):
        try:
            mood_data = DEFAULT_MOODS[self.mood]
            system_prompt = f"You are Carmen, {mood_data['prompt']}"
            response = self.llm.prompt(prompt, system_prompt=system_prompt)
        except Exception as e:
            response = f"Sorry, I had a brain freeze: {e}"
        self.memory.append({"role": "assistant", "content": response})
        self._save_memory()
        self._append_message("Carmen", response, user=False)
        self._speak(response)

    def _speak(self, text):
        mood_voice = DEFAULT_MOODS[self.mood].get("voice", {})
        for prop, value in mood_voice.items():
            self.tts.setProperty(prop, value)
        self.tts.say(text)
        self.tts.runAndWait()

    def _save_memory(self):
        try:
            os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
            with open(MEMORY_PATH, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            print(f"[Memory Save Error] {e}")

    def _load_memory(self):
        if os.path.exists(MEMORY_PATH):
            try:
                with open(MEMORY_PATH, "r", encoding="utf-8") as f:
                    self.memory = json.load(f)
                for msg in self.memory:
                    self._append_message("You" if msg["role"] == "user" else "Carmen", msg["content"], user=(msg["role"] == "user"))
            except Exception as e:
                print(f"[Memory Load Error] {e}")

    def _save_last_mood(self):
        try:
            os.makedirs(os.path.dirname(MOOD_STATE_PATH), exist_ok=True)
            with open(MOOD_STATE_PATH, "w", encoding="utf-8") as f:
                json.dump({"last_mood": self.mood}, f, indent=2)
        except Exception as e:
            print(f"[Mood Save Error] {e}")

    def _load_last_mood(self):
        if os.path.exists(MOOD_STATE_PATH):
            try:
                with open(MOOD_STATE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("last_mood", "Supportive")
            except Exception:
                pass
        return "Supportive"

if __name__ == '__main__':
    app = CarmenAICompanion()
    app.root.mainloop()
