import augen

file = open("entertainer.augen")
content = file.read()
file.close()

augen.save(augen.music.interpret(content), "entertainer.wav")
