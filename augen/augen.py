import math
import wave
import struct

from . import audio_info
from .functions import Segment
from .functions import Sample

formats = {1:"b", 2:"h", 4:"l"}

def save(samples, path, bits_per_sample=2):
    """ takes a segment and writes it to a wav file. mono only. """
    
    file = wave.open(path, "w")
    file.setparams((1, bits_per_sample, audio_info["SAMPLE_RATE"], len(samples), "NONE", "not compressed"))
    
    for sample in samples:

        file.writeframes(struct.pack(formats[bits_per_sample], int(sample.value * sample.volume)))
    
    file.close()

def load(path):
    """ extracts all samples from a wav file and returns a segment. only supports mono. """
    
    file = wave.open(path, "r")
    print("sample width: {}".format(file.getsampwidth()))
    print("samplerate: {}".format(file.getframerate()))
    print("channels: {}".format(file.getnchannels()))
    
    channels = file.getnchannels()
    bits_per_sample = file.getsampwidth()
    
    samples = []
    
    for i in range(file.getnframes()):
        d = file.readframes(1)
        #print(d)
        #print("<{}{}".format(channels, formats[bits_per_sample]))
        #print(d)
        #print(d[::channels])
        data = struct.unpack("<{}{}".format(channels, formats[bits_per_sample]), d)
        #print(int(data[0]))
        samples.append(Sample(int(data[0]), 1))
    
    return Segment(samples)
