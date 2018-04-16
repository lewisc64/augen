import augen

file = open(input("path: "))
content = file.read()
file.close()

augen.save(augen.music.interpret(content), "output.wav")
