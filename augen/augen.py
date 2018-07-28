import math
import wave
import struct

try:
    import pyaudio
    p = pyaudio.PyAudio()
    chunk = 1024
    device = p.get_default_output_device_info()["index"]
    PYAUDIO_PRESENT = True
except:
    PYAUDIO_PRESENT = False

from . import audio_info
from .functions import Segment
from .functions import Sample

formats = {1:"b", 2:"h", 4:"l"}

def play(segment, bits_per_sample=2, audio_device_index=None):
    if not PYAUDIO_PRESENT:
        print("You do not have PyAudio. Install it to play sounds without dumping the data.")
        return
        
    if audio_device_index is None:
        audio_device_index = p.get_default_output_device_info()["index"]
        
    stream = p.open(format=p.get_format_from_width(bits_per_sample),
                    channels=1,
                    rate=audio_info["SAMPLE_RATE"],
                    output_device_index=audio_device_index,
                    output=True)
    
    samples = [int(x) for x in segment.samples]
    
    for i in range(0, len(samples), chunk):
        sample_chunk = samples[i:i+chunk]
        data = struct.pack("<{}{}".format(len(sample_chunk), formats[bits_per_sample]), *sample_chunk)
        stream.write(data)
    
    stream.stop_stream()
    stream.close()

def save(samples, path, bits_per_sample=2):
    """ takes a segment and writes it to a wav file. mono only. """
    
    file = wave.open(path, "w")
    file.setparams((1, bits_per_sample, audio_info["SAMPLE_RATE"], len(samples), "NONE", "not compressed"))
    
    for sample in samples:

        file.writeframes(struct.pack(formats[bits_per_sample], int(sample)))
    
    file.close()

def load(path):
    """ extracts all samples from a wav file and returns a segment. only supports mono. """
    
    file = wave.open(path, "r")
    
    channels = file.getnchannels()
    bits_per_sample = file.getsampwidth()
    
    samples = []
    
    for i in range(file.getnframes()):
        data = struct.unpack("<{}{}".format(channels, formats[bits_per_sample]), file.readframes(1))
        samples.append(Sample(int(data[0]), 1))
    
    return Segment(samples)
