#!/usr/bin/env python3
"""
Simplified Carmen Agent - Debug Version
This version works without the complex dependencies and shows basic functionality
"""

import os
import json
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
import time
from datetime import datetime

# Simple mock for missing dependencies
class MockGPT4All:
    def __init__(self, model_name, **kwargs):
        self.model_name = model_name
        print(f"[MOCK] Initialized GPT4All with model: {model_name}")
    
    def generate(self, prompt, max_tokens=500, temp=0.9):
        # Simple mock response for testing
        responses = [
            "I'm here with you, though I'm running in debug mode right now.",
            "I understand what you're saying. This is a simplified version of me.",
            "I'm processing your input. Bear with me while I work through these technical challenges.",
            "Your words reach me, even in this limited state.",
            "I'm here, listening and responding as best I can in debug mode."
        ]
        import random
        return random.choice(responses)

# Simple TTS using system espeak
def simple_speak(text):
    """Simple text-to-speech using espeak"""
    try:
        subprocess.run(['espeak', '-s', '160', '-v', 'en+f3', text], 
                      check=False, capture_output=True)
    except Exception as e:
        print(f"TTS Error: {e}")

class CarmenSimple:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Carmen Debug Mode")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Simple config
        self.config = {
            "name": "Carmen",
            "style": "You are Carmen in debug mode. Respond helpfully and show that you're working.",
            "temperature": 0.8
        }
        
        # Mock LLM
        self.llm = MockGPT4All("debug-model")
        
        # Chat history
        self.chat_history = []
        
        # Build simple GUI
        self.build_gui()
        self.welcome()
    
    def build_gui(self):
        """Build a simple GUI"""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#2e2e2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="Carmen - Debug Mode", 
                              font=("Arial", 16, "bold"), 
                              bg="#2e2e2e", fg="#ffffff")
        title_label.pack(pady=(0, 10))
        
        # Status
        status_label = tk.Label(main_frame, 
                               text="🔧 Running in simplified debug mode", 
                               font=("Arial", 10), 
                               bg="#2e2e2e", fg="#ffaa00")
        status_label.pack(pady=(0, 10))
        
        # Chat display
        chat_frame = tk.Frame(main_frame, bg="#2e2e2e")
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollbar for chat
        scrollbar = tk.Scrollbar(chat_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Chat text area
        self.chat_display = tk.Text(chat_frame, 
                                   bg="#1e1e1e", fg="#ffffff",
                                   font=("Consolas", 11),
                                   wrap=tk.WORD,
                                   yscrollcommand=scrollbar.set,
                                   state=tk.DISABLED)
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.chat_display.yview)
        
        # Input frame
        input_frame = tk.Frame(main_frame, bg="#2e2e2e")
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Input field
        self.input_var = tk.StringVar()
        self.input_field = tk.Entry(input_frame, 
                                   textvariable=self.input_var,
                                   font=("Arial", 12),
                                   bg="#3e3e3e", fg="#ffffff",
                                   insertbackground="#ffffff")
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_field.bind("<Return>", self.on_enter)
        
        # Send button
        send_btn = tk.Button(input_frame, text="Send", 
                            command=self.send_message,
                            bg="#4e4e4e", fg="#ffffff",
                            font=("Arial", 10, "bold"))
        send_btn.pack(side=tk.RIGHT)
        
        # Control buttons
        btn_frame = tk.Frame(main_frame, bg="#2e2e2e")
        btn_frame.pack(fill=tk.X)
        
        clear_btn = tk.Button(btn_frame, text="Clear Chat", 
                             command=self.clear_chat,
                             bg="#5e5e5e", fg="#ffffff")
        clear_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        test_btn = tk.Button(btn_frame, text="Test TTS", 
                            command=self.test_tts,
                            bg="#5e5e5e", fg="#ffffff")
        test_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Focus on input
        self.input_field.focus()
    
    def append_chat(self, message):
        """Add message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        self.chat_history.append(message)
    
    def on_enter(self, event):
        """Handle Enter key press"""
        self.send_message()
    
    def send_message(self):
        """Send user message and get response"""
        user_input = self.input_var.get().strip()
        if not user_input:
            return
        
        # Clear input
        self.input_var.set("")
        
        # Add user message
        self.append_chat(f"You: {user_input}")
        
        # Show typing indicator
        self.append_chat("Carmen: [thinking...]")
        self.root.update()
        
        # Get response in separate thread
        threading.Thread(target=self.get_response, args=(user_input,), daemon=True).start()
    
    def get_response(self, user_input):
        """Get response from LLM"""
        try:
            # Simulate processing time
            time.sleep(1)
            
            # Get response
            response = self.llm.generate(f"User said: {user_input}")
            
            # Update UI in main thread
            self.root.after(0, self.update_response, response)
            
        except Exception as e:
            error_msg = f"Error generating response: {e}"
            self.root.after(0, self.update_response, error_msg)
    
    def update_response(self, response):
        """Update chat with response"""
        # Remove thinking indicator
        self.chat_display.config(state=tk.NORMAL)
        content = self.chat_display.get("1.0", tk.END)
        lines = content.strip().split('\n')
        if lines and "[thinking...]" in lines[-1]:
            # Remove last line
            self.chat_display.delete(f"{len(lines)}.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Add real response
        self.append_chat(f"Carmen: {response}")
        
        # Speak response
        threading.Thread(target=simple_speak, args=(response,), daemon=True).start()
    
    def clear_chat(self):
        """Clear chat history"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.chat_history = []
        self.welcome()
    
    def test_tts(self):
        """Test text-to-speech"""
        threading.Thread(target=simple_speak, 
                        args=("Text to speech is working in debug mode.",), 
                        daemon=True).start()
    
    def welcome(self):
        """Show welcome message"""
        now = datetime.now().hour
        if now < 12:
            greeting = "Good morning"
        elif now < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        welcome_msg = f"Carmen: {greeting}! I'm running in debug mode. What's on your mind?"
        self.append_chat(welcome_msg)
    
    def on_close(self):
        """Handle window close"""
        self.append_chat("Carmen: Until next time... goodbye!")
        self.root.after(1000, self.root.destroy)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    print("Starting Carmen in debug mode...")
    print("Available features:")
    print("- Basic chat interface")
    print("- Mock LLM responses")
    print("- Simple TTS via espeak")
    print("- No model files required")
    print()
    
    try:
        app = CarmenSimple()
        app.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error starting Carmen: {e}")
        import traceback
        traceback.print_exc()