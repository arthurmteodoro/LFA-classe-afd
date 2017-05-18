from AFD import *

automata1 = AFD()
automata1.load("minimizacaoProva.jff")

#automata2 = AFD()
#automata2.load("automata1.jff")

#automata3 = automata1.intersection(automata2)

#if automata1.accept("aabbaa"):
#    print "Automato 1 aceito com esta palavra"
#else:
#    print "automato 1 rejeitou esta palavra"
#
#if automata2.accept("baba"):
#    print "Automato 2 aceitou baba"
#else:
#    print "Automato 2 rejeitou baba"
#
#estado = automata1.initial()
#estado = automata1.move(estado, "aabbaa")
#if estado in automata1.finals():
#    print "Aceitou"
#else:
#    print "Rejeitou"

#automata1.equivalents()
#automata3 = automata1.intersection(automata2)
#ai = automata1.equivalents()
#automata1.salve("aaaaaa.jff")

automata2 = AFD()
automata2.addState(1, initial=True)
automata2.addState(2, final=True)
automata2.addState(3, final=True)
automata2.addState(4, final=True)
automata2.addTransition(1, 2, 'a')
automata2.addTransition(1, 3, 'b')
automata2.addTransition(1, 4, 'c')
print automata2.equivalents()
automata2.salve("aiaia.jff")