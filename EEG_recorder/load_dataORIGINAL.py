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

if __name__=="__main__":
    pts = ['kh13']
    sessions = [1,]
    path = r'./'
    outPath = r'./'
    for pNr, p in enumerate(pts):
        for ses in range(1,sessions[pNr]+1):
    
            streams = pyxdf.load_xdf(path + p + '/speech' + str(ses) + '.xdf',dejitter_timestamps=False)
            streamToPosMapping = {}
            for pos in range(0,len(streams[0])):
                stream = streams[0][pos]['info']['name']
                streamToPosMapping[stream[0]] = pos

            # Get sEEG
            eeg = streams[0][streamToPosMapping['Micromed']]['time_series']
            offset = float(streams[0][streamToPosMapping['Micromed']]['info']['created_at'][0])
            eeg_ts = streams[0][streamToPosMapping['Micromed']]['time_stamps'].astype('float')#+offset
            eeg_sr = int(streams[0][streamToPosMapping['Micromed']]['info']['nominal_srate'][0])
            if eeg_sr == 2048:
                eeg = decimate(eeg,2,axis=0)
                eeg_ts = eeg_ts[::2]
            #Get channel info
            chNames = []
            for ch in streams[0][streamToPosMapping['Micromed']]['info']['desc'][0]['channels'][0]['channel']:
                chNames.append(ch['label'])

            #Load Audio
            audio = streams[0][streamToPosMapping['AudioCaptureWin']]['time_series']
            offset_audio = float(streams[0][streamToPosMapping['AudioCaptureWin']]['info']['created_at'][0])
            audio_ts = streams[0][streamToPosMapping['AudioCaptureWin']]['time_stamps'].astype('float')#+offset
            audio_sr = int(streams[0][streamToPosMapping['AudioCaptureWin']]['info']['nominal_srate'][0]) 
            
            # Load Marker stream
            markers = streams[0][streamToPosMapping['SingleWordsMarkerStream']]['time_series']
            offset_marker = float(streams[0][streamToPosMapping['SingleWordsMarkerStream']]['info']['created_at'][0])
            marker_ts = streams[0][streamToPosMapping['SingleWordsMarkerStream']]['time_stamps'].astype('float')#-offset

            #Get Experiment time
            i=0
            while markers[i][0]!='experimentStarted':
                i+=1
            eeg_start= locate_pos(eeg_ts, marker_ts[i])
            audio_start = locate_pos(audio_ts, eeg_ts[eeg_start])
            while markers[i][0]!='experimentEnded':
                i+=1
            eeg_end= locate_pos(eeg_ts, marker_ts[i])
            audio_end = locate_pos(audio_ts, eeg_ts[eeg_end])
            markers=markers[:i]
            marker_ts=marker_ts[:i]

            eeg = eeg[eeg_start:eeg_end,:]
            eeg_ts = eeg_ts[eeg_start:eeg_end]
            audio = audio[audio_start:audio_end,:]
            audio_ts=audio_ts[audio_start:audio_end]

            # Get words
            words=['' for a in range(eeg.shape[0])]
            wordMask = [m[0].split(';')[0]=='start' for m in markers]
            wordStarts = marker_ts[wordMask]
            wordStarts = np.array([locate_pos(eeg_ts, x) for x in wordStarts])
            dispWords =  [m[0].split(';')[1] for m in markers if m[0].split(';')[0]=='start']
            wordEndMask = [m[0].split(';')[0]=='end' for m in markers]
            wordEnds = marker_ts[wordEndMask]
            wordEnds = np.array([locate_pos(eeg_ts, x) for x in wordEnds])

            for i, start in enumerate(wordStarts):
                words[start:wordEnds[i]]=[dispWords[i] for rep in range(wordEnds[i]-start)]
            print('All aligned')
            # Saving
            #Adding some white noise because the microphone thresholds the data
           
            noise = np.random.normal(0,0.0001, audio.shape[0])
            np.save(outPath  + p + '_' + str(ses) + '_sEEG.npy', eeg)
            np.save(outPath  + p + '_' + str(ses) +'_words.npy', np.array(words))
            np.save(outPath  + p + '_' + str(ses) +'_channelNames.npy', np.array(chNames))
            #
            np.save(outPath  + p + '_' + str(ses) +'_audio.npy',audio[:,0]+noise)
            
            #np.save(outPath  + p + '_' + str(ses) +'_audio.npy',a[0:240312]+noise)
            #a=audio[:,0]
            write("audio.wav", 48000, audio)
            # Downsample a 8KHz
            #audionew, fs = librosa.load('audio.wav', sr=8000, mono=False)
            #audionew=audionew.transpose()
            #write("audio_8k.wav", 8000, A)
            A=librosa.resample(audio[:,0], orig_sr=48000, target_sr=8000)
