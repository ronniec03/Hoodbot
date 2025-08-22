@echo off
title Carmen - CPU Only (silence CUDA DLL probes)
cd /d %~dp0

:: Hide all GPUs from subprocesses
set CUDA_VISIBLE_DEVICES=

:: Optionally add llama build path if you want, but not needed for CPU
:: set PATH=%PATH%;C:\Users\Justin\llama.cpp\build\bin\Release

:: Activate venv
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat

python -m pip install --upgrade pip
pip install gpt4all

python carmen_v7_fixed.py

pause
