# !/usr/bin/env python3

import time
import csv

import numpy as np
import sounddevice as sd

def frequency_Controller(chz, fmhz, kp, amp):
    # carrier_hz: Frequency of the carrier. BASE - 440.0
    # fm_hz: Frequency of the frequency modulator. BASE - 220.0
    # k_p: deviation constant. BASE - 25.0

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


filename = 'wavelength_parser.csv'
rows = []

with open(filename, 'r') as csvfile:
    data_reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    for row in data_reader:
        rows = row
        arg1, arg2, arg3, arg4 = rows
        # print(arg1, arg2, arg3)
        frequency_Controller(arg1, arg2, arg3, arg4)
