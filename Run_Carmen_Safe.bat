@echo off
title Carmen - Safe Boot (CPU + Live Mic + Async Video)
cd /d %~dp0

:: Hide GPUs to silence CUDA DLL probes
set CUDA_VISIBLE_DEVICES=

:: Ensure venv
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat

:: Deps required for safe boot
python -m pip install --upgrade pip
pip install sounddevice numpy SpeechRecognition opencv-python pygame pyttsx3 pillow gpt4all edge-tts gtts

:: Run safe wrapper
python carmen_safevideo_micfix.py

pause
