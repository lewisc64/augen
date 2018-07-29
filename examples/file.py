import augen

file = open(input("path: "))
content = file.read()
file.close()

augen.play(augen.music.interpret(content))
