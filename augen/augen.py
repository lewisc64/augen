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

class PyAudioNotPresent(Exception):
    def __init__(self):
        super().__init__("You do not have PyAudio. Install it to stream sounds to audio devices.")

class SamplerateMismatch(Exception):
    def __init__(self, s):
        super().__init__("""The sample rate of the file is set to {} Hz. augen is using {} Hz.
Ensure that augen.audio_info[\"SAMPLE_RATE\"] is equal to the file's.
Note that if augen.audio_info[\"SAMPLE_RATE\"] is changed after sounds are generated, the sounds will be pitch shifted.""".format(s, audio_info["SAMPLE_RATE"]))

class UnknownBitDepth(Exception):
    def __init__(self, bit_depth):
        super().__init__(str(bit_depth))

def play(segment, bit_depth=2, audio_device_index=None):
    if not PYAUDIO_PRESENT:
        raise PyAudioNotPresent()
        
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
    thread = Thread(target=play, args=(segment, bit_depth, audio_device_index))
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
    sample_rate = file.getframerate()

    if sample_rate != audio_info["SAMPLE_RATE"]:
        raise SamplerateMismatch(sample_rate)

    if bit_depth not in formats:
        raise UnknownBitDepth(bit_depth)
    
    samples = []
    
    for i in range(file.getnframes()):
        data = struct.unpack("<{}{}".format(channels, formats[bit_depth]), file.readframes(1))
        samples.append(int(data[0]))

    segment = Segment(samples)
    
    return Segment(samples)
