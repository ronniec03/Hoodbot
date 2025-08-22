#!/usr/bin/env python3
"""
Enhanced AI Companion System Test Suite
Tests all major components for functionality
"""

import sys
import os
import json
import sqlite3
from pathlib import Path

def print_status(test_name, status, details=""):
    """Print test status with formatting"""
    status_symbol = "✓" if status else "✗"
    status_color = "\033[92m" if status else "\033[91m"
    reset_color = "\033[0m"
    
    print(f"{status_color}{status_symbol} {test_name}{reset_color}")
    if details:
        print(f"  {details}")

def test_python_version():
    """Test Python version compatibility"""
    version = sys.version_info
    required = (3, 9)
    
    if version >= required:
        print_status("Python Version", True, f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_status("Python Version", False, f"Required: Python {required[0]}.{required[1]}+, Found: {version.major}.{version.minor}")
        return False

def test_dependencies():
    """Test if required dependencies are installed"""
    required_modules = [
        "tkinter",
        "PIL",
        "pygame",
        "numpy",
        "pyttsx3"
    ]
    
    optional_modules = [
        "gpt4all",
        "edge_tts", 
        "gtts",
        "speech_recognition",
        "anthropic",
        "openai"
    ]
    
    missing_required = []
    missing_optional = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_required.append(module)
    
    for module in optional_modules:
        try:
            __import__(module)
        except ImportError:
            missing_optional.append(module)
    
    if not missing_required:
        print_status("Required Dependencies", True, f"All {len(required_modules)} required modules available")
        success = True
    else:
        print_status("Required Dependencies", False, f"Missing: {', '.join(missing_required)}")
        success = False
    
    if missing_optional:
        print_status("Optional Dependencies", False, f"Missing: {', '.join(missing_optional)}")
    else:
        print_status("Optional Dependencies", True, "All optional modules available")
    
    return success

def test_configuration_files():
    """Test if configuration files exist and are valid"""
    config_dir = Path("config")
    required_configs = [
        "claude_config.json",
        "openai_config.json", 
        "stt_config.json",
        "tts_config.json"
    ]
    
    if not config_dir.exists():
        print_status("Configuration Directory", False, "config/ directory not found")
        return False
    
    print_status("Configuration Directory", True, "config/ directory exists")
    
    all_valid = True
    for config_file in required_configs:
        config_path = config_dir / config_file
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    json.load(f)
                print_status(f"Config: {config_file}", True, "Valid JSON")
            except json.JSONDecodeError:
                print_status(f"Config: {config_file}", False, "Invalid JSON format")
                all_valid = False
        else:
            print_status(f"Config: {config_file}", False, "File not found")
            all_valid = False
    
    return all_valid

def test_database_operations():
    """Test SQLite database operations"""
    try:
        # Test basic SQLite functionality
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        
        # Create a test table
        cursor.execute("""
            CREATE TABLE test_conversation (
                id INTEGER PRIMARY KEY,
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert test data
        cursor.execute("INSERT INTO test_conversation (message) VALUES (?)", ("Test message",))
        
        # Query test data
        cursor.execute("SELECT * FROM test_conversation")
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            print_status("Database Operations", True, "SQLite operations working")
            return True
        else:
            print_status("Database Operations", False, "No data retrieved")
            return False
            
    except Exception as e:
        print_status("Database Operations", False, f"Error: {str(e)}")
        return False

def test_audio_system():
    """Test audio system functionality"""
    audio_tests = []
    
    # Test pygame
    try:
        import pygame
        pygame.mixer.init()
        audio_tests.append(("Pygame Audio", True, "Audio mixer initialized"))
        pygame.mixer.quit()
    except Exception as e:
        audio_tests.append(("Pygame Audio", False, f"Error: {str(e)}"))
    
    # Test pyttsx3
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if voices:
            audio_tests.append(("TTS Engine", True, f"Found {len(voices)} voices"))
        else:
            audio_tests.append(("TTS Engine", False, "No voices found"))
        engine.stop()
    except Exception as e:
        audio_tests.append(("TTS Engine", False, f"Error: {str(e)}"))
    
    success = all(test[1] for test in audio_tests)
    for test_name, status, details in audio_tests:
        print_status(test_name, status, details)
    
    return success

def test_ai_model_availability():
    """Test if AI models are available"""
    ai_tests = []
    
    # Test local LLM
    try:
        import gpt4all
        ai_tests.append(("GPT4All", True, "Local LLM support available"))
    except ImportError:
        ai_tests.append(("GPT4All", False, "Not installed"))
    
    # Test API configurations
    config_dir = Path("config")
    
    if (config_dir / "claude_config.json").exists():
        try:
            with open(config_dir / "claude_config.json", 'r') as f:
                config = json.load(f)
                if config.get("api_key") and config["api_key"] != "YOUR_ANTHROPIC_API_KEY_HERE":
                    ai_tests.append(("Claude API", True, "API key configured"))
                else:
                    ai_tests.append(("Claude API", False, "API key not configured"))
        except:
            ai_tests.append(("Claude API", False, "Configuration error"))
    else:
        ai_tests.append(("Claude API", False, "Config file missing"))
    
    if (config_dir / "openai_config.json").exists():
        try:
            with open(config_dir / "openai_config.json", 'r') as f:
                config = json.load(f)
                if config.get("api_key") and config["api_key"] != "YOUR_OPENAI_API_KEY_HERE":
                    ai_tests.append(("OpenAI API", True, "API key configured"))
                else:
                    ai_tests.append(("OpenAI API", False, "API key not configured"))
        except:
            ai_tests.append(("OpenAI API", False, "Configuration error"))
    else:
        ai_tests.append(("OpenAI API", False, "Config file missing"))
    
    for test_name, status, details in ai_tests:
        print_status(test_name, status, details)
    
    return any(test[1] for test in ai_tests)

def test_main_application():
    """Test if main application file exists and is valid Python"""
    main_app = "carmen_v7_fixed.py"
    
    if not os.path.exists(main_app):
        print_status("Main Application", False, f"{main_app} not found")
        return False
    
    try:
        with open(main_app, 'r') as f:
            content = f.read()
            # Basic validation - check for required class/functions
            if "class CarmenApp" in content:
                print_status("Main Application", True, f"{main_app} appears valid")
                return True
            else:
                print_status("Main Application", False, "Main class not found")
                return False
    except Exception as e:
        print_status("Main Application", False, f"Error reading file: {str(e)}")
        return False

def main():
    """Run all system tests"""
    print("Enhanced AI Companion - System Test Suite")
    print("=" * 45)
    print()
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Configuration", test_configuration_files),
        ("Database", test_database_operations),
        ("Audio System", test_audio_system),
        ("AI Models", test_ai_model_availability),
        ("Main Application", test_main_application)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} Tests ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_status(f"{test_name} Test", False, f"Unexpected error: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 45)
    print("TEST SUMMARY")
    print("=" * 45)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status_symbol = "✓" if result else "✗"
        print(f"{status_symbol} {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All systems ready! You can launch the Enhanced AI Companion.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} issues found. Check the details above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    input("\nPress Enter to exit...")
    sys.exit(exit_code)