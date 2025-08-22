
@echo off
title Carmen - Live Mic (sounddevice) Launcher
cd /d %~dp0

:: Activate venv
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat

:: Deps for mic fix
python -m pip install --upgrade pip
pip install sounddevice numpy SpeechRecognition pygame pyttsx3 pillow opencv-python gpt4all edge-tts gtts

:: Optional: CPU torch if needed (non-fatal if fails)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

:: Run mic-fixed wrapper (keeps your original file intact)
python carmen_v7_micfix.py

pause
