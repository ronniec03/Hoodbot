@echo off
echo [*] Enhanced AI Companion Dependency Installer
echo.

:: Set working directory
cd /d %~dp0

:: Step 1: Create venv if it doesn't exist
if not exist venv (
    echo [*] Creating virtual environment...
    python -m venv venv
)

:: Step 2: Activate venv
echo [*] Activating virtual environment...
call venv\Scripts\activate

:: Step 3: Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip

:: Step 4: Install enhanced dependencies
echo [*] Installing enhanced dependencies...
pip install -r requirements_enhanced.txt

:: Step 5: Install PyAudio separately (often problematic)
echo [*] Installing PyAudio...
pip install pipwin
pipwin install pyaudio

echo.
echo [*] Installation complete! You can now run:
echo     Launch_Carmen_Companion.bat
echo.
pause