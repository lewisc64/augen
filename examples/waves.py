import augen

duration = 5

wave = augen.BrownianNoise(1, duration)
wave_in, wave_out = wave.split(duration / 2)

wave_in.fade_in()
wave_out.fade_out()

augen.play((wave_in + wave_out) * 5)
