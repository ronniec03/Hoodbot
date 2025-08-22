@echo off
:: Set working directory
cd /d %~dp0

:: Step 1: Create venv
if not exist venv (
    echo [*] Creating virtual environment...
    python -m venv venv
)

:: Step 2: Activate venv
call venv\Scripts\activate

:: Step 3: Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip

:: Step 4: Install dependencies
echo [*] Installing required packages...
pip install torch==2.2.2+cpu torchvision==0.17.2+cpu torchaudio==2.2.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
pip install pygame pyttsx3 pillow opencv-python gpt4all speechrecognition edge-tts gtts

:: Step 5: Launch interface
echo [*] Launching Carmen Companion...
python carmen_v7_fixed.py

pause
