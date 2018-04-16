from .instruments import *
import re
import functools

note_regex = re.compile("^(?:[A-G][b#]?[0-8]|X)$")
time_regex = re.compile("^[0-9.]+\/?[0-9.]*$")
instrument_regex = re.compile("^\[([a-z]+)\]$")

instruments = {"sine":SineWave(), "saw":SawWave(), "snare":Snare(), "drum":Drum(), "ping":Ping(), "organ":Organ()}

def get_sections(data):
    bracket_level = 0
    sections = []
    record = ""
    i = 0
    for letter in data:
        i += 1
        record += letter
        if letter == "(":
            bracket_level += 1
        if letter == ")":
            if bracket_level == 1:
                break
            bracket_level -= 1
        if letter == "," and bracket_level == 1:
            sections.append(record)
            record = ""
    sections.append(record)
    return [section.strip()[1 if section.startswith("(") else 0:-1] for section in sections], i

def interpret(content, note_duration=0.25, instrument="sine"):
    
    print(content)
    
    out = Segment()
    
    data = content.replace("\n", "").replace(" ", "")
    print(data)
    
    cooldown = 0
    
    i1 = 0
    i2 = 1
    
    expanding = False
    valid = False
    do = False
    
    while i2 <= len(data):
        section = data[i1:i2]
        print(section)
        
        if section == "(":
            subsections, cooldown = get_sections(data[i1:])
            i1 += cooldown
            i2 = i1
            out += functools.reduce(Segment.__mul__, [interpret(s, note_duration, instrument) for s in subsections], Segment())
            
        elif time_regex.match(section):
            expanding = True
            valid = True
            if do:
                if "/" in section:
                    fraction = section.split("/")
                    note_duration = int(fraction[0]) / int(fraction[1])
                else:
                    note_duration = float(section)
                i1 = i2
            
        elif note_regex.match(section):
            out += instruments[instrument].use(section, note_duration)
            i1 = i2
        
        elif section == "_":
            out += Silence(note_duration)
            i1 = i2
        
        elif instrument_regex.match(section):
            instrument = section[1:-1]
            i1 = i2
        
        else:
            valid = False
        
        if do:
            do = False
            expanding = False
            valid = False
        elif expanding and not valid:
            i2 -= 2
            do = True
            
        i2 += 1
            
    return out
