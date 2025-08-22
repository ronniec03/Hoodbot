@echo off
title Carmen Launcher - Auto Fix Mode
cd /d %~dp0

echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo [*] Installing compatible CPU Torch...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

echo [*] Downloading PyAudio wheel (x64)...
curl -L -o PyAudio-0.2.11-cp311-cp311-win_amd64.whl https://download.lfd.uci.edu/pythonlibs/n4et3xkz/PyAudio-0.2.11-cp311-cp311-win_amd64.whl

echo [*] Installing PyAudio wheel...
pip install PyAudio-0.2.11-cp311-cp311-win_amd64.whl

echo [*] Launching Carmen...
python carmen_v7_fixed.py

pause