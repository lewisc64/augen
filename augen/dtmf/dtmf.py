from ..functions import *

characters = {
    "1":[697, 1209],
    "2":[697, 1336],
    "3":[697, 1477],
    "A":[697, 1633],
    "4":[770, 1209],
    "5":[770, 1336],
    "6":[770, 1477],
    "B":[770, 1633],
    "7":[852, 1209],
    "8":[852, 1336],
    "9":[852, 1477],
    "C":[852, 1633],
    "*":[941, 1209],
    "0":[941, 1336],
    "#":[941, 1477],
    "D":[941, 1633],
}

def generate(sequence, tone_duration=0.1, silence_duration=0.1):
    out = Segment()
    for char in sequence:
        segment = Silence(tone_duration)
        if char in characters:
            for freq in characters[char]:
                segment *= Square(freq, 1, tone_duration)
            out += segment + Silence(silence_duration)
    return out