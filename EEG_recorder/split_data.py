# -*- coding: utf-8 -*-
"""
Created on Tue May  4 19:42:23 2021

@author: myriam
"""
import numpy as np
from scipy.io.wavfile import write

# Duracion de cada palabra en segundos (no cuenta silencio)
d_words=2  
# Frecuencia de muestreo
fs=44100
# Tiempo (segundos) de silencio tras cada palabra
d_silen=0.5
# Numero de palabras tratadas
n_words=25
# Duracion en muestras de cada palabra + silencio
d_tramas=int((d_words+d_silen)*fs)

#len_frame=np.floor(solapamiento*fs);  
#n_tramas=int(np.floor((audio.shape[0]-windowLength*sr)/(frameshift*sr))

# Cargar los datos .xdf
exec(open('load_data.py').read())

audio=np.load('pablo_1.npy')

w=np.zeros((d_tramas,n_words)).astype(np.int16)

# Variable auxiliar utilizada como contador
ind=0

# Bucle de segmentación. Reshape de la señal de audio (vector fila) en una matriz de tamaño [d_tramas x n_words].
# En cada iteración genera un archivo .wav correspondiente a cada palabra
for i in range(0, n_words):
    w[:,i]=audio[ind:ind+d_tramas]
    ind += d_tramas
    
    write('pablo_words' +str(i)+'.wav',fs, w[:,i])


#write('A.wav', fs, audio[d_tramas:d_tramas+d_tramas])