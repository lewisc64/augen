import augen
import augen.file

file = open("mario.augen")
content = file.read()
file.close()

augen.output(augen.file.interpret(content), "mario.wav")
