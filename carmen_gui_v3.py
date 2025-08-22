
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import threading
import time
import pyttsx3

from llm_runner import GGUFModelRunner

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

CONFIG_PATH = 'config/enhanced_companion_config.json'
AVATAR_PATH = 'assets/avatars/avatar_carmen.png'
MEMORY_PATH = 'data/chat_history/current_chat.json'

DEFAULT_MOODS = {
    "Supportive": {"prompt": "You're sweet, caring, gentle.", "emoji": "💖"},
    "Flirty": {"prompt": "You're playful, a little flirty, charming.", "emoji": "😘"},
    "Intellectual": {"prompt": "You're thoughtful, insightful, and articulate.", "emoji": "🧠"},
    "Chaotic": {"prompt": "You're unpredictable, random, and a bit wild.", "emoji": "🤪"},
}

class CarmenAICompanion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Carmen • Local AI Companion")
        self.root.geometry("900x740")
        self.root.configure(bg="#ffe6f0")
        self.font = ("Segoe UI", 11)
        self.name = "Carmen"
        self.memory = []
        self.llm = GGUFModelRunner()
        self.mood = "Supportive"

        self.tts = pyttsx3.init()
        self.tts.setProperty("rate", 185)

        self._build_gui()
        self._load_memory()

    def _build_gui(self):
        top = tk.Frame(self.root, bg="#ffe6f0")
        top.pack(fill="both", expand=True, padx=12, pady=12)

        if PIL_AVAILABLE and os.path.exists(AVATAR_PATH):
            avatar_img = Image.open(AVATAR_PATH).resize((128, 128))
            self.avatar_photo = ImageTk.PhotoImage(avatar_img)
            tk.Label(top, image=self.avatar_photo, bg="#ffe6f0").pack(side="left", padx=(0, 12), anchor="n")

        self.chat_display = tk.Text(top, wrap="word", state="disabled", bg="white", fg="black", font=self.font)
        self.chat_display.pack(fill="both", expand=True, side="left")

        # Mood selector
        bottom = tk.Frame(self.root, bg="#ffe6f0")
        bottom.pack(fill="x", padx=12, pady=(0, 6))

        tk.Label(bottom, text="Mood:", font=("Segoe UI", 10), bg="#ffe6f0").pack(side="left")
        self.mood_var = tk.StringVar(value="Supportive")
        mood_menu = ttk.Combobox(bottom, textvariable=self.mood_var, values=list(DEFAULT_MOODS.keys()), state="readonly", width=15)
        mood_menu.pack(side="left", padx=(6, 12))
        mood_menu.bind("<<ComboboxSelected>>", self._update_mood)

        # Input area
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

    def _update_mood(self, event):
        self.mood = self.mood_var.get()

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
        prefix = "🧍 You:" if user else f"{DEFAULT_MOODS[self.mood]['emoji']} {self.name}:"
        self.chat_display.insert(tk.END, f"{prefix} {message}\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def _query_model(self, prompt):
        try:
            mood_config = DEFAULT_MOODS[self.mood]
            system_prompt = f"You are {self.name}, {mood_config['prompt']}"
            response = self.llm.prompt(prompt, system_prompt=system_prompt)
        except Exception as e:
            response = f"Sorry, I had a brain freeze: {e}"
        self.memory.append({"role": "assistant", "content": response})
        self._save_memory()
        self._append_message(self.name, response, user=False)
        self.tts.say(response)
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
                    self._append_message("You" if msg["role"] == "user" else self.name, msg["content"], user=(msg["role"] == "user"))
            except Exception as e:
                print(f"[Memory Load Error] {e}")

if __name__ == '__main__':
    app = CarmenAICompanion()
    app.root.mainloop()
