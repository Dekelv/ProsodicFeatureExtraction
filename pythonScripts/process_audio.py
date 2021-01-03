from numpy import argmax
from scipy.signal import fftconvolve

import extract_features
import scipy
from scipy.io import wavfile

import scipy.io

extract_features.Extract("dataset/audioFiles/m4aFiles/Experiment")
extract_features.Extract("dataset/audioFiles/m4aFiles/Computer")
extract_features.Extract("dataset/audioFiles/m4aFiles/Participant")


expRate, experiment = scipy.io.wavfile.read("dataset/audioFiles/m4aFiles/Experiment.wav")
compRate, computer = scipy.io.wavfile.read("dataset/audioFiles/m4aFiles/Computer.wav")
partRate, participant = scipy.io.wavfile.read("dataset/audioFiles/m4aFiles/Participant.wav")

mode = 'valid'

print(expRate)
#print(experiment)
print(len(experiment))
print(len(experiment)/expRate/60)
print(compRate)
#print(computer)
print(len(computer))
print(len(computer)/compRate/60)
print(partRate)
#print(participant)
print(len(participant))
print(len(participant)/partRate/60)

print("COMPUTER")
print("Get Correlation")
corr = fftconvolve(computer, experiment, mode=mode)
print(len(corr))
print(max(abs(corr)))
print(argmax(abs(corr)))
print(argmax(abs(corr))/32000)
print(argmax(abs(corr))/32000/60)

print("Get Correlation")
print(max(corr))
print(argmax(corr))
print(argmax(corr)/32000)
print(argmax(corr)/32000/60)

print("Get Correlation")
corr2 = fftconvolve(experiment, computer, mode=mode)
print(max(abs(corr2)))
print(argmax(abs(corr2)))
print(argmax(abs(corr2))/32000)
print(argmax(abs(corr2))/32000/60)

print("Get Correlation")
print(max(corr2))
print(argmax(corr2))
print(argmax(corr2)/32000)
print(argmax(corr2)/32000/60)


print("PARTICIPANT")
print("Get Correlation")
corr = fftconvolve(participant, experiment, mode=mode)
print(len(corr))
print(max(abs(corr)))
print(argmax(abs(corr)))
print(argmax(abs(corr))/32000)
print(argmax(abs(corr))/32000/60)

print("Get Correlation")
print(max(corr))
print(argmax(corr))
print(argmax(corr)/32000)
print(argmax(corr)/32000/60)

print("Get Correlation")
corr2 = fftconvolve(experiment, participant, mode=mode)
print(max(abs(corr2)))
print(argmax(abs(corr2)))
print(argmax(abs(corr2))/32000)
print(argmax(abs(corr2))/32000/60)

print("Get Correlation")
print(max(corr2))
print(argmax(corr2))
print(argmax(corr2)/32000)
print(argmax(corr2)/32000/60)