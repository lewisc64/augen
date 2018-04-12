from .functions import *
from .notes import *
import re
import functools

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
        noise1, noise2 = WhiteNoise(volume, 0.5).split(0.01)
        noise1.fade_in()
        noise2.fade_out()
        return noise1 + noise2 + Silence(duration - 0.5)

class Drum(Instrument):
    def use(self, note, duration, volume=1):
        noise1, noise2 = BrownianNoise(volume * 1.5, 0.5).split(0.01)
        noise1.fade_in()
        noise2.fade_out()
        return noise1 + noise2 + Silence(duration - 0.5)
        

note_regex = re.compile("^[A-G][b#]?[0-8]$")
time_regex = re.compile("^[0-9.]+$")
instrument_regex = re.compile("\[([a-z]+)\]")

instruments = {"sine":SineWave(), "saw":SawWave(), "snare":Snare(), "drum":Drum()}

def get_sections(data):

    bracket_level = 0
    sections = []
    record = ""
    i = 0
    for section in data:
        i += 1
        record += section + " "
        if "(" in section:
            bracket_level += 1
        elif ")" in section:
            if bracket_level == 1:
                break
            bracket_level += 1
        elif "," in section and bracket_level == 1:
            sections.append(record)
            record = ""
    sections.append(record)
    return [section.strip()[1 if section.startswith("(") else 0:-1] for section in sections], i

def interpret(content, note_duration=None, instrument="sine"):
    
    out = Segment()
    
    data = content.replace("\n", " ").split()
    
    cooldown = 0
    
    for i, section in enumerate(data):
        if cooldown > 0:
            cooldown -= 1
            continue
            
        if "(" in section:
            subsections, cooldown = get_sections(data[i:])
            cooldown -= 1
            out += functools.reduce(Segment.__mul__, [interpret(s, note_duration, instrument) for s in subsections], Segment())
            
        elif time_regex.match(section):
            note_duration = float(section)
            
        elif note_regex.match(section):
            out += instruments[instrument].use(section, note_duration)
        
        elif "_" in section:
            out += Silence(note_duration)
        
        elif "[" in section:
            instrument = instrument_regex.search(section).group(1)
            
    return out
