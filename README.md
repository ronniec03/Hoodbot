# Enhanced AI Companion - Arielle

An advanced AI companion application with voice recognition, multiple AI model support, and romantic personality features.

## 🌟 Features

### Core Functionality
- **Advanced Voice Recognition**: Multi-method speech-to-text with Google and offline fallback
- **Enhanced Text-to-Speech**: High-quality voices using Microsoft Edge TTS
- **Multiple AI Models**: Support for Claude, GPT-4, and local LLM models
- **Romantic Personality Layer**: Emotional intelligence and relationship depth tracking
- **Conversation Memory**: SQLite database with mood tracking and statistics
- **Hands-Free Mode**: Continuous voice interaction support

### Voice Features
- **High-Quality TTS**: Microsoft Edge neural voices (AriaNeural, JennyNeural, etc.)
- **Noise Filtering**: Advanced audio processing with ambient noise adjustment
- **Multiple Recognition Methods**: Google Web Speech API with offline Sphinx fallback
- **Voice Controls**: Adjustable speed, volume, and recognition sensitivity
- **Audio Optimization**: Pygame-based playback with fallback support

### AI Integration
- **Claude Integration**: Anthropic's Claude 3.5 Sonnet support
- **OpenAI Integration**: GPT-4 and GPT-3.5 Turbo support  
- **Local LLM Support**: llama.cpp integration for offline models
- **Dynamic Model Switching**: Switch between models without restart
- **Response Enhancement**: Romantic personality layer for all AI responses

### User Experience
- **Modern GUI**: Dark theme with romantic color scheme
- **Mood Detection**: Automatic emotional state recognition
- **Relationship Tracking**: Intimacy level and conversation depth monitoring
- **Session Statistics**: Real-time conversation and voice usage stats
- **Customizable Settings**: Adjustable AI creativity, voice parameters, and more

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10/11 (primary), Linux/macOS (limited support)
- **Python**: 3.9 or higher
- **RAM**: 4GB minimum (8GB recommended for local LLMs)
- **Storage**: 2GB free space (more for local models)
- **Audio**: Microphone and speakers/headphones

### Python Dependencies
```
pillow>=10.0.0          # Image processing
pygame>=2.5.0           # Audio playback
edge-tts>=6.1.0         # Text-to-speech
pydub>=0.25.0           # Audio processing
speechrecognition>=3.10.0  # Speech recognition
pyaudio>=0.2.11         # Audio I/O
anthropic>=0.7.0        # Claude API
openai>=1.0.0           # OpenAI API
llama-cpp-python>=0.2.0 # Local LLM support (optional)
numpy>=1.24.0           # Numerical computing
requests>=2.31.0        # HTTP requests
```

## 🚀 Quick Start

### 1. Clone or Download
```bash
# If using git
git clone https://github.com/ronniec03/Hoodbot.git
cd Hoodbot

# Or download and extract the files to your desired location
```

### 2. Install Dependencies
```bash
# Run the automated installer (Windows)
Launch_Carmen_Companion.bat

# Or install manually
pip install -r requirements.txt
```

### 3. Configure API Keys
Edit the configuration files in the `config/` directory:

**config/claude_config.json**:
```json
{
  "api_key": "YOUR_ANTHROPIC_API_KEY_HERE",
  "model": "claude-3-5-sonnet-20241022"
}
```

**config/openai_config.json**:
```json
{
  "api_key": "YOUR_OPENAI_API_KEY_HERE",
  "model": "gpt-4"
}
```

### 4. Setup Voice System
```bash
# Run voice configuration (Windows)
powershell -ExecutionPolicy Bypass -File setup_enhanced_voice.ps1
```

### 5. Test Installation
```bash
# Run system tests
python test_enhanced_system.py
```

### 6. Launch Application
```bash
# Use the launcher (recommended)
Launch_Carmen_Companion.bat

# Or run directly
python carmen_v7_fixed.py
```

## 🔧 Configuration

### Voice Settings
Edit `config/stt_config.json` for speech recognition:
```json
{
  "energy_threshold": 300,
  "pause_threshold": 1.5,
  "language": "en-US",
  "timeout": 10
}
```

Edit `config/tts_config.json` for text-to-speech:
```json
{
  "voice": "en-US-AriaNeural",
  "rate": "+0%",
  "volume": "+0%",
  "backup_voices": ["en-US-JennyNeural", "en-US-SaraNeural"]
}
```

### Local LLM Setup
1. Download a GGUF model file (e.g., Phi-3, Llama)
2. Place in `models/` directory or update the path in code
3. Recommended: Phi-3-mini-4k-instruct.Q4_0.gguf

### API Key Setup
1. **Anthropic Claude**: Get key from https://console.anthropic.com
2. **OpenAI**: Get key from https://platform.openai.com
3. Add keys to respective config files

## 💡 Usage

### Basic Chat
- Type messages in the input field and press Enter
- Use mood buttons for quick emotional context
- AI responds with personality-enhanced messages

### Voice Interaction
- Click "🎤 Talk" for voice input
- Enable "Hands-free mode" for continuous listening
- Adjust voice settings in the control panel

### Model Selection
- Choose AI models from the dropdown
- Switch between cloud and local models
- Adjust creativity (temperature) and response length

### Voice Controls
- **Voice Speed**: Control TTS playback speed
- **Volume**: Adjust TTS volume
- **Noise Threshold**: Microphone sensitivity

## 🗂️ File Structure

```
Hoodbot/
├── carmen_v7_fixed.py             # Main application
├── lust_layer.py                  # Personality engine
├── config/                        # Configuration files
│   ├── claude_config.json
│   ├── openai_config.json
│   ├── stt_config.json
│   └── tts_config.json
├── models/                        # Local LLM models (.gguf files)
├── avatar.png                     # Companion avatar image
├── enhanced_arielle.db            # SQLite database
├── Launch_Carmen_Companion.bat    # Main launcher
├── Launch_Carmen_FixAll.bat       # Dependency fixer
├── setup_enhanced_voice.ps1       # Voice system setup
├── test_enhanced_system.py        # System test suite
└── requirements.txt               # Python dependencies
```

## 🎯 Features Guide

### Personality System
The Lust Layer provides:
- **Emotional Intelligence**: Responds to user mood
- **Relationship Depth**: Tracks intimacy over time
- **Romantic Enhancement**: Adds warmth to AI responses
- **Memory Integration**: References past conversations

### Database Features
- **Conversation Logging**: All chats saved with metadata
- **Mood Tracking**: Emotional state analysis over time
- **Voice Session Tracking**: Usage statistics and quality metrics
- **User Profiling**: Preferences and communication style learning

### Advanced Voice
- **Multi-Engine Recognition**: Google + offline Sphinx
- **High-Quality TTS**: Microsoft Edge neural voices
- **Noise Handling**: Ambient noise filtering
- **Voice Activity Detection**: Smart listening activation

## 🛠️ Troubleshooting

### Common Issues

**Voice Recognition Not Working**:
- Check microphone permissions in Windows Settings
- Run `setup_enhanced_voice.ps1` as administrator
- Verify microphone is default recording device
- Test with Windows Voice Recorder

**AI Models Not Responding**:
- Verify API keys in config files
- Check internet connection for cloud models
- Ensure local model files are in correct location
- Run `test_enhanced_system.py` to diagnose

**Audio Playback Issues**:
- Install/update audio drivers
- Check default playback device
- Try different voice in TTS config
- Verify pygame installation: `pip install pygame`

**PyAudio Installation Fails**:
- Windows: Install Microsoft C++ Build Tools
- Try: `pip install pipwin && pipwin install pyaudio`
- Alternative: Download wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/

### Performance Optimization

**For Better Voice Recognition**:
- Use USB microphone for clearer audio
- Reduce background noise
- Speak clearly and at normal pace
- Adjust energy threshold in STT config

**For Faster AI Responses**:
- Use local models for offline operation
- Reduce max_tokens for shorter responses
- Close unnecessary applications
- Use SSD storage for local models

### Log Files
Check these locations for debugging:
- Console output when running `python carmen_v7_fixed.py`
- Windows Event Viewer for system-level audio issues
- Python error traces in terminal

## 🔒 Privacy & Security

### Data Storage
- All conversations stored locally in SQLite database
- No data sent to third parties except chosen AI services
- API keys stored in local configuration files
- Voice data processed locally (except Google STT)

### API Usage
- Claude: Anthropic's usage policies apply
- OpenAI: OpenAI's usage policies apply
- Local models: Completely offline and private

### Recommendations
- Keep API keys secure and private
- Regularly backup your conversation database
- Use local models for maximum privacy
- Review and clear conversation history as needed

## 🤝 Support

### Getting Help
1. Run `test_enhanced_system.py` to diagnose issues
2. Check the troubleshooting section above
3. Review console output for error messages
4. Ensure all dependencies are properly installed

### System Requirements Check
Run the test suite to verify your system:
```bash
python test_enhanced_system.py
```

This will check:
- Python dependencies
- Audio system functionality
- Database operations
- Configuration files
- AI model availability
- Voice system status

## 📝 License

This project is for personal use. Please respect the terms of service of any AI APIs you use with this application.

## 🔄 Updates

To update the Enhanced AI Companion:
1. Backup your `config/` directory and database files
2. Download the latest version
3. Restore your configuration files
4. Run `test_enhanced_system.py` to verify compatibility

---

**Enjoy your enhanced AI companion experience! 💕**
