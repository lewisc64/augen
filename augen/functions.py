import math
import random
import copy
from . import audio_info

class Segment:
    def __init__(self, samples=None):
        if samples is None:
            self.samples = []
        else:
            self.samples = samples

    def __iter__(self):
        """ returns the samples """
        return (x for x in self.samples)

    def __len__(self):
        """ returns the amount of samples """
        return len(self.samples)
    
    def __getitem__(self, key):
        """ returns the sample at an index. returns sliced segment if slice. """
        if isinstance(key, slice):
            return Segment(self.samples[key.start:key.stop:key.step])
        else:
            return self.samples[key]

    def __setitem__(self, i, v):
        self.samples[i] = v
    
    def __add__(self, segment):
        """ appends two segment objects. """
        return Segment(self.samples + segment.samples)
    
    def __mul__(self, value):
        if type(value) is int:
            return Segment(self.samples * value)
        elif isinstance(value, Segment):
            if len(self) > len(value):
                out = self.copy()
                out.merge(value)
            else:
                out = value.copy()
                out.merge(self)
            return out
        
    def copy(self):
        return copy.deepcopy(self)
    
    def merge(self, segment):
        """ merge a given segment into this one. """
        if len(segment) > len(self):
            raise ValueError("Given segment is longer than self.")
        for i in range(len(segment)):
            self.samples[i] += segment[i]
    
    def duration(self):
        """ returns the length in seconds. """
        return len(self.samples) / audio_info["SAMPLE_RATE"]
    
    def repeat_until_duration(self, duration):
        length = len(self)
        i = length
        while self.duration() < duration:
            self.samples.append(self.samples[i - length])
            i += 1 

    def change_speed(self, speed):
        samples = []
        expected_samples = len(self.samples) * (1 / speed)
        for i, v in enumerate(self.samples):
            while (i / len(self.samples)) * expected_samples > len(samples):
                samples.append(v)
        self.samples = samples

    def echo(self, delay, decay, amount=1):
        echoed = self.copy()
        for x in range(amount):
            echoed.samples = [x * decay for x in echoed.samples]
            echoed = (Silence(delay) + echoed)[:len(self)]
            self.merge(echoed)

    def reverse(self):
        self.samples = self.samples[::-1]

    def split(self, seconds):
        """ splits the segment into two, cut at seconds given. """
        sample = int(seconds * audio_info["SAMPLE_RATE"])
        return self[:sample], self[sample:]
    
    def fade_in(self):
        """ increases the volume from 0 to the volume of the last sample. """
        for i, sample in enumerate(self.samples):
            self.samples[i] = sample * (i / len(self.samples))
    
    def fade_out(self):
        """ decreases the volume from the volume of the first sample. """
        for i, sample in enumerate(self.samples):
            self.samples[i] = sample * (1 - i / len(self.samples))
    
    def invert(self):
        for i, sample in enumerate(self.samples):
            self.samples[i] = -sample
    
    def function(self, n, amount):
        raise NotImplemented
    
    def construct(self, duration):
        """ generates many samples and returns them as a list """
        samples = int(duration * audio_info["SAMPLE_RATE"])
        return [self.function(x, samples) for x in range(samples)]
        
class Sine(Segment):
    def __init__(self, frequency, volume, duration, **kwargs):
        self.frequency = frequency
        self.volume = volume
        super().__init__(self.construct(duration))
        
    def function(self, n, amount):
        return math.sin(n * 2 * math.pi * self.frequency / audio_info["SAMPLE_RATE"]) * audio_info["BASE_AMPLITUDE"] * self.volume

class Saw(Segment):
    def __init__(self, frequency, volume, duration, **kwargs):
        self.frequency = frequency
        self.volume = volume
        super().__init__(self.construct(duration))
    
    def function(self, n, amount):
        return ((n % (audio_info["SAMPLE_RATE"] / self.frequency)) * (self.frequency / audio_info["SAMPLE_RATE"]) * 2 - 1) * audio_info["BASE_AMPLITUDE"] * self.volume

class Square(Segment):
    def __init__(self, frequency, volume, duration, **kwargs):
        self.frequency = frequency
        self.volume = volume
        super().__init__(self.construct(duration))
    
    def function(self, n, amount):
        return (1 if ((n % (audio_info["SAMPLE_RATE"] / self.frequency)) * (self.frequency / audio_info["SAMPLE_RATE"]) * 2 - 1) > 0 else -1) * audio_info["BASE_AMPLITUDE"] * self.volume

class WhiteNoise(Segment):
    def __init__(self, volume, duration, **kwargs):
        self.volume = volume
        super().__init__(self.construct(duration))
    
    def function(self, n, amount):
        return (random.random() * 2 - 1) * audio_info["BASE_AMPLITUDE"] * self.volume

class BrownianNoise(Segment):
    def __init__(self, volume, duration, **kwargs):
        self.frequency = 0
        self.volume = volume
        super().__init__(self.construct(duration))
    
    def function(self, n, amount):
        self.frequency = max(min(self.frequency + (random.random() * 2 - 1) / 5, 1), -1)
        return self.frequency * audio_info["BASE_AMPLITUDE"] * self.volume

class SlidingSine(Segment):
    def __init__(self, f_start, f_stop, volume, duration, **kwargs):
        self.f_start = f_start
        self.f_stop = f_stop
        self.volume = volume
        super().__init__(self.construct(duration))
        
    def function(self, n, amount):
        f = self.f_start + (self.f_stop - self.f_start) * (n / amount)
        return math.sin(n * 2 * math.pi * f / audio_info["SAMPLE_RATE"]) * audio_info["BASE_AMPLITUDE"] * self.volume

class Silence(Segment):
    def __init__(self, duration, **kwargs):
        super().__init__(self.construct(duration))
    
    def function(self, n, amount):
        return 0
