
# carmen_safevideo_micfix.py
# 1) Force CPU (silence CUDA DLL probes)
# 2) Patch speech_recognition.Microphone to sounddevice (no PyAudio)
# 3) Patch cv2.VideoCapture to an async preloader to prevent UI stalls or gray screens
# 4) Launch your original app: carmen_v7_fixed.py

import os
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")  # hide GPUs by default

import sys, queue, runpy, threading, time

# ---- Mic patch (sounddevice) ----
try:
    import sounddevice as sd
    import numpy as np
    import speech_recognition as sr
    from speech_recognition import AudioSource
    class _SDByteStream:
        def __init__(self, q):
            self._q, self._buf = q, bytearray()
        def read(self, n):
            while len(self._buf) < n:
                chunk = self._q.get()
                if chunk is None: break
                self._buf.extend(chunk)
            out = bytes(self._buf[:n]); del self._buf[:n]; return out
    class SDMicrophone(AudioSource):
        def __init__(self, device_index=None, samplerate=16000, channels=1, blocksize=1024, dtype="int16"):
            self.device_index = device_index; self.SAMPLE_RATE=int(samplerate); self.SAMPLE_WIDTH=2; self.CHUNK=int(blocksize)
            self._q = queue.Queue(maxsize=64); self.stream = _SDByteStream(self._q); self._sd_stream=None
        def __enter__(self):
            def cb(indata, frames, t, status):
                arr = indata.reshape(-1).astype("int16", copy=False).tobytes()
                try: self._q.put_nowait(arr)
                except queue.Full:
                    try: _ = self._q.get_nowait()
                    except queue.Empty: pass
                    self._q.put_nowait(arr)
            if self.device_index is None:
                try: self.device_index = sd.default.device[0]
                except Exception: self.device_index = None
            self._sd_stream = sd.InputStream(samplerate=self.SAMPLE_RATE, blocksize=self.CHUNK, device=self.device_index,
                                             channels=1, dtype="int16", callback=cb)
            self._sd_stream.start(); return self
        def __exit__(self, *a):
            try:
                if self._sd_stream: self._sd_stream.stop(); self._sd_stream.close()
                self._q.put_nowait(None)
            except: pass
            return False
    sr.Microphone = SDMicrophone
    if not hasattr(sr.Recognizer, "adjust_for_ambient_noise"):
        sr.Recognizer.adjust_for_ambient_noise = lambda self, source, duration=1: None
    print("[SafeBoot] Mic: sounddevice InputStream active (no PyAudio).")
except Exception as e:
    print(f"[SafeBoot] Mic patch skipped: {e}")

# ---- Video patch (async prefetch) ----
try:
    import cv2
    import numpy as np
    class AsyncVideoCapture:
        def __init__(self, path):
            self._cap = cv2.VideoCapture(path)
            self._q = queue.Queue(maxsize=2)
            self._stop = False
            self._opened = self._cap.isOpened()
            def reader():
                while not self._stop:
                    if not self._opened:
                        # dummy black frame 720p @ ~30 fps
                        frame = np.zeros((720,1280,3), dtype=np.uint8)
                        try: self._q.put_nowait(frame)
                        except queue.Full:
                            try: _ = self._q.get_nowait()
                            except queue.Empty: pass
                            self._q.put_nowait(frame)
                        time.sleep(1/30.0)
                        continue
                    ok, frame = self._cap.read()
                    if not ok:
                        self._cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue
                    try: self._q.put_nowait(frame)
                    except queue.Full:
                        try: _ = self._q.get_nowait()
                        except queue.Empty: pass
                        self._q.put_nowait(frame)
            threading.Thread(target=reader, daemon=True).start()
        def isOpened(self): return True  # always present a source
        def read(self):
            frame = self._q.get()
            return True, frame
        def release(self):
            self._stop = True
            try: self._cap.release()
            except Exception: pass
    # Monkey-patch
    _orig_VC = cv2.VideoCapture
    def _patched_VC(path, *a, **k): return AsyncVideoCapture(path)
    cv2.VideoCapture = _patched_VC
    print("[SafeBoot] Video: async preloader enabled. Gray-screen stutters suppressed.")
except Exception as e:
    print(f"[SafeBoot] Video patch skipped: {e}")

# ---- Launch original app ----
runpy.run_path("carmen_v7_fixed.py", run_name="__main__")
