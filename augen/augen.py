import math
import wave
import struct

from . import SAMPLE_RATE
from . import BASE_AMPLITUDE
from .functions import Segment
from .functions import Sample

def save(samples, path):
    """ takes a segment and writes it to a wav file. """
        
    file = wave.open(path, "w")
    file.setparams((1, 2, SAMPLE_RATE, len(samples), "NONE", "not compressed"))
    
    for sample in samples:

        file.writeframes(struct.pack("h", int(sample.value * sample.volume)))
    
    file.close()

def load(path):
    file = wave.open(path, "r")
    
    samples = []
    
    for i in range(file.getnframes()):
        data = struct.unpack("<h", file.readframes(1))
        samples.append(Sample(int(data[0]), 1))
    
    return Segment(samples)