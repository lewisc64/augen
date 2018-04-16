import augen

length = 5

wave = augen.BrownianNoise(1, length)
wave_in, wave_out = wave.split(length / 2)

wave_in.fade_in()
wave_out.fade_out()

augen.save((wave_in + wave_out) * 5, "output.wav")
