import asyncio
import edge_tts
import tempfile
import os
import playsound

class VoiceSynth:
    def __init__(self, voice="en-US-JennyNeural"):
        self.voice = voice

    def speak(self, text):
        if not text:
            return
        asyncio.run(self._speak_async(text))

    async def _speak_async(self, text):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            path = f.name
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(path)
        playsound.playsound(path)
        os.remove(path)
