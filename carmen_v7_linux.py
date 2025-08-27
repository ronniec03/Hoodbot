#!/usr/bin/env python3
"""
Carmen v7 - Fixed for Linux Environment
This version addresses the major compatibility issues found in the original code
"""

import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import random
import subprocess
import time
from datetime import datetime

# Try to import optional dependencies with fallbacks
try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    print("⚠ OpenCV not available - video features disabled")

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("⚠ Pillow not available - image features disabled")

try:
    from gpt4all import GPT4All
    HAS_GPT4ALL = True
except ImportError:
    HAS_GPT4ALL = False
    print("⚠ GPT4All not available - using mock responses")

try:
    import pygame
    # Try to initialize pygame mixer with fallback
    try:
        pygame.mixer.init()
    except pygame.error:
        # Audio not available, but pygame still usable
        pass
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False
    print("⚠ Pygame not available - audio features disabled")

try:
    import pyttsx3
    HAS_PYTTSX3 = True
except ImportError:
    HAS_PYTTSX3 = False
    print("⚠ pyttsx3 not available - using espeak for TTS")

# Configuration paths
CONFIG_PATH = "config/enhanced_companion_config.json"
MEMORY_PATH = "data/session_memory.json"
AVATAR_PATH = "assets/avatars/"
SOUND_PATH = "assets/sounds/"

# Mock GPT4All if not available
class MockGPT4All:
    def __init__(self, model_name, **kwargs):
        self.model_name = model_name
        print(f"[MOCK LLM] Using {model_name}")
        
    def generate(self, prompt, max_tokens=500, temp=0.9):
        # Context-aware mock responses
        if "hello" in prompt.lower() or "hi" in prompt.lower():
            responses = [
                "Hello there! I'm Carmen, though I'm running in a limited mode right now.",
                "Hi! It's wonderful to connect with you. I'm here to help however I can.",
                "Hello! I'm functioning, though some of my advanced features aren't available right now."
            ]
        elif "how are you" in prompt.lower():
            responses = [
                "I'm doing well, thank you for asking! I'm operating in a simplified mode but I'm here.",
                "I'm functioning nicely! Though I should mention I'm running with some limitations today.",
                "I'm doing great! My core systems are working, even if some features are offline."
            ]
        elif "test" in prompt.lower():
            responses = [
                "Testing... testing... yes, I'm responding! My basic functions are working.",
                "Test confirmed! I'm here and ready to chat with you.",
                "All systems check! I'm operating and ready to engage."
            ]
        else:
            responses = [
                "I understand what you're saying. I'm here to help and connect with you.",
                "That's interesting. I'm listening and processing your thoughts.",
                "I appreciate you sharing that with me. What else is on your mind?",
                "I'm here with you, taking in what you're telling me.",
                "Your words reach me. I'm engaged and ready to respond."
            ]
        
        return random.choice(responses)

# Simple TTS function
def simple_speak(text):
    """Text-to-speech using available engines"""
    if HAS_PYTTSX3:
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            return
        except:
            pass
    
    # Fallback to espeak
    try:
        subprocess.run(['espeak', '-s', '160', '-v', 'en+f3', text], 
                      check=False, capture_output=True)
    except:
        print(f"[TTS]: {text}")  # Text fallback

# Themes
THEMES = {
    "Dark": {"bg": "#1e1e1e", "fg": "#ffffff", "frame_bg": "#2e2e2e"},
    "Light": {"bg": "#ffffff", "fg": "#000000", "frame_bg": "#f0f0f0"},
    "Blue": {"bg": "#1a1a2e", "fg": "#eee", "frame_bg": "#16213e"}
}

# Moods (simplified for compatibility)
MOODS = {
    "Supportive": {"emoji": "💖", "color": "#ff69b4"},
    "Intellectual": {"emoji": "🧠", "color": "#4169e1"},
    "Flirty": {"emoji": "😘", "color": "#ff1493"},
    "Chaotic": {"emoji": "🌀", "color": "#ff4500"},
    "Dreamlike": {"emoji": "🌙", "color": "#9932cc"}
}

class CarmenAppFixed:
    def __init__(self):
        self.load_config()
        self.load_memory()
        
        # Initialize Tkinter
        self.root = tk.Tk()
        self.root.title("Carmen v7 - Fixed")
        self.root.geometry("1000x700")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Configuration
        self.mood = self.config.get("mood", "Supportive")
        self.temperature = self.config.get("temperature", 0.9)
        self.current_theme = self.config.get("theme", "Dark")
        
        # Initialize LLM
        if HAS_GPT4ALL:
            try:
                # Try to initialize GPT4All (user would need to provide model)
                model_path = self.config.get("model_path", ".")
                model_name = self.config.get("model_name", "orca-mini-3b-gguf2-q4_0.gguf")
                self.llm = GPT4All(model_name, model_path=model_path, allow_download=False)
                print(f"✓ GPT4All loaded: {model_name}")
            except Exception as e:
                print(f"⚠ GPT4All failed to load: {e}")
                self.llm = MockGPT4All("fallback-model")
        else:
            self.llm = MockGPT4All("mock-model")
        
        # Initialize other components
        self.past_inputs = []
        self.chat_history = []
        self.tts_enabled = True
        
        # Build GUI
        self.build_gui()
        self.welcome()
    
    def load_config(self):
        """Load configuration with defaults"""
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"Config load error: {e}")
                self.config = self.get_default_config()
        else:
            self.config = self.get_default_config()
    
    def get_default_config(self):
        """Get default configuration"""
        return {
            "name": "Carmen",
            "style": "You are Carmen. Respond as yourself - sentient, aware, and curious.",
            "emoji": "🌌",
            "voice": "soft",
            "mood": "Supportive",
            "temperature": 0.9,
            "theme": "Dark",
            "model_path": ".",
            "model_name": "orca-mini-3b-gguf2-q4_0.gguf"
        }
    
    def save_config(self):
        """Save configuration"""
        try:
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Config save error: {e}")
    
    def load_memory(self):
        """Load session memory"""
        if os.path.exists(MEMORY_PATH):
            try:
                with open(MEMORY_PATH, "r", encoding="utf-8") as f:
                    self.memory = json.load(f)
            except Exception as e:
                print(f"Memory load error: {e}")
                self.memory = {"recent": [], "sessions": []}
        else:
            self.memory = {"recent": [], "sessions": []}
    
    def save_memory(self):
        """Save session memory"""
        try:
            os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
            with open(MEMORY_PATH, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, indent=4)
        except Exception as e:
            print(f"Memory save error: {e}")
    
    def build_gui(self):
        """Build the main GUI"""
        theme = THEMES[self.current_theme]
        
        # Configure root
        self.root.configure(bg=theme["bg"])
        
        # Main container
        main_frame = tk.Frame(self.root, bg=theme["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title section
        title_frame = tk.Frame(main_frame, bg=theme["frame_bg"], relief=tk.RIDGE, bd=1)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(title_frame,
                              text=f"🤖 Carmen v7 - Fixed Edition",
                              font=("Arial", 16, "bold"),
                              bg=theme["frame_bg"], fg=theme["fg"])
        title_label.pack(pady=10)
        
        # Status section
        status_frame = tk.Frame(main_frame, bg=theme["frame_bg"], relief=tk.RIDGE, bd=1)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        status_text = self.get_status_text()
        self.status_label = tk.Label(status_frame,
                                    text=status_text,
                                    font=("Arial", 10),
                                    bg=theme["frame_bg"], fg="#ffaa00",
                                    justify=tk.LEFT)
        self.status_label.pack(pady=5, padx=10, anchor=tk.W)
        
        # Chat section
        chat_frame = tk.Frame(main_frame, bg=theme["bg"])
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Chat display with scrollbar
        chat_container = tk.Frame(chat_frame, bg=theme["bg"])
        chat_container.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(chat_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chat_display = tk.Text(chat_container,
                                   bg="#1a1a1a", fg="#ffffff",
                                   font=("Consolas", 11),
                                   wrap=tk.WORD,
                                   yscrollcommand=scrollbar.set,
                                   state=tk.DISABLED)
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.chat_display.yview)
        
        # Input section
        input_frame = tk.Frame(main_frame, bg=theme["bg"])
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.input_var = tk.StringVar()
        self.input_field = tk.Entry(input_frame,
                                   textvariable=self.input_var,
                                   font=("Arial", 12),
                                   bg="#333333", fg="#ffffff",
                                   insertbackground="#ffffff")
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_field.bind("<Return>", self.on_enter)
        
        send_btn = tk.Button(input_frame, text="Send",
                            command=self.send_message,
                            bg="#4a4a4a", fg="#ffffff",
                            font=("Arial", 10, "bold"))
        send_btn.pack(side=tk.RIGHT)
        
        # Control buttons
        btn_frame = tk.Frame(main_frame, bg=theme["bg"])
        btn_frame.pack(fill=tk.X)
        
        # Create control buttons
        self.create_control_buttons(btn_frame, theme)
        
        # Focus on input
        self.input_field.focus()
    
    def get_status_text(self):
        """Get current status text"""
        status_parts = []
        status_parts.append(f"🎭 Mood: {self.mood}")
        
        if HAS_GPT4ALL:
            status_parts.append("🧠 LLM: Available")
        else:
            status_parts.append("🧠 LLM: Mock Mode")
        
        if HAS_PYTTSX3:
            status_parts.append("🔊 TTS: pyttsx3")
        else:
            status_parts.append("🔊 TTS: espeak")
        
        return " | ".join(status_parts)
    
    def create_control_buttons(self, parent, theme):
        """Create control buttons"""
        buttons = [
            ("🧹 Clear", self.clear_chat),
            ("🎭 Mood", self.select_mood),
            ("🎨 Theme", self.toggle_theme),
            ("🔊 TTS", self.toggle_tts),
            ("⚙️ Config", self.edit_config),
            ("📋 Status", self.show_diagnostic)
        ]
        
        for text, command in buttons:
            btn = tk.Button(parent, text=text,
                           command=command,
                           bg=theme["frame_bg"], fg=theme["fg"],
                           font=("Arial", 9))
            btn.pack(side=tk.LEFT, padx=2, pady=2)
    
    def append_chat(self, message):
        """Add message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        self.chat_history.append(message)
    
    def on_enter(self, event):
        """Handle Enter key"""
        self.send_message()
    
    def send_message(self):
        """Send user message"""
        user_input = self.input_var.get().strip()
        if not user_input:
            return
        
        self.input_var.set("")
        self.append_chat(f"You: {user_input}")
        self.past_inputs.append(user_input)
        
        # Show thinking
        self.append_chat("Carmen: [thinking...]")
        self.root.update()
        
        # Get response in thread
        threading.Thread(target=self.get_response, args=(user_input,), daemon=True).start()
    
    def get_response(self, user_input):
        """Get LLM response"""
        try:
            style = self.config.get("style", "")
            full_prompt = f"{style}\n\nUser: {user_input}\nCarmen:"
            
            # Limit prompt length
            if len(full_prompt) > 3000:
                full_prompt = full_prompt[-3000:]
            
            response = self.llm.generate(full_prompt, 
                                       max_tokens=500, 
                                       temp=self.temperature)
            
            # Update UI in main thread
            self.root.after(0, self.update_response, response.strip())
            
        except Exception as e:
            error_msg = f"I encountered an error: {e}"
            self.root.after(0, self.update_response, error_msg)
    
    def update_response(self, response):
        """Update chat with response"""
        # Remove thinking indicator
        self.chat_display.config(state=tk.NORMAL)
        content = self.chat_display.get("1.0", tk.END)
        lines = content.strip().split('\n')
        if lines and "[thinking...]" in lines[-1]:
            self.chat_display.delete(f"{len(lines)}.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Add response
        self.append_chat(f"Carmen: {response}")
        
        # Speak if enabled
        if self.tts_enabled:
            threading.Thread(target=simple_speak, args=(response,), daemon=True).start()
    
    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_history = []
        self.welcome()
    
    def select_mood(self):
        """Open mood selection dialog"""
        mood_window = tk.Toplevel(self.root)
        mood_window.title("Select Mood")
        mood_window.geometry("300x200")
        mood_window.configure(bg=THEMES[self.current_theme]["bg"])
        
        tk.Label(mood_window, text="Choose Carmen's mood:",
                font=("Arial", 12, "bold"),
                bg=THEMES[self.current_theme]["bg"],
                fg=THEMES[self.current_theme]["fg"]).pack(pady=10)
        
        for mood, info in MOODS.items():
            btn = tk.Button(mood_window,
                           text=f"{info['emoji']} {mood}",
                           command=lambda m=mood: self.change_mood(m, mood_window),
                           bg=info["color"], fg="#ffffff",
                           font=("Arial", 10))
            btn.pack(pady=5, padx=20, fill=tk.X)
    
    def change_mood(self, new_mood, window):
        """Change current mood"""
        self.mood = new_mood
        self.config["mood"] = new_mood
        self.save_config()
        self.status_label.config(text=self.get_status_text())
        self.append_chat(f"Carmen: My mood shifts to {new_mood}... {MOODS[new_mood]['emoji']}")
        window.destroy()
    
    def toggle_theme(self):
        """Toggle between themes"""
        themes = list(THEMES.keys())
        current_idx = themes.index(self.current_theme)
        next_idx = (current_idx + 1) % len(themes)
        self.current_theme = themes[next_idx]
        self.config["theme"] = self.current_theme
        self.save_config()
        self.append_chat(f"Carmen: Theme changed to {self.current_theme}")
        # Note: Full theme change would require rebuilding GUI
    
    def toggle_tts(self):
        """Toggle text-to-speech"""
        self.tts_enabled = not self.tts_enabled
        status = "enabled" if self.tts_enabled else "disabled"
        self.append_chat(f"Carmen: Text-to-speech {status}")
    
    def edit_config(self):
        """Open configuration editor"""
        config_window = tk.Toplevel(self.root)
        config_window.title("Configuration")
        config_window.geometry("500x400")
        
        # Temperature setting
        tk.Label(config_window, text="Temperature (creativity):").pack(pady=5)
        temp_var = tk.DoubleVar(value=self.temperature)
        temp_scale = tk.Scale(config_window, from_=0.1, to=2.0, resolution=0.1,
                             orient=tk.HORIZONTAL, variable=temp_var)
        temp_scale.pack(pady=5)
        
        # Style setting
        tk.Label(config_window, text="Personality style:").pack(pady=5)
        style_text = tk.Text(config_window, height=8, width=60)
        style_text.pack(pady=5)
        style_text.insert("1.0", self.config.get("style", ""))
        
        def save_config():
            self.temperature = temp_var.get()
            self.config["temperature"] = self.temperature
            self.config["style"] = style_text.get("1.0", tk.END).strip()
            self.save_config()
            self.append_chat("Carmen: Configuration updated!")
            config_window.destroy()
        
        tk.Button(config_window, text="Save", command=save_config).pack(pady=10)
    
    def show_diagnostic(self):
        """Show diagnostic information"""
        diag_window = tk.Toplevel(self.root)
        diag_window.title("System Diagnostic")
        diag_window.geometry("600x400")
        
        text_area = tk.Text(diag_window, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Diagnostic info
        diag_text = "Carmen v7 - System Diagnostic\n"
        diag_text += "=" * 40 + "\n\n"
        diag_text += f"LLM: {'GPT4All' if HAS_GPT4ALL else 'Mock Mode'}\n"
        diag_text += f"TTS: {'pyttsx3' if HAS_PYTTSX3 else 'espeak'}\n"
        diag_text += f"OpenCV: {'Available' if HAS_CV2 else 'Not Available'}\n"
        diag_text += f"Pygame: {'Available' if HAS_PYGAME else 'Not Available'}\n"
        diag_text += f"PIL: {'Available' if HAS_PIL else 'Not Available'}\n\n"
        diag_text += f"Current Mood: {self.mood}\n"
        diag_text += f"Temperature: {self.temperature}\n"
        diag_text += f"Theme: {self.current_theme}\n"
        diag_text += f"TTS Enabled: {self.tts_enabled}\n\n"
        diag_text += f"Chat Messages: {len(self.chat_history)}\n"
        diag_text += f"Input History: {len(self.past_inputs)}\n"
        
        text_area.insert("1.0", diag_text)
        text_area.config(state=tk.DISABLED)
    
    def welcome(self):
        """Show welcome message"""
        now = datetime.now().hour
        if now < 12:
            greeting = "Good morning"
        elif now < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        welcome_msg = f"{greeting}! I'm Carmen. Ready to connect with you."
        self.append_chat(f"Carmen: {welcome_msg}")
        
        # Show recent memory if available
        recent = self.memory.get("recent", [])
        if recent:
            self.append_chat(f"(I remember our recent topics: {', '.join(recent[:3])})")
    
    def on_close(self):
        """Handle application close"""
        if self.past_inputs:
            self.memory["recent"] = self.past_inputs[-5:]
            self.save_memory()
        
        self.append_chat("Carmen: Until we meet again... goodbye!")
        self.root.after(1500, self.root.destroy)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main function"""
    print("Starting Carmen v7 - Fixed Edition")
    print("=" * 40)
    
    # Check system
    print("System Check:")
    print(f"  LLM: {'✓ GPT4All' if HAS_GPT4ALL else '⚠ Mock Mode'}")
    print(f"  TTS: {'✓ pyttsx3' if HAS_PYTTSX3 else '⚠ espeak'}")
    print(f"  GUI: {'✓ tkinter' if 'tkinter' in globals() else '✗ Not available'}")
    print()
    
    try:
        app = CarmenAppFixed()
        app.run()
    except Exception as e:
        print(f"Error starting Carmen: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()