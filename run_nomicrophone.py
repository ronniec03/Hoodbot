import sys, types, runpy

# ---- Shim a minimal 'speech_recognition' module to avoid PyAudio requirement ----
sr = types.ModuleType("speech_recognition")

class Recognizer:
    def __init__(self): pass
    def listen(self, *a, **k): return None
    def recognize_google(self, *a, **k): return ""

class Microphone:
    def __init__(self, *a, **k):
        print("[NoMic] Microphone disabled (PyAudio not installed).")
    def __enter__(self): return None
    def __exit__(self, exc_type, exc, tb): return False

sr.Recognizer = Recognizer
sr.Microphone = Microphone
sys.modules["speech_recognition"] = sr

# ---- Run the companion app without touching the original file ----
runpy.run_path("carmen_v7_fixed.py", run_name="__main__")