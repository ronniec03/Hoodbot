@echo off
title Carmen - GPU (llama.cpp CUDA)
cd /d %~dp0

:: Set PATH so Windows can find your freshly built CUDA DLLs
set PATH=%PATH%;C:\Users\Justin\llama.cpp\build\bin\Release

:: Expose GPU 0 to llama backend
set CUDA_VISIBLE_DEVICES=0

:: Activate venv
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat

:: Ensure gpt4all present
python -m pip install --upgrade pip
pip install gpt4all

:: Run your companion
python carmen_v7_fixed.py

pause
