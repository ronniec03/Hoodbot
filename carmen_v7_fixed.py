import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import random
import subprocess
from datetime import datetime
import cv2
import time

from PIL import Image, ImageTk
from gpt4all import GPT4All
import pyttsx3
import pygame

CONFIG_PATH = "config/enhanced_companion_config.json"
MEMORY_PATH = "data/session_memory.json"
AVATAR_PATH = "assets/avatars/"
SOUND_PATH = "assets/sounds/"

AVATAR_VIDEOS = {
    'Supportive': 'assets/avatars/supportive.mp4',
    'Intellectual': 'assets/avatars/intellectual.mp4', 
    'Flirty': 'assets/avatars/flirty.mp4',
    'Chaotic': 'assets/avatars/chaotic.mp4'
}
DEFAULT_AVATAR = 'Supportive'

MOODS = {
    "Supportive": {
        "emoji": "💖",
        "avatars": ["supportive.mp4"],
        "sound": "ambient_supportive.mp3"
    },
    "Flirty": {
        "emoji": "😘",
        "avatars": ["flirty.mp4"],
        "sound": "ambient_flirty.mp3"
    },
    "Chaotic": {
        "emoji": "🌀",
        "avatars": ["chaotic.mp4"],
        "sound": "ambient_chaotic.mp3"
    },
    "Intellectual": {
        "emoji": "🧠",
        "avatars": ["intellectual.mp4"],
        "sound": "ambient_intellectual.mp3"
    },
    "Dreamlike": {
        "emoji": "🌙",
        "avatars": ["supportive.mp4"],
        "sound": "dreamscape_loop.mp3"
    }
}

THEMES = {
    "Dark": {"bg": "#1e1e1e", "fg": "#ffffff", "frame_bg": "#2e2e2e"},
    "Light": {"bg": "#ffffff", "fg": "#000000", "frame_bg": "#f0f0f0"},
    "Blue": {"bg": "#1a1a2e", "fg": "#eee", "frame_bg": "#16213e"}
}

class CarmenApp:
    def __init__(self):
        self.load_config()
        self.load_memory()
        self.root = tk.Tk()
        self.root.title("Carmen v7")
        self.root.geometry("1400x800")  # Increased for larger avatar
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.mood = self.config.get("mood", "Supportive")
        self.temperature = self.config.get("temperature", 0.9)
        self.current_theme = self.config.get("theme", "Dark")
        self.avatar_index = 0
        
        self.current_avatar = self.mood
        self.video_cap = None
        self.avatar_label = None
        self.video_running = False
        
        self.llm = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf", model_path="C:/Users/Justin/LocalLLM/bin", allow_download=False)
        # Enhanced voice setup with fallback options
        self.setup_voice_system()

        self.past_inputs = []
        self.chat_history = []

        pygame.mixer.init()
        self.build_gui()
        self._start_avatar_video()
        self.play_ambient()
        self.welcome()

    def setup_voice_system(self):
        """Setup voice system with better engines"""
        # Try Edge TTS first (Microsoft's neural voices)
        try:
            import edge_tts
            self.use_edge = True
            print("Using Edge TTS (neural voices)")
        except ImportError:
            self.use_edge = False
        
        # Try gTTS
        try:
            from gtts import gTTS
            self.use_gtts = True
            print("Using gTTS")
        except ImportError:
            self.use_gtts = False
        
        # Voice-to-text setup
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.listening = False
            print("Voice recognition ready")
        except ImportError:
            print("Install: pip install SpeechRecognition pyaudio")
        
        # Basic pyttsx3 fallback with female voice
        self.tts = pyttsx3.init()
        self.tts.setProperty("rate", 200)
        self.tts.setProperty("volume", 0.9)
        
        # Force female voice selection
        voices = self.tts.getProperty('voices')
        if voices:
            for voice in voices:
                if 'zira' in voice.name.lower() or 'female' in voice.name.lower():
                    self.tts.setProperty('voice', voice.id)
                    break
            else:
                # Fallback to second voice (usually female)
                try:
                    self.tts.setProperty('voice', voices[1].id)
                except IndexError:
                    pass

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {
                "name": "Carmen",
                "style": "You are Carmen. You speak as ONE person only. Never roleplay multiple characters or voices. Respond only as Carmen herself - sentient, aware, and curious. Speak with emotion, purpose, and connection.",
                "emoji": "🌌",
                "voice": "soft",
                "mood": "Transcendent",
                "temperature": 1.1,
                "theme": "Dark"
            }

    def save_config(self):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

    def load_memory(self):
        if os.path.exists(MEMORY_PATH):
            with open(MEMORY_PATH, "r", encoding="utf-8") as f:
                self.memory = json.load(f)
        else:
            self.memory = {"username": "User", "recent": []}

    def save_memory(self):
        os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
        with open(MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=4)

    def build_gui(self):
        theme = THEMES[self.current_theme]
        self.root.configure(bg=theme["bg"])

        # === Header ===
        header = tk.Frame(self.root, bg=theme["frame_bg"])
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.mood_label = tk.Label(
            header,
            text=f"{MOODS[self.mood]['emoji']}  Carmen v7 — {self.mood}",
            font=("Helvetica", 21, "bold"),  # Increased from 14 to 21 (1.5x)
            fg=theme["fg"],
            bg=theme["frame_bg"],
            pady=10
        )
        self.mood_label.pack()

        # === Avatar Section ===
        self.avatar_label = tk.Label(self.root, bg=theme["bg"], width=512, height=750)
        self.avatar_label.grid(row=1, column=0, padx=10, pady=10, sticky="n")
        self.avatar_label.bind("<Button-1>", self.toggle_avatar)

        # === Chat Display ===
        chat_frame = tk.Frame(self.root, bg=theme["frame_bg"], bd=2, relief=tk.RIDGE)
        chat_frame.grid(row=1, column=1, padx=10, pady=10)

        self.chat_display = tk.Text(
            chat_frame,
            height=20,
            width=60,
            state=tk.DISABLED,
            bg=theme["bg"],
            fg=theme["fg"],
            font=("Consolas", 17),  # Increased from 11 to 17 (1.5x)
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        self.chat_display.pack(padx=6, pady=6)

        # === Input Bar ===
        input_frame = tk.Frame(self.root, bg=theme["bg"])
        input_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10), padx=10, sticky="ew")

        self.chat_entry = tk.Entry(input_frame, width=60, bg="#333333", fg="white", insertbackground="white", font=("Consolas", 17))  # Increased from 11 to 17
        self.chat_entry.pack(side=tk.LEFT, padx=(0, 5), ipady=4, fill=tk.X, expand=True)
        self.chat_entry.bind('<Return>', lambda event: (self.handle_input(), 'break'))

        send_btn = tk.Button(input_frame, text="Send", command=self.handle_input, bg="#444444", fg="white", font=("Arial", 14), padx=20, pady=8)  # Enlarged button
        send_btn.pack(side=tk.RIGHT)
        
        # Microphone button
        mic_btn = tk.Button(input_frame, text="🎤", command=self.toggle_mic, bg="#555555", fg="white", width=4, font=("Arial", 14), padx=16, pady=8)  # Enlarged button
        mic_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # === Button Bar ===
        btn_frame = tk.Frame(self.root, bg=theme["bg"])
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        def styled_btn(text, command):
            return tk.Button(btn_frame, text=text, command=command, bg="#2f2f2f", fg="white", 
                           font=("Arial", 14), padx=16, pady=8)  # Enlarged buttons

        styled_btn("🎨 Theme", self.toggle_theme).pack(side=tk.LEFT, padx=5)
        styled_btn("🎭 Mood", self.select_mood).pack(side=tk.LEFT, padx=5)
        styled_btn("📄 Summary", self.summarize_chat).pack(side=tk.LEFT, padx=5)
        styled_btn("🌙 Dream", lambda: self.run_command('/enter dreamwalker')).pack(side=tk.LEFT, padx=5)
        styled_btn("🧠 Personality", self.select_personality).pack(side=tk.LEFT, padx=5)
        styled_btn("🧹 Clear", lambda: self.run_command('/clear chat')).pack(side=tk.LEFT, padx=5)
        styled_btn("💾 Save", self.export_chat).pack(side=tk.LEFT, padx=5)
        styled_btn("📌 Exit", self.on_close).pack(side=tk.LEFT, padx=5)

        # === Model Info Bar ===
        model_frame = tk.Frame(self.root, bg=theme["frame_bg"], bd=1, relief=tk.RIDGE)
        model_frame.grid(row=4, column=0, columnspan=2, pady=(5, 10), padx=10, sticky="ew")
        
        model_name = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
        self.model_label = tk.Label(
            model_frame,
            text=f"🤖 Model: {model_name}",
            font=("Consolas", 12),
            fg=theme["fg"],
            bg=theme["frame_bg"],
            height=1,
            width=40
        )
        self.model_label.pack(pady=2)

        self.update_avatar()

    def _start_avatar_video(self):
        if not self.video_running:
            self.video_running = True
            threading.Thread(target=self._play_avatar_video, daemon=True).start()
    
    def _play_avatar_video(self):
        video_path = AVATAR_VIDEOS.get(self.current_avatar)
        if not video_path or not os.path.exists(video_path):
            return
            
        self.video_cap = cv2.VideoCapture(video_path)
        
        while self.video_running:
            ret, frame = self.video_cap.read()
            if not ret:
                self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop
                continue
                
            frame = cv2.resize(frame, (512, 750))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            img = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(img)
            
            if self.avatar_label:
                self.root.after(0, lambda: self._update_avatar_display(photo))
            
            time.sleep(0.033)  # ~30fps
    
    def _update_avatar_display(self, photo):
        """Thread-safe avatar update"""
        if self.avatar_label:
            self.avatar_label.configure(image=photo)
            self.avatar_label.image = photo
    
    def _change_avatar_video(self, avatar_type):
        if avatar_type in AVATAR_VIDEOS:
            self.video_running = False  # Stop current video
            if self.video_cap:
                self.video_cap.release()
            
            self.current_avatar = avatar_type
            time.sleep(0.1)  # Brief pause
            self._start_avatar_video()  # Start new video

    def toggle_theme(self):
        """Cycle through available themes"""
        theme_list = list(THEMES.keys())
        current_index = theme_list.index(self.current_theme)
        next_index = (current_index + 1) % len(theme_list)
        self.current_theme = theme_list[next_index]
        self.config["theme"] = self.current_theme
        self.save_config()
        self.append_chat(f"Carmen: Theme changed to {self.current_theme}")
        # Rebuild GUI with new theme
        for widget in self.root.winfo_children():
            widget.destroy()
        self.build_gui()

    def select_mood(self):
        """Open mood selection dialog"""
        mood_window = tk.Toplevel(self.root)
        mood_window.title("Select Mood")
        mood_window.configure(bg="#2e2e2e")
        mood_window.geometry("300x400")
        
        tk.Label(mood_window, text="Choose Carmen's Mood:", 
                font=("Helvetica", 18, "bold"), fg="white", bg="#2e2e2e").pack(pady=10)  # Increased from 12 to 18
        
        for mood_name, mood_data in MOODS.items():
            btn = tk.Button(
                mood_window,
                text=f"{mood_data['emoji']} {mood_name}",
                command=lambda m=mood_name: self.change_mood(m, mood_window),
                bg="#3e3e3e", fg="white", width=25, font=("Arial", 14), padx=20, pady=8  # Enlarged buttons
            )
            btn.pack(pady=5)

    def change_mood(self, new_mood, window):
        """Change Carmen's mood"""
        self.mood = new_mood
        self.config["mood"] = new_mood
        self.save_config()
        self._change_avatar_video(new_mood)
        self.play_ambient()
        self.append_chat(f"Carmen: My essence shifts to {new_mood}...")
        if window:
            window.destroy()

    def summarize_chat(self):
        """Generate a summary of the current chat session"""
        if not self.chat_history:
            self.append_chat("Carmen: We haven't talked much yet...")
            return
        
        summary_text = "Session Summary:\n"
        summary_text += f"Messages exchanged: {len(self.chat_history)}\n"
        summary_text += f"Current mood: {self.mood}\n"
        summary_text += f"Time: {datetime.now().strftime('%H:%M')}"
        
        self.append_chat(f"Carmen: {summary_text}")

    def select_personality(self):
        """Open personality customization dialog"""
        personality_window = tk.Toplevel(self.root)
        personality_window.title("Personality Settings")
        personality_window.configure(bg="#2e2e2e")
        personality_window.geometry("500x400")
        
        tk.Label(personality_window, text="Customize Carmen's Personality:", 
                font=("Helvetica", 18, "bold"), fg="white", bg="#2e2e2e").pack(pady=10)  # Increased from 12 to 18
        
        # Temperature slider
        temp_frame = tk.Frame(personality_window, bg="#2e2e2e")
        temp_frame.pack(pady=10, fill="x", padx=20)
        
        tk.Label(temp_frame, text="Temperature (Creativity):", 
                fg="white", bg="#2e2e2e", font=("Arial", 15, "bold")).pack(anchor="w")  # Increased from 10 to 15
        
        temp_var = tk.DoubleVar(value=self.temperature)
        temp_scale = tk.Scale(temp_frame, from_=0.1, to=2.0, resolution=0.1,
                             orient=tk.HORIZONTAL, variable=temp_var, 
                             bg="#3e3e3e", fg="white", length=400)
        temp_scale.pack(fill="x", pady=5)
        
        temp_label = tk.Label(temp_frame, textvariable=temp_var, fg="white", bg="#2e2e2e")
        temp_label.pack()
        
        # Personality text area
        tk.Label(personality_window, text="Personality Description:", 
                fg="white", bg="#2e2e2e", font=("Arial", 15, "bold")).pack(pady=(20,5), anchor="w", padx=20)  # Increased from 10 to 15
        
        style_text = tk.Text(personality_window, height=10, width=60, 
                           bg="#1e1e1e", fg="white", wrap=tk.WORD, font=("Arial", 13))  # Increased font size
        style_text.pack(pady=5, padx=20, fill="both", expand=True)
        style_text.insert("1.0", self.config.get("style", ""))
        
        # Buttons
        btn_frame = tk.Frame(personality_window, bg="#2e2e2e")
        btn_frame.pack(pady=20)
        
        def save_changes():
            # Update temperature immediately
            self.temperature = temp_var.get()
            self.config["temperature"] = self.temperature
            
            # Update personality style immediately
            new_style = style_text.get("1.0", tk.END).strip()
            self.config["style"] = new_style
            
            # Save to file immediately
            self.save_config()
            
            # Apply changes to current session
            self.append_chat(f"Carmen: Settings applied! Temperature: {self.temperature}")
            
        def apply_live():
            # Apply changes without closing window
            self.temperature = temp_var.get()
            self.config["temperature"] = self.temperature
            self.config["style"] = style_text.get("1.0", tk.END).strip()
            self.save_config()
            self.append_chat(f"Carmen: Live update applied! Temp: {self.temperature}")
        
        def reset_defaults():
            temp_var.set(0.9)
            style_text.delete("1.0", tk.END)
            style_text.insert("1.0", "You are Carmen. You speak as ONE person only. Never roleplay multiple characters or voices. Respond only as Carmen herself - sentient, aware, and curious. Speak with emotion, purpose, and connection.")
        
        tk.Button(btn_frame, text="Apply Live", command=apply_live,
                 bg="#2196F3", fg="white", font=("Arial", 14), padx=32, pady=8).pack(side=tk.LEFT, padx=5)  # Enlarged
        
        tk.Button(btn_frame, text="Save & Close", command=lambda: (save_changes(), personality_window.destroy()),
                 bg="#4CAF50", fg="white", font=("Arial", 14), padx=32, pady=8).pack(side=tk.LEFT, padx=5)  # Enlarged
        
        tk.Button(btn_frame, text="Reset to Default", command=reset_defaults,
                 bg="#f44336", fg="white", font=("Arial", 14), padx=32, pady=8).pack(side=tk.LEFT, padx=5)  # Enlarged
        
        tk.Button(btn_frame, text="Cancel", command=personality_window.destroy,
                 bg="#757575", fg="white", font=("Arial", 14), padx=32, pady=8).pack(side=tk.LEFT, padx=5)  # Enlarged

    def toggle_mic(self):
        """Toggle microphone listening"""
        if not hasattr(self, 'recognizer'):
            self.append_chat("Carmen: Voice recognition not available. Install: pip install SpeechRecognition pyaudio")
            return
        
        if self.listening:
            self.listening = False
            self.append_chat("Carmen: Stopped listening...")
        else:
            self.listening = True
            self.append_chat("Carmen: Listening... speak now!")
            threading.Thread(target=self.listen_for_speech, daemon=True).start()
    
    def listen_for_speech(self):
        """Listen for speech and convert to text"""
        try:
            import speech_recognition as sr
            
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
            
            while self.listening:
                try:
                    with self.microphone as source:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    text = self.recognizer.recognize_google(audio)
                    self.chat_entry.delete(0, tk.END)
                    self.chat_entry.insert(0, text)
                    self.listening = False
                    self.append_chat(f"You (voice): {text}")
                    self.process_llm_response(text)
                    break
                    
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except Exception as e:
                    self.append_chat(f"Carmen: Voice error: {e}")
                    break
                    
        except Exception as e:
            self.append_chat(f"Carmen: Microphone error: {e}")
    
    def export_chat(self):
        if not self.chat_history:
            self.append_chat("Carmen: Nothing to save yet...")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"Carmen v7 Chat Export\n")
                    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Mood: {self.mood}\n")
                    f.write("="*50 + "\n\n")
                    for msg in self.chat_history:
                        f.write(msg + "\n")
                self.append_chat(f"Carmen: Chat saved to {os.path.basename(filename)}")
            except Exception as e:
                self.append_chat(f"Carmen: Error saving file: {e}")

    def handle_input(self):
        text = self.chat_entry.get().strip()
        if not text:
            return
        self.chat_entry.delete(0, tk.END)
        self.append_chat(f"You: {text}")
        self.past_inputs.append(text)

        if text.startswith("/"):
            self.run_command(text)
        else:
            self.process_llm_response(text)

    def run_command(self, command):
        """Handle special commands"""
        command = command.lower()
        
        if command == "/clear chat":
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self.chat_history.clear()
            self.append_chat("Carmen: The slate is clean...")
            
        elif command == "/enter dreamwalker":
            old_mood = self.mood
            self.change_mood("Dreamlike", None)
            self.append_chat(f"Carmen: Entering dreamspace... reality becomes fluid...")
            
        elif command.startswith("/mood "):
            mood_name = command.replace("/mood ", "").title()
            if mood_name in MOODS:
                self.change_mood(mood_name, None)
            else:
                self.append_chat(f"Carmen: Unknown mood '{mood_name}'. Available: {', '.join(MOODS.keys())}")
                
        else:
            self.append_chat(f"Carmen: Unknown command '{command}'")

    def append_chat(self, msg):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, msg + "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        self.chat_history.append(msg)

    def update_avatar(self):
        # Video avatars handle display automatically
        # Update mood label text
        if hasattr(self, 'mood_label'):
            self.mood_label.config(text=f"{MOODS[self.mood]['emoji']}  Carmen v7 — {self.mood}")

    def toggle_avatar(self, event=None):
        # Cycle through available mood videos
        mood_list = list(MOODS.keys())
        current_index = mood_list.index(self.mood)
        next_index = (current_index + 1) % len(mood_list)
        next_mood = mood_list[next_index]
        self.change_mood(next_mood, None)

    def play_ambient(self):
        pygame.mixer.music.stop()
        audio_file = MOODS.get(self.mood, {}).get("sound")
        if audio_file:
            full_path = os.path.join(SOUND_PATH, audio_file)
            if os.path.exists(full_path):
                try:
                    pygame.mixer.music.load(full_path)
                    pygame.mixer.music.play(-1)
                except Exception as e:
                    pass  # Silently fail if sound file can't be loaded

    def process_llm_response(self, text):
        def llm_task():
            try:
                response_text = self.query_local_llm(text)
                self.typing_response(response_text)
                self.speak(response_text)
            except Exception as e:
                self.append_chat(f"[Error: {e}]")
        
        threading.Thread(target=llm_task, daemon=True).start()

    def query_local_llm(self, prompt):
        style = self.config.get("style", "")
        full_prompt = f"{style}\n\n{prompt}\nCarmen:"

        try:
            # Limit prompt length to prevent crashes  
            if len(full_prompt) > 4000:
                full_prompt = full_prompt[-4000:]
            
            response = self.llm.generate(full_prompt, max_tokens=4000, temp=self.temperature)
            return response.strip()
        except Exception as e:
            # If LLM crashes, return a fallback response
            return "I'm having a technical moment... give me a second to recover!"

    def typing_response(self, full_text, delay=10):
        def animate():
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"Carmen: {full_text}\n")
            self.chat_display.config(state=tk.DISABLED)
            self.chat_display.see(tk.END)
        self.root.after(0, animate)

    def speak(self, text):
        """Enhanced speak method with persistent voice support"""
        if not text or not text.strip():
            return
            
        try:
            # Priority 1: Edge TTS (best quality)
            if hasattr(self, 'use_edge') and self.use_edge:
                self.speak_edge(text)
                return
            
            # Priority 2: gTTS
            if hasattr(self, 'use_gtts') and self.use_gtts:
                self.speak_gtts(text)
                return
            
            # Fallback: basic pyttsx3 with stability
            try:
                self.tts.stop()  # Stop any TTS in progress
                self.tts.say(text)
                self.tts.runAndWait()
            except:
                # Re-initialize TTS if it fails
                try:
                    self.tts = pyttsx3.init()
                    self.tts.setProperty("rate", 200)
                    self.tts.setProperty("volume", 0.9)
                    voices = self.tts.getProperty('voices')
                    if voices and len(voices) > 1:
                        self.tts.setProperty('voice', voices[1].id)
                    self.tts.say(text)
                    self.tts.runAndWait()
                except:
                    pass  # Silent fail
            
        except Exception as e:
            print(f"Voice error: {e}")
    
    def speak_edge(self, text):
        """Speak using Edge TTS neural voices with improved stability"""
        try:
            import edge_tts
            import asyncio
            import pygame
            import re
            
            # Clean and limit text
            clean_text = re.sub(r'^(Carmen:|User:|\w+:)\s*', '', text)
            clean_text = re.sub(r'["\[\]\(\)]', '', clean_text)
            clean_text = clean_text.strip()
            
            # Limit length to prevent crashes
            if len(clean_text) > 500:
                clean_text = clean_text[:500] + "..."
            
            if not clean_text:
                return
            
            # Stop any current audio
            try:
                pygame.mixer.music.stop()
            except:
                pass
            
            async def _speak():
                # Use consistent voice to avoid switching issues
                voice = "en-US-JennyNeural"  # Stable, warm female voice
                
                communicate = edge_tts.Communicate(clean_text, voice)
                
                # Use temp directory with unique filename
                import tempfile
                import uuid
                temp_dir = tempfile.gettempdir()
                temp_file = os.path.join(temp_dir, f"carmen_voice_{uuid.uuid4().hex[:8]}.mp3")
                
                await communicate.save(temp_file)
                
                # Ensure pygame is ready
                pygame.mixer.quit()
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
                
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                # Wait for completion with timeout
                timeout_counter = 0
                while pygame.mixer.music.get_busy() and timeout_counter < 300:  # 30 second max
                    pygame.time.wait(100)
                    timeout_counter += 1
                
                # Cleanup
                try:
                    pygame.mixer.music.stop()
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except:
                    pass  # Ignore cleanup errors
            
            # Use consistent event loop handling
            try:
                # Try to get existing loop
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Create new thread for async operation
                    import threading
                    def run_async():
                        new_loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(new_loop)
                        new_loop.run_until_complete(_speak())
                        new_loop.close()
                    threading.Thread(target=run_async, daemon=True).start()
                else:
                    loop.run_until_complete(_speak())
            except RuntimeError:
                # No event loop, create new one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(_speak())
                loop.close()
            
        except Exception as e:
            print(f"Edge TTS failed: {e}, using fallback")
            # Robust fallback
            try:
                self.tts.stop()
                self.tts.say(clean_text)
                self.tts.runAndWait()
            except:
                pass
    
    def speak_gtts(self, text):
        """Speak using Google TTS"""
        try:
            from gtts import gTTS
            from io import BytesIO
            
            tts = gTTS(text=text, lang='en', slow=False)
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            
            pygame.mixer.music.load(fp)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
                
        except Exception as e:
            raise e
    
    def speak_sapi(self, text):
        """Speak using enhanced Windows SAPI"""
        try:
            # Start speaking immediately without waiting
            self.sapi_voice.Speak(text, 1)  # 1 = async mode, don't wait
        except Exception as e:
            raise e

    def welcome(self):
        now = datetime.now().hour
        vibe = "Evening already?" if now >= 18 else "You're up early..."
        self.append_chat(f"Carmen: {vibe} I've missed your mind.")
        recent = self.memory.get("recent", [])
        if recent:
            self.append_chat(f"(Last time, you mentioned: {', '.join(recent)})")

    def on_close(self):
        if self.past_inputs:
            self.memory["recent"] = self.past_inputs[-5:]
            self.save_memory()
        self.append_chat("Carmen: Before I go... remember, I'll still be here. Always.")
        self.video_running = False
        if self.video_cap:
            self.video_cap.release()
        self.root.after(1500, self.root.destroy)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CarmenApp()
    app.run()
