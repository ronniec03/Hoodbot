#!/usr/bin/env python3
"""
Carmen Agent - Command Line Debug Version
This version works in terminal without GUI dependencies
"""

import os
import json
import threading
import subprocess
import time
from datetime import datetime
import random

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
            "I'm here, listening and responding as best I can in debug mode.",
            "That's an interesting thought. In debug mode, I can still engage with your ideas.",
            "I'm functioning, just in a more basic way than my full version.",
            "Even in this simplified state, I want to be helpful to you."
        ]
        # Add some context-aware responses
        if "how are you" in prompt.lower():
            return "I'm doing well in debug mode! All my basic systems are functioning."
        elif "test" in prompt.lower():
            return "Testing... testing... yes, I'm working! My core responses are active."
        elif "problem" in prompt.lower() or "issue" in prompt.lower():
            return "I understand you're facing some challenges. Even in debug mode, I'm here to help however I can."
        elif "hello" in prompt.lower() or "hi" in prompt.lower():
            return "Hello! It's good to connect with you. I'm running in debug mode but I'm here."
        else:
            return random.choice(responses)

# Simple TTS using system espeak
def simple_speak(text):
    """Simple text-to-speech using espeak"""
    try:
        subprocess.run(['espeak', '-s', '160', '-v', 'en+f3', text], 
                      check=False, capture_output=True)
    except Exception as e:
        print(f"[TTS Error: {e}]")

class CarmenCLI:
    def __init__(self):
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
        
        # TTS enabled flag
        self.tts_enabled = True
        
        print("🤖 Carmen Debug Mode - Command Line Interface")
        print("=" * 50)
        self.welcome()
    
    def welcome(self):
        """Show welcome message"""
        now = datetime.now().hour
        if now < 12:
            greeting = "Good morning"
        elif now < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"
        
        welcome_msg = f"{greeting}! I'm Carmen running in debug mode."
        print(f"\n🌟 Carmen: {welcome_msg}")
        print("💬 Type your message and press Enter to chat.")
        print("🔧 Commands: /help, /tts on/off, /clear, /quit")
        print()
        
        if self.tts_enabled:
            threading.Thread(target=simple_speak, args=(welcome_msg,), daemon=True).start()
    
    def process_command(self, user_input):
        """Process special commands"""
        if user_input.startswith('/'):
            command = user_input.lower().strip()
            
            if command == '/help':
                print("\n🆘 Available commands:")
                print("  /help     - Show this help")
                print("  /tts on   - Enable text-to-speech")
                print("  /tts off  - Disable text-to-speech")
                print("  /clear    - Clear chat history")
                print("  /quit     - Exit Carmen")
                print("  /test     - Test basic functionality")
                print()
                return True
            
            elif command == '/tts on':
                self.tts_enabled = True
                print("🔊 Text-to-speech enabled")
                return True
            
            elif command == '/tts off':
                self.tts_enabled = False
                print("🔇 Text-to-speech disabled")
                return True
            
            elif command == '/clear':
                self.chat_history = []
                print("\n" + "="*50)
                print("💾 Chat history cleared")
                self.welcome()
                return True
            
            elif command == '/test':
                print("🧪 Testing Carmen debug mode...")
                print("  ✓ Mock LLM initialized")
                print("  ✓ Basic I/O working")
                print("  ✓ Command processing active")
                try:
                    subprocess.run(['espeak', '--version'], 
                                  check=True, capture_output=True)
                    print("  ✓ Text-to-speech available")
                except:
                    print("  ⚠ Text-to-speech not available")
                print("🎉 All basic systems operational!")
                return True
            
            elif command == '/quit':
                return False
            
            else:
                print(f"❓ Unknown command: {command}")
                print("💡 Type /help for available commands")
                return True
        
        return None  # Not a command
    
    def get_response(self, user_input):
        """Get response from mock LLM"""
        try:
            print("🤔 Carmen: [thinking...]", end="", flush=True)
            time.sleep(0.5)  # Simulate processing
            print("\r" + " "*25 + "\r", end="", flush=True)  # Clear thinking
            
            response = self.llm.generate(f"User said: {user_input}")
            return response
            
        except Exception as e:
            return f"I encountered an error: {e}"
    
    def chat_loop(self):
        """Main chat loop"""
        try:
            while True:
                # Get user input
                try:
                    user_input = input("You: ").strip()
                except (EOFError, KeyboardInterrupt):
                    break
                
                if not user_input:
                    continue
                
                # Process commands
                command_result = self.process_command(user_input)
                if command_result is False:  # /quit
                    break
                elif command_result is True:  # Other commands
                    continue
                
                # Add to history
                self.chat_history.append(f"You: {user_input}")
                
                # Get and display response
                response = self.get_response(user_input)
                print(f"🤖 Carmen: {response}")
                
                # Add response to history
                self.chat_history.append(f"Carmen: {response}")
                
                # Speak response if enabled
                if self.tts_enabled:
                    threading.Thread(target=simple_speak, args=(response,), daemon=True).start()
                
                print()  # Add spacing
                
        except KeyboardInterrupt:
            pass
        
        # Goodbye message
        goodbye = "Until next time... goodbye!"
        print(f"\n🌙 Carmen: {goodbye}")
        if self.tts_enabled:
            simple_speak(goodbye)
        time.sleep(1)

def main():
    """Main function"""
    print("Starting Carmen Debug Mode...")
    print("📋 Available features:")
    print("  - Command line chat interface")
    print("  - Mock LLM responses")
    print("  - Simple TTS via espeak (if available)")
    print("  - No model files required")
    print("  - Basic command system")
    print()
    
    try:
        carmen = CarmenCLI()
        carmen.chat_loop()
    except Exception as e:
        print(f"❌ Error starting Carmen: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()