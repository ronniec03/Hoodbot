@echo off
echo [*] Launching Enhanced AI Companion - Arielle
echo.

:: Set working directory
cd /d %~dp0

:: Activate virtual environment
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo [WARNING] Virtual environment not found. Run install_enhanced_deps.bat first.
    echo [*] Continuing with system Python...
)

:: Launch the enhanced companion
echo [*] Starting Enhanced AI Companion...
python carmen_v7_fixed.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start the companion. Check the error messages above.
    echo [*] Try running install_enhanced_deps.bat to fix dependencies.
)

pause