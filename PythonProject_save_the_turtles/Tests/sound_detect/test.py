import pyaudio
import numpy as np

# Configuration de l'audio
chunk_size = 1024
sample_rate = 44100  # FrÃ©quence d'Ã©chantillonnage audio (en Hz)

# Seuil pour la dÃ©tection des applaudissements
seuil_applaudissements = 60  # Vous pouvez ajuster ce seuil en fonction de la sensibilitÃ© souhaitÃ©e

# Initialisation de PyAudio
p = pyaudio.PyAudio()

# Ouvrir un flux audio en entrÃ©e (microphone)
stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=sample_rate,
                input=True,
                frames_per_buffer=chunk_size)

while True:
    try:
        # Lire les donnÃ©es audio du flux
        audio_data = np.frombuffer(stream.read(chunk_size), dtype=np.int16)

        # Calculer le niveau sonore (dB) uniquement si rms n'est pas nul
        rms = np.sqrt(np.mean(np.square(audio_data)))
        if rms > 0:
            db = 20 * np.log10(rms)
            print(f"Niveau sonore : {db:.2f} dB")
            
            # Si le niveau sonore dÃ©passe le seuil des applaudissements, dÃ©clencher un Ã©vÃ©nement
            if db > seuil_applaudissements:
                print("Applaudissements dÃ©tectÃ©s ! DÃ©clenchement de l'Ã©vÃ©nement...")
                # Ajoutez ici le code pour dÃ©clencher l'Ã©vÃ©nement souhaitÃ©

    except KeyboardInterrupt:
        break

# Fermer le flux audio
stream.stop_stream()
stream.close()
p.terminate()