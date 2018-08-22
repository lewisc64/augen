import math
import wave
import struct
from threading import Thread

try:
    import pyaudio
    p = pyaudio.PyAudio()
    chunk = 1024
    PYAUDIO_PRESENT = True
except:
    PYAUDIO_PRESENT = False

from . import audio_info
from .functions import Segment

formats = {1:"b", 2:"h", 4:"l"}

def play(segment, bit_depth=2, audio_device_index=None):
    if not PYAUDIO_PRESENT:
        print("You do not have PyAudio. Install it to play sounds without dumping the data.")
        return
        
    if audio_device_index is None:
        audio_device_index = p.get_default_output_device_info()["index"]
        
    stream = p.open(format=p.get_format_from_width(bit_depth),
                    channels=1,
                    rate=audio_info["SAMPLE_RATE"],
                    output_device_index=audio_device_index,
                    output=True)
    
    samples = [int(x) for x in segment.samples]
    
    for i in range(0, len(samples), chunk):
        sample_chunk = samples[i:i+chunk]
        data = struct.pack("<{}{}".format(len(sample_chunk), formats[bit_depth]), *sample_chunk)
        stream.write(data)
    
    stream.stop_stream()
    stream.close()

def play_async(segment, bit_depth=2, audio_device_index=None):
    """ calls the play function in a thread, then returns the thread """
    thread = Thread(target = play, args = (segment, bit_depth, audio_device_index))
    thread.start()
    return thread

def save(samples, path, bit_depth=2):
    """ takes a segment and writes it to a wav file. mono only. """
    
    file = wave.open(path, "w")
    file.setparams((1, bit_depth, audio_info["SAMPLE_RATE"], len(samples), "NONE", "not compressed"))
    
    for sample in samples:

        file.writeframes(struct.pack(formats[bit_depth], sample))
    
    file.close()

def load(path):
    """ extracts all samples from a wav file and returns a segment. only supports mono. """
    
    file = wave.open(path, "r")
    
    channels = file.getnchannels()
    bit_depth = file.getsampwidth()
    
    samples = []
    
    for i in range(file.getnframes()):
        data = struct.unpack("<{}{}".format(channels, formats[bit_depth]), file.readframes(1))
        samples.append(int(data[0]))
    
    return Segment(samples)
