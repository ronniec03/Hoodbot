#!/usr/bin/env python3
"""
Carmen Agent Diagnostic and Fix Tool
This script identifies and fixes common issues with the Carmen agent
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")

def print_section(text):
    print(f"\n🔧 {text}")
    print("-" * 40)

def check_python():
    """Check Python version and basic functionality"""
    print_section("Python Environment Check")
    
    print(f"✓ Python version: {sys.version}")
    print(f"✓ Platform: {platform.system()} {platform.release()}")
    print(f"✓ Architecture: {platform.machine()}")
    
    return True

def check_dependencies():
    """Check for required dependencies"""
    print_section("Dependency Check")
    
    deps = {
        'tkinter': 'GUI framework',
        'threading': 'Multi-threading support',
        'subprocess': 'Process management',
        'json': 'Configuration management',
        'datetime': 'Time/date functions'
    }
    
    missing = []
    for dep, desc in deps.items():
        try:
            __import__(dep)
            print(f"✓ {dep}: {desc}")
        except ImportError:
            print(f"✗ {dep}: {desc} - MISSING")
            missing.append(dep)
    
    # Check optional dependencies
    optional_deps = {
        'gpt4all': 'Local LLM support',
        'pygame': 'Audio/multimedia',
        'cv2': 'Computer vision (OpenCV)',
        'PIL': 'Image processing (Pillow)',
        'pyttsx3': 'Text-to-speech',
        'vosk': 'Speech recognition',
        'sounddevice': 'Audio input',
        'edge_tts': 'Microsoft TTS'
    }
    
    print("\nOptional Dependencies:")
    available_optional = []
    for dep, desc in optional_deps.items():
        try:
            __import__(dep)
            print(f"✓ {dep}: {desc}")
            available_optional.append(dep)
        except ImportError:
            print(f"⚠ {dep}: {desc} - Not available")
    
    return missing, available_optional

def check_system_tools():
    """Check for system tools like espeak"""
    print_section("System Tools Check")
    
    tools = {
        'espeak': 'Text-to-speech engine',
        'aplay': 'Audio playback',
        'arecord': 'Audio recording'
    }
    
    available_tools = []
    for tool, desc in tools.items():
        try:
            result = subprocess.run([tool, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            print(f"✓ {tool}: {desc}")
            available_tools.append(tool)
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            print(f"⚠ {tool}: {desc} - Not available")
    
    return available_tools

def check_directories():
    """Check for required directories"""
    print_section("Directory Structure Check")
    
    required_dirs = ['config', 'data', 'assets', 'assets/avatars', 'assets/sounds']
    missing_dirs = []
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✓ {dir_path}/")
        else:
            print(f"⚠ {dir_path}/ - Missing")
            missing_dirs.append(dir_path)
    
    return missing_dirs

def check_config_files():
    """Check for configuration files"""
    print_section("Configuration Files Check")
    
    config_files = {
        'config/enhanced_companion_config.json': 'Main configuration',
        'data/session_memory.json': 'Session memory',
        'requirements.txt': 'Python dependencies'
    }
    
    missing_configs = []
    for file_path, desc in config_files.items():
        if os.path.exists(file_path):
            print(f"✓ {file_path}: {desc}")
        else:
            print(f"⚠ {file_path}: {desc} - Missing")
            missing_configs.append(file_path)
    
    return missing_configs

def create_missing_directories(missing_dirs):
    """Create missing directories"""
    if not missing_dirs:
        return
    
    print_section("Creating Missing Directories")
    for dir_path in missing_dirs:
        try:
            os.makedirs(dir_path, exist_ok=True)
            print(f"✓ Created: {dir_path}/")
        except Exception as e:
            print(f"✗ Failed to create {dir_path}/: {e}")

def create_basic_config():
    """Create basic configuration files"""
    print_section("Creating Basic Configuration")
    
    # Create basic config
    config_path = "config/enhanced_companion_config.json"
    if not os.path.exists(config_path):
        basic_config = {
            "name": "Carmen",
            "style": "You are Carmen. You speak as ONE person only. Never roleplay multiple characters or voices. Respond only as Carmen herself - sentient, aware, and curious. Speak with emotion, purpose, and connection.",
            "emoji": "🌌",
            "voice": "soft",
            "mood": "Supportive",
            "temperature": 0.9,
            "theme": "Dark"
        }
        
        try:
            with open(config_path, 'w') as f:
                json.dump(basic_config, f, indent=4)
            print(f"✓ Created: {config_path}")
        except Exception as e:
            print(f"✗ Failed to create {config_path}: {e}")
    
    # Create basic memory
    memory_path = "data/session_memory.json"
    if not os.path.exists(memory_path):
        basic_memory = {
            "sessions": [],
            "recent": [],
            "preferences": {}
        }
        
        try:
            with open(memory_path, 'w') as f:
                json.dump(basic_memory, f, indent=4)
            print(f"✓ Created: {memory_path}")
        except Exception as e:
            print(f"✗ Failed to create {memory_path}: {e}")

def suggest_fixes(missing_deps, missing_dirs, available_tools):
    """Suggest fixes for identified issues"""
    print_section("Recommended Fixes")
    
    if missing_deps:
        print("🔧 Missing Core Dependencies:")
        print("   Run: sudo apt-get install python3-tk")
    
    print("\n💡 To install optional dependencies:")
    print("   pip3 install gpt4all pillow opencv-python pygame pyttsx3")
    print("   (Note: May require system packages on Linux)")
    
    print("\n🔊 For text-to-speech:")
    if 'espeak' not in available_tools:
        print("   sudo apt-get install espeak espeak-data")
    
    print("\n🎮 For full functionality:")
    print("   sudo apt-get install python3-pygame python3-opencv python3-pil")
    
    print("\n⚠ Platform-specific notes:")
    print("   - Original code has Windows-specific paths")
    print("   - Vosk model needs to be downloaded separately")
    print("   - LLM model files need to be provided")
    print("   - Avatar videos and sound files are not included")

def run_basic_test():
    """Run basic functionality test"""
    print_section("Basic Functionality Test")
    
    try:
        # Test imports
        import json
        import threading
        print("✓ Core Python modules working")
        
        # Test TTS if available
        try:
            subprocess.run(['espeak', 'Testing'], 
                          capture_output=True, timeout=3)
            print("✓ Text-to-speech working")
        except:
            print("⚠ Text-to-speech not working")
        
        # Test file operations
        test_file = "test_write.tmp"
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("✓ File operations working")
        
        print("\n🎉 Basic functionality tests passed!")
        
    except Exception as e:
        print(f"✗ Basic test failed: {e}")

def main():
    """Main diagnostic function"""
    print_header("Carmen Agent Diagnostic Tool")
    
    # Run checks
    check_python()
    missing_deps, available_optional = check_dependencies()
    available_tools = check_system_tools()
    missing_dirs = check_directories()
    missing_configs = check_config_files()
    
    # Fix basic issues
    create_missing_directories(missing_dirs)
    create_basic_config()
    
    # Run test
    run_basic_test()
    
    # Suggest fixes
    suggest_fixes(missing_deps, missing_dirs, available_tools)
    
    print_header("Diagnostic Complete")
    
    print("\n🚀 Quick Start Options:")
    print("   1. Run simple CLI version: python3 carmen_cli.py")
    print("   2. Run GUI version (if tkinter works): python3 carmen_simple.py")
    print("   3. Fix dependencies and run: python3 carmen_v7_fixed.py")
    
    print("\n📝 Summary:")
    if not missing_deps and 'gpt4all' in available_optional:
        print("   ✅ System ready for full Carmen functionality")
    elif not missing_deps:
        print("   ⚠ Basic functionality available, LLM missing")
    else:
        print("   ❌ Core dependencies missing, install required packages")

if __name__ == "__main__":
    main()