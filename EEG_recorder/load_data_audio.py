# -*- coding: utf-8 -*-
"""
Created on Thu May  6 12:20:43 2021

@author: myriam
"""

import pyxdf
import bisect
import numpy as np
import scipy.signal
from scipy.signal import decimate
from scipy.io.wavfile import write
import librosa    


def locate_pos(available_freqs, target_freq):
    pos = bisect.bisect_right(available_freqs, target_freq)
    if pos == 0:
        return 0
    if pos == len(available_freqs):
        return len(available_freqs)-1
    if abs(available_freqs[pos]-target_freq) < abs(available_freqs[pos-1]-target_freq):
        return pos
    else:
        return pos-1  

#    pts = ['kh13']
#    path = r'./'
#    outPath = r'./'
path='/home/dell/Escritorio/eeg-recorder/kh13'
streams = pyxdf.load_xdf(path + '/prueba' + '.xdf',dejitter_timestamps=True)

   #streams = pyxdf.load_xdf(path + p + '/speech' + str(ses) + '.xdf',dejitter_timestamps=False)

streamToPosMapping = {}
for pos in range(0,len(streams[0])):
    stream = streams[0][pos]['info']['name']
    streamToPosMapping[stream[0]] = pos


#Load Audio
audio = streams[0][streamToPosMapping['MyAudioStream']]['time_series']
offset_audio = float(streams[0][streamToPosMapping['MyAudioStream']]['info']['created_at'][0])
audio_ts = streams[0][streamToPosMapping['MyAudioStream']]['time_stamps'].astype('float')#+offset
audio_sr = int(float(streams[0][streamToPosMapping['MyAudioStream']]['info']['nominal_srate'][0]))

# Load Marker stream
markers = streams[0][streamToPosMapping['SingleWordsMarkerStream']]['time_series']
offset_marker = float(streams[0][streamToPosMapping['SingleWordsMarkerStream']]['info']['created_at'][0])
marker_ts = streams[0][streamToPosMapping['SingleWordsMarkerStream']]['time_stamps'].astype('float')#-offset

# Get words
wordMask = [m[0].split(';')[0]=='start' for m in markers]
wordStarts = marker_ts[wordMask]
dispWords =  [m[0].split(';')[1] for m in markers if m[0].split(';')[0]=='start']
wordEndMask = [m[0].split(';')[0]=='end' for m in markers]
wordEnds = marker_ts[wordEndMask]

   
# Saving
#
outPath = "pablo_1"
np.save(outPath + '_'  +'_audio.npy',audio[:,0])

#np.save(outPath  + p + '_' + str(ses) +'_audio.npy',a[0:240312]+noise)
#a=audio[:,0]
write("audio.wav",44100, audio)
# Downsample a 8KHz
#audionew, fs = librosa.load('audio.wav', sr=8000, mono=False)
#audionew=audionew.transpose()
#write("audio_8k.wav", 8000, A)
#A=librosa.resample(audio[:,0], orig_sr=48000, target_sr=8000)
