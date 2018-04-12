import augen
import augen.file

file = open("entertainer.augen")
content = file.read()
file.close()

augen.output(augen.file.interpret(content), "entertainer.wav")
