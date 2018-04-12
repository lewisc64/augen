import math
import wave
import struct

from . import SAMPLE_RATE
from . import BASE_AMPLITUDE

def output(samples, path):
    """ takes a segment and writes it to a wav file. """
        
    wav_file = wave.open(path, "w")
    wav_file.setparams((1, 2, SAMPLE_RATE, len(samples), "NONE", "not compressed"))
    
    for sample in samples:
        wav_file.writeframes(struct.pack("h", int(sample.value * sample.volume * BASE_AMPLITUDE / 2)))
    wav_file.close()

