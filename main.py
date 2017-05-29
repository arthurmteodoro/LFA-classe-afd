#            Primeiro Trabalho de LFA
# Arthur Alexsander Martins Teodoro - 0022427
# Saulo Ricardo Dias Fernandes - 0021581
# Data: 05/05/2017

from AFD import *

automata1 = AFD()
automata1.load("minimizacaoProva.jff")
print "Estados equivalentes:"
print automata1.equivalentsStates()
automata1Min = automata1.minimum()
automata1Min.save("automatoProvaMinimizado.jff")

if AFD.equivalents(automata1, automata1Min):
	print "Os automatos sao equivalentes"
else:
	print "Os automatos nao sao equivalentes"
	
#quantidade par de a's
automata2 = AFD()
automata2.addState(0, True, True)
automata2.addState(1)
automata2.addTransition(0, 1, "a")
automata2.addTransition(1, 0, "a")
automata2.addTransition(0, 0, "b")
automata2.addTransition(1, 1, "b")

#quantidade impar de b's
automata3 = AFD()
automata3.addState(0, initial=True)
automata3.addState(1, final=True)
automata3.addTransition(0, 1, "b")
automata3.addTransition(1, 0, "b")
automata3.addTransition(0, 0, "a")
automata3.addTransition(1, 1, "a")

automata4 = automata2.difference(automata3)
if automata4.accept("aaaabbbb"):
	print "Palavra aceita"
else:
	print "Palavra nao aceita"
