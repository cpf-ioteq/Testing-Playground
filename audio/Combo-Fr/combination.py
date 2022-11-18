#!/usr/bin/env python3

import sys
import csv
import time
import threading

import numpy as np
import sounddevice as sd

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

        # Play the waveform 
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

class baseline_feed():
    def sample_feed(self, f, k, m):
        samplerate = 44100

        def callback(outdata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            global start_idx
            t = (start_idx + np.arange(frames)) / samplerate
            t = t.reshape(-1, 1)
            if m != 250.0 or k != 25.0:
                outdata[:] = np.cos((1 * np.sin(2 * np.pi * f * t))+(k * np.sin(2 * np.pi * m * t)))
            else:
                outdata[:] = 1 * np.sin(2 * np.pi * f * t)

            start_idx += frames

        with sd.OutputStream(callback=callback, samplerate=samplerate):
            print(x)
    



class main(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # setup csv feed
        csv_feeder = csv_feed()
        csv_feeder.open_csv('amplitude_mod.csv')

        # setup baseline feed
        baseline_feeder = baseline_feed()
        baseline_feeder.sample_feed(200, 40, 25)
        baseline_feeder.sample_feed(25, 2, 15)

# run script 
main()