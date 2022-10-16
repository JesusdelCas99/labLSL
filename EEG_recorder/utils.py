import numpy as np

# Genera un tono a una frecuencia de muestreo de 44100Hz
def generate_beep(duration, freq=2000, fs=44100):
    t = np.linspace(0, duration, int(fs * duration))
    y = 10 * np.cos(2 * np.pi * freq * t)
    return y
