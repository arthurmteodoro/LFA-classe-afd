from AFD import *

automata1 = AFD()
automata1.load("automata.jff")

automata2 = AFD()
automata2.load("automata1.jff")

if automata1.accept("aabbaa"):
    print "Automato 1 aceito com esta palavra"
else:
    print "automato 1 rejeitou esta palavra"

if automata2.accept("baba"):
    print "Automato 2 aceitou baba"
else:
    print "Automato 2 rejeitou baba"

automata3 = automata1.intersection(automata2)