import pyaudio
import numpy as np
import matplotlib.pyplot as plt

# Paramètres de l'enregistrement
CHUNK = 1024 # Nombre de points à lire à chaque fois
FORMAT = pyaudio.paInt16 # Format des données audio
CHANNELS = 1 # Nombre de canaux (mono)
RATE = 44100 # Fréquence d'échantillonnage

# Initialisation de PyAudio
p = pyaudio.PyAudio()

# Ouverture du flux audio
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Initialisation du graphique
fig, ax = plt.subplots()
x = np.arange(0, 2 * CHUNK, 2)
line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)

# Réglages du graphique
ax.set_ylim(0, 255)
ax.set_xlim(0, 2 * CHUNK)
plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])

# Affichage du graphique
plt.show(block=False)

# Calibration du bruit ambiant
print("Calibration du bruit ambiant en cours...")
noise = []
for i in range(10):
    data = stream.read(CHUNK)
    data = np.frombuffer(data, dtype=np.int16)
    noise.append(data)
noise = np.concatenate(noise)
noise = np.mean(np.abs(noise))
print(f"Calibration terminée. Niveau de bruit ambiant : {noise:.2f}")

# Boucle d'enregistrement
while True:
    # Lecture des données audio
    data = stream.read(CHUNK)
    # Conversion des données en tableau numpy
    data = np.frombuffer(data, dtype=np.int16)
    # Calibration du bruit ambiant
    rms = np.sqrt(np.mean(np.square(data)))
    db = 20 * np.log10(rms / noise)
    # Mise à jour du graphique
    line.set_ydata(data)
    fig.canvas.draw()
    fig.canvas.flush_events()
    # Affichage du niveau de décibels
    print(f"Décibels : {db:.2f} dB")

# Fermeture du flux audio
stream.stop_stream()
stream.close()
p.terminate()
