import queue
import sounddevice as sd
import vosk
import json
import os

MODEL_PATH = r"C:\Users\Justin\Documents\CompanionAI\vosk-model-small-en-us-0.15"

class SpeechRecognizer:
    def __init__(self):
        if not os.path.isdir(MODEL_PATH):
            print("Vosk model not found at", MODEL_PATH)
            self.model = None
            return
        self.model = vosk.Model(MODEL_PATH)
        self.q = queue.Queue()
        self.stream = sd.InputStream(samplerate=16000, channels=1, callback=self.callback)
        self.stream.start()
        self.rec = vosk.KaldiRecognizer(self.model, 16000)

    def callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.q.put(bytes(indata))

    def listen(self):
        if not self.model:
            return None
        while not self.q.empty():
            data = self.q.get()
            if self.rec.AcceptWaveform(data):
                result = json.loads(self.rec.Result())
                return result.get("text", "")
        return None
