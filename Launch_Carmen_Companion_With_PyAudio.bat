@echo off
:: Set working directory
cd /d %~dp0

:: Step 1: Create virtual environment if it doesn't exist
if not exist venv (
    echo [*] Creating virtual environment...
    python -m venv venv
)

:: Step 2: Activate venv
call venv\Scripts\activate

:: Step 3: Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip

:: Step 4: Install core packages
echo [*] Installing core dependencies...
pip install pygame pyttsx3 pillow opencv-python gpt4all edge-tts gtts speechrecognition

:: Step 5: Install torch (CPU-only for now)
pip install torch==2.2.2+cpu torchvision==0.17.2+cpu torchaudio==2.2.2+cpu -f https://download.pytorch.org/whl/torch_stable.html

:: Step 6: Download and install PyAudio .whl for Python 3.13 on Win64
echo [*] Installing PyAudio...
curl -L -o pyaudio.whl "https://download.lfd.uci.edu/pythonlibs/archive/cp313/PyAudio‑0.2.11‑cp313‑cp313‑win_amd64.whl"
pip install pyaudio.whl
del pyaudio.whl

:: Step 7: Launch app
echo [*] Launching Carmen Companion...
python carmen_v7_fixed.py

pause
