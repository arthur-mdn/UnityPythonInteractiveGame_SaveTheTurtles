import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Paramètres pour l'audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Fonction pour calculer la valeur RMS
def rms(frame):
    rms_val = np.sqrt(np.mean(np.square(np.frombuffer(frame, dtype=np.int16))))
    return 20 * np.log10(rms_val) if rms_val > 0 else -100.0

# Initialisation de PyAudio
p = pyaudio.PyAudio()

# Ouverture du flux audio
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Configuration de la figure pour matplotlib
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r-', animated=True)
plt.title('Niveau sonore en dB')
ax.set_ylim(-90, 0)
ax.set_xlim(0, 10)
ax.set_xlabel('Temps (s)')
ax.set_ylabel('Niveau sonore (dB)')

# Initialisation de la visualisation
def init():
    ax.set_ylim(-60, 0)
    ax.set_xlim(0, 10)
    del xdata[:]
    del ydata[:]
    return ln,

# Fonction d'animation appelée à chaque intervalle
def update(frame):
    data = stream.read(CHUNK)
    level = rms(data)
    xdata.append(frame / (RATE / CHUNK))
    ydata.append(level)
    if len(xdata) > 10 * (RATE / CHUNK):
        ax.set_xlim(xdata[-1]-10, xdata[-1])
    ln.set_data(xdata, ydata)
    return ln,

# Animation
ani = FuncAnimation(fig, update, frames=np.arange(0, int(RATE / CHUNK * 200)), init_func=init, blit=True, interval=1000/(RATE / CHUNK), repeat=False)

# Afficher le graphique
plt.show()

# Fermeture du flux audio et terminaison de PyAudio
stream.stop_stream()
stream.close()
p.terminate()
