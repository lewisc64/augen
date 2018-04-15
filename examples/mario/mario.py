import augen

file = open("mario.augen")
content = file.read()
file.close()

augen.save(augen.music.interpret(content), "mario.wav")
