#!/usr/bin/env python3

import csv
import time

import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io.wavfile import write, read


class csv_feed:
    def frequency_Controller(self, chz, fmhz, kp, amp):
        # carrier_hz: Frequency of the carrier.
        # fm_hz: Frequency of the frequency modulator.
        # k_p: deviation constant.
        sample_rate = 44100
        carrier_hz = chz
        fm_hz = fmhz
        k = kp
        a = amp

        # First, define our range of sample numbers
        each_sample_number = np.arange(sample_rate)

        # Create the carrier
        carrier = 2 * np.pi * each_sample_number * carrier_hz / sample_rate

        # Frequency modulator
        modulator = k * np.sin(2 * np.pi * each_sample_number * fm_hz / sample_rate)

        # Modulated waveform, and attenuate it
        waveform = np.cos(carrier + modulator)
        waveform_quiet = waveform * a

        # Play the waveform & write the wav file for visualization
        waveform_integers = np.int16(waveform_quiet * 32767)
        write('testing.wav', sample_rate, waveform_integers)
        sd.play(waveform_quiet, sample_rate)
        time.sleep(1)
        sd.stop()
    
    def open_csv(self, filename):
        fn = filename
        rows = []

        # read through and parse data from csv
        with open(fn, 'r') as csvfile:
            data_reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            for row in data_reader:
                rows = row
                arg1, arg2, arg3, arg4 = rows
                # print(arg1, arg2, arg3)
                self.frequency_Controller(arg1, arg2, arg3, arg4)

class visualizer:
    def visualize(self, wave_file):
        # read audio samples
        input_data = read(wave_file)
        audio = input_data[1]

        # plot the first 1024 samples
        plt.plot(audio[0:1024])
        # label the axes
        plt.ylabel("Amplitude")
        plt.xlabel("Time")
        # set the title  
        plt.title("Visualized Waveform")
        # display the plot
        plt.show()



class main():
    def __init__(self):
        # setup csv feed
        csv_feeder = csv_feed()
        csv_feeder.open_csv('amplitude_mod.csv')

        # setup visualizer
        visual = visualizer()
        visual.visualize('testing.wav')


# run script 
main()