#!/usr/bin/env python3

import sys
import argparse

import numpy as np
import sounddevice as sd


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)

args, remaining = parser.parse_known_args()

parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])

parser.add_argument(
    'frequency',
    nargs='?',
    type=float,
    default=500,
    help='frequency in Hz (DEFAULT: %(default)s)')
parser.add_argument(
    '-a',
    type=float,
    default=1.0,
    help='Amplitude (DEFAULT: %(default)s)')
parser.add_argument(
    '-d',
    type=int_or_str,
    help='Output Device')
args = parser.parse_args(remaining)

start_idx = 0

try:
    samplerate = sd.query_devices(args.d, 'output')['default_samplerate']

    def callback(outdata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        global start_idx
        t = (start_idx + np.arange(frames)) / samplerate
        t = t.reshape(-1, 1)
        outdata[:] = args.a * np.sin(2 * np.pi * args.frequency * t)
        start_idx += frames

    with sd.OutputStream(device=args.d, callback=callback, samplerate=samplerate):
        print()
        print('#' * 80)
        print('\t\t\t\t Return to quit')
        print('#' * 80)
        input()

except KeyboardInterrupt:
    parser.exit('')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))