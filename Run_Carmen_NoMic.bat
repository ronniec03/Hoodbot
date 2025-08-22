@echo off
title Carmen - No Microphone Mode
cd /d %~dp0

:: Activate venv
call venv\Scripts\activate.bat

:: Install core deps (no PyAudio)
python -m pip install --upgrade pip
pip install pygame pyttsx3 pillow opencv-python gpt4all edge-tts gtts

:: Optional: CPU torch if not installed yet (non-fatal if already installed)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

:: Run with microphone shim
python run_nomicrophone.py

pause
