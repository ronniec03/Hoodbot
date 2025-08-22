
# carmen_v7_micfix.py (rev2)
# Patch speech_recognition to use sounddevice.InputStream (NumPy array callback),
# avoid PyAudio, and launch your existing carmen_v7_fixed.py.

import sys, queue, runpy

# --- Require deps ---
try:
    import numpy as np
    import sounddevice as sd
except Exception as e:
    print("[MicFix] Missing deps. In venv run: pip install sounddevice numpy")
    raise

# --- Patch speech_recognition ---
try:
    import speech_recognition as sr
    from speech_recognition import AudioSource
except Exception as e:
    print("[MicFix] SpeechRecognition not installed. In venv: pip install SpeechRecognition")
    raise

# Ensure Recognizer has adjust_for_ambient_noise (noop if missing)
if not hasattr(sr.Recognizer, "adjust_for_ambient_noise"):
    def _noop_adjust(self, source, duration=1):
        print(f"[MicFix] adjust_for_ambient_noise noop (duration={duration})")
    sr.Recognizer.adjust_for_ambient_noise = _noop_adjust
    print("[MicFix] Injected noop Recognizer.adjust_for_ambient_noise")

class _SDByteStream:
    """Minimal stream exposing .read(n) for SpeechRecognition's consumers."""
    def __init__(self, q: queue.Queue):
        self._q = q
        self._buf = bytearray()

    def read(self, n: int) -> bytes:
        while len(self._buf) < n:
            chunk = self._q.get()
            if chunk is None:
                break
            self._buf.extend(chunk)
        out = bytes(self._buf[:n])
        del self._buf[:n]
        return out

class SDMicrophone(AudioSource):
    def __init__(self, device_index=None, samplerate=16000, channels=1, blocksize=1024, dtype="int16"):
        assert channels == 1, "[MicFix] Only mono audio supported"
        self.device_index = device_index
        self.SAMPLE_RATE = int(samplerate)
        self.SAMPLE_WIDTH = 2  # int16 PCM
        self.CHUNK = int(blocksize)
        # Use InputStream so callback receives NumPy arrays
        self.dtype = "int16"

        self._q = queue.Queue(maxsize=64)
        self.stream = _SDByteStream(self._q)
        self._sd_stream = None

    def __enter__(self):
        def callback(indata, frames, time_info, status):
            # indata is a NumPy ndarray (frames, 1) dtype=int16
            if status:
                # print("[MicFix] sd status:", status)
                pass
            # ensure contiguous bytes
            data = indata.reshape(-1).tobytes()
            try:
                self._q.put_nowait(data)
            except queue.Full:
                try:
                    _ = self._q.get_nowait()
                except queue.Empty:
                    pass
                self._q.put_nowait(data)

        # Auto-pick default input device if None
        if self.device_index is None:
            try:
                default_in = sd.default.device[0]
                self.device_index = default_in
            except Exception:
                self.device_index = None

        self._sd_stream = sd.InputStream(
            samplerate=self.SAMPLE_RATE,
            blocksize=self.CHUNK,
            device=self.device_index,
            channels=1,
            dtype=self.dtype,
            callback=callback,
        )
        self._sd_stream.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if self._sd_stream:
                self._sd_stream.stop()
                self._sd_stream.close()
        finally:
            try:
                self._q.put_nowait(None)
            except:
                pass
        return False

# Monkey-patch Microphone
sr.Microphone = SDMicrophone
print("[MicFix] Using sounddevice InputStream (int16). PyAudio not required.")

# Optional: list input devices once
try:
    devices = sd.query_devices()
    print("[MicFix] Available input devices:")
    for i, d in enumerate(devices):
        if d.get("max_input_channels", 0) > 0:
            star = ""
            try:
                if i == sd.default.device[0]:
                    star = "*"
            except Exception:
                pass
            print(f"  #{i}: {d.get('name')} (in={d.get('max_input_channels')}) {star}")
except Exception:
    pass

# --- Launch original app ---
runpy.run_path("carmen_v7_fixed.py", run_name="__main__")
