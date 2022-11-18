#!/usr/bin/env python3

import time
import pyaudio
import threading
import numpy as np

class WavePlayerLoop(threading.Thread) :

  def __init__(self, freq=440., length=1., volume=0.5):
    threading.Thread.__init__(self)
    self.p = pyaudio.PyAudio()

    self.volume = volume     # range [0.0, 1.0]
    self.fs = 44100          # sampling rate, Hz, must be integer
    self.duration = length   # in seconds, may be float
    self.f = freq            # sine frequency, Hz, may be float

  def run(self) :
    # generate samples, note conversion to float32 array
    self.samples = (np.sin(2*np.pi*np.arange(self.fs*self.duration)*self.f/self.fs)).astype(np.float32)

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    self.stream = self.p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=self.fs,
                    output=True)
    
    self.stream.write(self.volume*self.samples)

    self.stream.stop_stream()
    self.stream.close()

    self.p.terminate()

s = WavePlayerLoop(freq=240, length=15, volume=0.5)
r = WavePlayerLoop(freq=3000, length=15, volume=0.5)

r.start()
time.sleep(3)
s.start()
