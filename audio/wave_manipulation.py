import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import time

def frequency_Controller(dur, chz, fmhz, kp):
    # duration_s: Duration. BASE - 5.0
    # carrier_hz: Frequency of the carrier. BASE - 440.0
    # fm_hz: Frequency of the frequency modulator. BASE - 220.0
    # k_p: deviation constant. BASE - 25.0

    sample_rate = 44100
    duration_s = dur
    carrier_hz = chz
    fm_hz = fmhz
    k = kp

    # First, define our range of sample numbers
    each_sample_number = np.arange(duration_s * sample_rate)

    # Create the carrier
    carrier = 2 * np.pi * each_sample_number * carrier_hz / sample_rate

    # Frequency modulator
    modulator = k * np.sin(2 * np.pi * each_sample_number * fm_hz / sample_rate)

    # Modulated waveform, and attenuate it
    waveform = np.cos(carrier + modulator)
    waveform_quiet = waveform * 0.3

    # Adjust amplitude of waveform and write the .wav file.
    waveform_integers = np.int16(waveform_quiet * 32767)
    write('fm-out.wav', sample_rate, waveform_integers)

    # Play the waveform 
    sd.play(waveform_quiet, sample_rate)
    time.sleep(duration_s)
    sd.stop()

#Running the controller with inputted values
def get_input():
    arg1 = float(input("Duration of Sample (5.0): "))
    arg2 = float(input("Frequency of Carrier (440.0): "))
    arg3 = float(input("Frequency of Modulator (220.0): "))
    arg4 = float(input("Deviation Constant (25.0): "))

    frequency_Controller(arg1, arg2, arg3, arg4)

yes = ['yes', 'y', '']
run_manipulator = True

while run_manipulator:
    print()
    get_input()
    check = input("Run again? (y/n): ").lower()
    if check in yes:
        run_manipulator = True
    else:
        run_manipulator = False