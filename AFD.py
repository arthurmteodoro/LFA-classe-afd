from __future__ import print_function
from State import *
from Transition import *

class AFD(object):

    def __init__(self):
        self.__listState = []
        self.__alphabet = []
        self.__transistions = []
        self.__initalState = None
        self.__finalStates = []

    def getInitialState(self):
        return self.__initalState

    def addState(self, id, initial=False, final=False):
        if initial and self.__initalState != None:
            return False

        state = State(id)
        state.setInitial(initial)
        state.setFinal(final)

        self.__listState.append(state)
        if(final):
            self.__finalStates.append(state)

        if(initial and self.__initalState == None):
            self.__initalState = state

    def addTransition(self, idSource, idDestination, consume):
        idSource = str(idSource)
        idDestination = str(idDestination)

        stateSource = None
        stateDestination = None

        for state in self.__listState:
            if(state.getId() == idSource):
                stateSource = state
            if(state.getId() == idDestination):
                stateDestination = state

        transition = Transition(stateSource, stateDestination, consume)

        if(consume not in self.__alphabet):
            self.__alphabet.append(consume)

        self.__transistions.append(transition)

    def __outputList__(self, state):
        listTransistion = []
        for transition in self.__transistions:
            if transition.getSource() == state:
                listTransistion.append(transition)
        return listTransistion

    def accept(self, input):
        state = self.__initalState

        for char in input:

            listTransition = self.__outputList__(state)

            if char not in self.__alphabet:
                return False

            encontrouTransicao = False
            for transistion in listTransition:
                if transistion.getConsume() == char:
                    encontrouTransicao = True
                    state = transistion.getDestination()
                    break

            if encontrouTransicao == False:
                return False

        return True if state.getFinal() else False

    def getStateById(self, stateId):
        for state in self.__listState:
            if state.getId() == stateId:
                return state

    def __createMultiplication__(self, automata):
        newAutomata = AFD()
        for stateA in self.__listState:
            for stateB in automata.__listState:
                newAutomata.addState(stateA.getId()+"."+stateB.getId())

        for state in newAutomata.__listState:
            statesSplit = state.getId().split(".")

            stateA = self.getStateById(statesSplit[0])
            stateB = automata.getStateById(statesSplit[1])

            listA = self.__outputList__(stateA)
            listB = automata.__outputList__(stateB)

            for char in self.__alphabet:
                stateDestination = ""
                for transitionA in listA:
                    if transitionA.getConsume() == char:
                        stateDestination += transitionA.getDestination().getId()

                stateDestination += "."

                for transitionB in listB:
                    if transitionB.getConsume() == char:
                        stateDestination += transitionB.getDestination().getId()

                newAutomata.addTransition(state.getId(), stateDestination, char)

        return newAutomata

    def intersection(self, automata):
        newAutomata = self.__createMultiplication__(automata)
        stateA = self.getInitialState()
        stateB = automata.getInitialState()

        initialState = newAutomata.getStateById(stateA.getId()+"."+stateB.getId())
        initialState.setInitial(True)
        newAutomata.__initalState = initialState

        for stateA in self.__listState:
            for stateB in automata.__listState:
                if(stateA.getFinal() and stateB.getFinal()):
                    finalState = newAutomata.getStateById(stateA.getId()+"."+stateB.getId())
                    finalState.setFinal(True)
                    newAutomata.__finalStates.append(finalState)

        return newAutomata


if __name__ == "__main__":

#    aPar = AFD()
#    aPar.addState(1, True, True)
#    aPar.addState(2)
#    aPar.addTransition(1, 2, "a")
#    aPar.addTransition(2, 1, "a")
#    aPar.addTransition(1, 1, "b")
#    aPar.addTransition(2, 2, "b")

#    bPar = AFD()
#    bPar.addState(1, True, True)
#    bPar.addState(2)
#    bPar.addTransition(1, 1, "a")
#    bPar.addTransition(1, 2, "b")
#    bPar.addTransition(2, 2, "a")
#    bPar.addTransition(2, 1, "b")
#
#    m = aPar.intersection(bPar)

#    notAba = AFD()
#    notAba.addState(1, True, True)
#    notAba.addState(2, False, True)
#    notAba.addState(3, False, True)
#    notAba.addState(4)
#    notAba.addTransition(1, 2, "a")
#    notAba.addTransition(1, 1, "b")
#    notAba.addTransition(2, 2, "a")
#    notAba.addTransition(2, 3, "b")
#    notAba.addTransition(3, 4, "a")
#    notAba.addTransition(3, 1, "b")
#    notAba.addTransition(4, 4, "a")
#    notAba.addTransition(4, 4, "b")

#    notAbaAndAPar = aPar.intersection(notAba)
#    if(notAbaAndAPar.accept("aaaabaa")):
#        print("aceitou")
#    else:
#        print("nao aceitou")

    segBImpar = AFD()
    segBImpar.addState(1, True)
    segBImpar.addState(2, final=True)
    segBImpar.addState(3, final=True)
    segBImpar.addState(4)
    segBImpar.addState(5)
    segBImpar.addTransition(1, 1, "a")
    segBImpar.addTransition(1, 2, "b")
    segBImpar.addTransition(2, 3, "a")
    segBImpar.addTransition(2, 4, "b")
    segBImpar.addTransition(3, 3, "a")
    segBImpar.addTransition(3, 2, "b")
    segBImpar.addTransition(4, 5, "a")
    segBImpar.addTransition(4, 2, "b")
    segBImpar.addTransition(5, 5, "a")
    segBImpar.addTransition(5, 5, "b")

    segAPar = AFD()
    segAPar.addState(1, True, True)
    segAPar.addState(2)
    segAPar.addState(3)
    segAPar.addTransition(1, 2, "a")
    segAPar.addTransition(1, 1, "b")
    segAPar.addTransition(2, 1, "a")
    segAPar.addTransition(2, 3, "b")
    segAPar.addTransition(3, 3, "a")
    segAPar.addTransition(3, 3, "b")

    m = segBImpar.intersection(segAPar)

    if m.accept("aaaabbbaabaaaabbb"):
        print("aceitou")
    else:
        print("nao aceitou")