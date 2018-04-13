from .functions import *
from .notes import *

class Instrument:
    def __init__(self):
        pass

    def use(self, note, duration, volume=1):
        raise NotImplemented

class SineWave(Instrument):
    def use(self, note, duration, volume=1):
        return Sine(get_frequency(note), volume, duration)

class SawWave(Instrument):
    def use(self, note, duration, volume=1):
        return Saw(get_frequency(note), volume, duration)

class Snare(Instrument):
    def use(self, note, duration, volume=1):
        noise1, noise2 = WhiteNoise(volume, min(0.5, duration)).split(0.01)
        noise1.fade_in()
        noise2.fade_out()
        return noise1 + noise2 + Silence(duration - min(0.5, duration))

class Drum(Instrument):
    def use(self, note, duration, volume=1):
        noise1, noise2 = BrownianNoise(volume, min(0.2, duration)).split(0.01)
        noise1.fade_in()
        noise2.fade_out()
        return noise1 + noise2 + Silence(duration - min(0.2, duration))

class Ping(Instrument):
    def use(self, note, duration, volume=1):
        out = Sine(get_frequency(note), volume, duration)
        out.fade_out()
        return out

class Piano(Instrument):
    def use(self, note, duration, volume=1):
        out = Sine(get_frequency(note), volume, duration) * Sine(get_frequency(note) / 2, volume / 2, duration) * Sine(get_frequency(note) * 2, volume / 2, duration)
        return out
