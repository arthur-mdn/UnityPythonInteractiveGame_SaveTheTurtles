import numpy as np
import sounddevice as sd

def audio_callback(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    print(str(int(volume_norm)) + "|" * int(volume_norm))

stream = sd.InputStream(callback=audio_callback)
with stream:
    while True:
        pass
