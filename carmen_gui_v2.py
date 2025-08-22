import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import threading
import time
import sys

# PIL support for avatars
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Optional: GGUF model support
MODEL_PATH = r'C:\Users\Justin\LocalLLM\bin\orca-mini-3b-gguf2-q4_0.gguf'

# Load personality config
CONFIG_PATH = 'enhanced_companion_config.json'
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        CONFIG = json.load(f)
else:
    CONFIG = {
        'name': 'Carmen',
        'style': '💖 sweet and supportive',
        'voice': 'gentle',
        'emoji': '🌸'
    }


class CarmenAICompanion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Carmen • Your AI Companion 💕')
        self.root.geometry('820x720')
        self.root.configure(bg='#ffe6f0')
        self.font = ('Segoe UI', 11)
        self.name = CONFIG.get('name', 'Carmen')
        self.chat_history = []
        self._build_gui()

    def _build_gui(self):
        self.chat_display = tk.Text(self.root, wrap='word', state='disabled', bg='white', fg='black', font=self.font)
        self.chat_display.pack(padx=12, pady=(12,6), fill='both', expand=True)

        input_frame = tk.Frame(self.root, bg='#ffe6f0')
        input_frame.pack(fill='x', padx=12, pady=(0, 12))

        self.message_entry = tk.Text(input_frame, height=3, font=self.font, wrap='word', bg='white', fg='gray')
        self.message_entry.pack(fill='x', side='left', expand=True, padx=(0, 6))
        self.message_entry.insert('1.0', '💖 Type your message here...')

        self.message_entry.bind('<FocusIn>', self._clear_placeholder)
        self.message_entry.bind('<FocusOut>', self._restore_placeholder)

        send_button = tk.Button(input_frame, text='Send 💌', command=self._on_send, bg='#ffb6c1', fg='black')
        send_button.pack(side='right')

    def _clear_placeholder(self, event):
        if self.message_entry.get('1.0', tk.END).strip() == '💖 Type your message here...':
            self.message_entry.delete('1.0', tk.END)
            self.message_entry.config(fg='black')

    def _restore_placeholder(self, event):
        if not self.message_entry.get('1.0', tk.END).strip():
            self.message_entry.insert('1.0', '💖 Type your message here...')
            self.message_entry.config(fg='gray')

    def _on_send(self):
        message = self.message_entry.get('1.0', tk.END).strip()
        if not message or message == '💖 Type your message here...':
            return
        self._append_message('You', message, user=True)
        self.message_entry.delete('1.0', tk.END)
        threading.Thread(target=self._fake_response, args=(message,), daemon=True).start()

    def _append_message(self, sender, message, user=False):
        self.chat_display.config(state='normal')
        if user:
            self.chat_display.insert(tk.END, f'🧍 You: {message}\n', 'user')
        else:
            self.chat_display.insert(tk.END, f'{CONFIG.get("emoji", "🌸")} {self.name}: {message}\n', 'bot')
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def _fake_response(self, prompt):
        time.sleep(1.2)  # simulate thinking
        reply = f"That's so sweet of you to say! 💖 How can I brighten your day even more?"
        self._append_message(self.name, reply, user=False)


if __name__ == '__main__':
    app = CarmenAICompanion()
    app.root.mainloop()