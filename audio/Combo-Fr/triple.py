#!/usr/bin/env python3

import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.io.wavfile import read

def step1(wave_file):
    data, fs = sf.read(wave_file)
    sd.play(data, fs)
    sd.wait()

    # audio = data[1]
    # # plot the first 1024 samples
    # plt.plot(audio[0:1024])
    # # label the axes
    # plt.ylabel("Amplitude")
    # plt.xlabel("Time")
    # # set the title  
    # plt.title("Visualized Waveform")
    # # display the plot
    # plt.show()

step1('three.wav')