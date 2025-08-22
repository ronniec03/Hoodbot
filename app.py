import tkinter as tk
from tkinter import scrolledtext
import json
import os

CONFIG_PATH = os.path.join("config", "companion_config.json")

def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "name": "Carmen",
            "emoji": "💠",
            "mood": "Default",
            "theme": "Dark"
        }

class CompanionApp:
    def __init__(self, root):
        self.root = root
        self.config = load_config()
        self.setup_ui()

    def setup_ui(self):
        self.root.title(f"{self.config['name']} - Companion AI")
        self.root.geometry("1400x800")

        # Frame for avatar + chat
        self.left_frame = tk.Frame(self.root, bg="#111111", width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(self.root, bg="#222222")
        self.right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Avatar placeholder
        self.avatar_label = tk.Label(self.left_frame, text=self.config['emoji'], font=("Arial", 64), bg="#111111", fg="white")
        self.avatar_label.pack(pady=20)

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(self.right_frame, wrap=tk.WORD, bg="#1e1e1e", fg="white", font=("Arial", 12))
        self.chat_display.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Input bar
        self.entry = tk.Entry(self.right_frame, font=("Arial", 12))
        self.entry.pack(fill=tk.X, padx=10, pady=5)
        self.entry.bind("<Return>", self.on_enter)

    def on_enter(self, event=None):
        user_text = self.entry.get().strip()
        if not user_text:
            return
        self.chat_display.insert(tk.END, f"You: {user_text}\n")
        self.entry.delete(0, tk.END)

        # Basic echo bot for now
        bot_reply = f"{self.config['name']}: I heard '{user_text}'"
        self.chat_display.insert(tk.END, bot_reply + "\n")

def run_app():
    root = tk.Tk()
    app = CompanionApp(root)
    root.mainloop()
