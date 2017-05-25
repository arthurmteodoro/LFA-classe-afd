from AFD import *

automata1 = AFD()
automata1.addState(1, initial=True)
automata1.addState(2, final=True)
automata1.addState(3)
automata1.addTransition(1, 2, 'a')
automata1.addTransition(1, 2, 'b')
automata1.addTransition(2, 3, 'a')
automata1.addTransition(2, 3, 'b')
automata1.addTransition(3, 3, 'a')
automata1.addTransition(3, 3, 'a')
#automata1.load("minimizacaoProva.jff")

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

#automata2 = AFD()
#automata2.addState(1, initial=True)
#automata2.addState(2, final=True)
#automata2.addState(3, final=True)
#automata2.addState(4, final=True)
#automata2.addTransition(1, 2, 'a')
#automata2.addTransition(1, 3, 'b')
#automata2.addTransition(1, 4, 'c')

#automata3 = automata1.minimum()
#automata3.salve("ababab.jff")
automata3 = AFD()
automata3.addState(1, initial=True)
automata3.addState(2)
automata3.addState(3, final=True)
automata3.addTransition(1, 2, 'a')
automata3.addTransition(1, 2, 'b')
automata3.addTransition(2, 3, 'a')
automata3.addTransition(2, 3, 'b')
automata3.addTransition(3, 3, 'a')
automata3.addTransition(3, 3, 'a')
#automata3.load("automata2.jff")

if AFD.equivalents(automata1, automata3):
    print "Equivalentes"
else:
    print "Nao equivalentes"

automata3.save("aa.jff")

automata2 = AFD()
automata2.load("automata3.jff")
automata2.save("bb.jff")