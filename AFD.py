from __future__ import print_function #use python3 print function
import copy #use to copy a object
import xml.etree.ElementTree as ET #XML
from xml.dom import minidom

class State(object):
    """
    Class of state for AFD
    """
    def __init__(self, id):
        self.__id = str(id)
        self.__initial = False
        self.__final = False

    def getId(self):
        return self.__id

    def setId(self, id):
        self.__id = id

    def getInitial(self):
        return self.__initial

    def setInitial(self, value):
        self.__initial = value

    def getFinal(self):
        return self.__final

    def setFinal(self, value):
        self.__final = value

    def __str__(self):
        return self.__id

class Transition(object):
    """
    Class for Transition for AFD
    """
    def __init__(self, source, destination, consume):
        self.__source = source
        self.__destination = destination
        self.__consume = consume

    def getSource(self):
        return self.__source

    def setSource(self, source):
        self.__source = source

    def getDestination(self):
        return self.__destination

    def setDestination(self, destination):
        self.__destination = destination

    def getConsume(self):
        return self.__consume

    def setConsume(self, consume):
        self.__consume = consume

    def __str__(self):
        return "Source: "+self.__source.getId()+" Destination: "+self.__destination.getId()+" Consume: "+self.__consume+"\n"

class Equivalent(object):
    """
    Class for equivalent state for AFD
    """
    def __init__(self, state1, state2):
        self.__states = (state1, state2)
        self.__equivalent = True
        self.__dependents = []

    def getStates(self):
        return self.__states

    def setStates(self, state1, state2):
        self.__states = (state1, state2)

    def getEquivalent(self):
        return self.__equivalent

    def setEquivalent(self, equivalent):
        self.__equivalent = equivalent

    def getDependents(self):
        return self.__dependents

    def setDependents(self, equivalent):
        self.__dependents = equivalent

    def __str__(self):
        return "States: ("+self.__states[0]+", "+self.__states[1]+") Equivalent: "+str(self.__equivalent)


class AFD(object):
    """
    Class that implements an automaton.
    """

    def __init__(self):
        """
        Create a empty automaton
        """
        self.__listState = []
        self.__alphabet = []
        self.__transitions = []
        self.__initialState = None
        self.__finalStates = []

    def __getInitialState(self):
        """
        get a initial state
        :return: initial state
        """
        return self.__initialState

    def addState(self, id, initial=False, final=False):
        """
        Function to add a new state in automaton
        :param id: state id (int)
        :param initial: if a state is initial (bool)
        :param final: if a state is final (bool)
        :return: if a state is create or not (bool)
        """
        if initial and self.__initialState != None:
            return False

        state = State(id)
        state.setInitial(initial)
        state.setFinal(final)

        self.__listState.append(state)
        if(final):
            self.__finalStates.append(state)

        if(initial and self.__initialState == None):
            self.__initialState = state

        return True

    def addTransition(self, idSource, idDestination, consume):
        """
        Add a transition in automaton
        :param idSource: state id for source (int)
        :param idDestination: state id for destination (int)
        :param consume: caracter to consume in transition (char)
        """
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

        self.__transitions.append(transition)

    def __outputList(self, state):
        """
        Returns a list of all transitions that exit this state
        :param state: State 
        :return: List of transitions
        """
        listTransistion = []
        for transition in self.__transitions:
            if transition.getSource() == state:
                listTransistion.append(transition)
        return listTransistion

    def accept(self, input):
        """
        Checks of this word is accepted
        :param input: word for test (string)
        :return: if word is accept or not (boolean)
        """
        state = self.__initialState

        for char in input:

            listTransition = self.__outputList(state)

            if char not in self.__alphabet:
                return False

            findTransition = False
            for transition in listTransition:
                if transition.getConsume() == char:
                    findTransition = True
                    state = transition.getDestination()
                    break

            if findTransition == False:
                return False

        return True if state.getFinal() else False

    def __getStateById(self, stateId):
        """
        Return a state by your Id
        :param stateId: id (string)
        :return: State or None case state not exist
        """
        for state in self.__listState:
            if state.getId() == stateId:
                return state
        return None

    def __getMaxId(self):
        """
        Return a max id for this automaton
        :return: max id (int)
        """
        listId = []
        for state in self.__listState:
            listId.append(int(state.getId()))
        return max(listId)

    def complete(self):
        """
        Complete this automaton, creating error state
        """
        stateError = State(self.__getMaxId()+900)
        newTransitions = []
        existError = False

        for state in self.__listState:
            if len(self.__outputList(state)) < len(self.__alphabet):
                existError = True

                transitionsEmpty = []
                for transition in self.__outputList(state):
                    transitionsEmpty.append(transition.getConsume())

                for char in self.__alphabet:
                    if char not in transitionsEmpty:
                        newTransition = Transition(state, stateError, char)
                        newTransitions.append(newTransition)

        if existError:
            self.__listState.append(stateError)

            for transition in newTransitions:
                self.__transitions.append(transition)

            for char in self.__alphabet:
                transition = Transition(stateError, stateError, char)
                self.__transitions.append(transition)


    def __createMultiplication(self, automata):
        """
        Create a new automaton with multiplication
        :param automata: automaton a multiplication (AFD)
        :return: new automaton (AFD)
        """
        #create a automata copy
        selfCopy = copy.deepcopy(self)
        automataCopy = copy.deepcopy(automata)

        selfCopy.complete()
        automataCopy.complete()

        newAutomaton = AFD()
        for stateA in selfCopy.__listState:
            for stateB in automataCopy.__listState:
                newAutomaton.addState(stateA.getId()+"."+stateB.getId())

        for state in newAutomaton.__listState:
            statesSplit = state.getId().split(".")

            stateA = selfCopy.__getStateById(statesSplit[0])
            stateB = automataCopy.__getStateById(statesSplit[1])

            listA = selfCopy.__outputList(stateA)
            listB = automataCopy.__outputList(stateB)

            for char in selfCopy.__alphabet:
                stateDestination = ""
                for transitionA in listA:
                    if transitionA.getConsume() == char:
                        stateDestination += transitionA.getDestination().getId()

                stateDestination += "."

                for transitionB in listB:
                    if transitionB.getConsume() == char:
                        stateDestination += transitionB.getDestination().getId()

                newAutomaton.addTransition(state.getId(), stateDestination, char)

        return newAutomaton

    def __deletePoint(self):
        """
        Remove a point create in multiplication
        """
        for state in self.__listState:
            listId = state.getId().split('.')
            state.setId(listId[0]+listId[1])

    def intersection(self, automata):
        """
        return a new automaton create by self intersection automata
        :param automata: automaton for intersection (AFD)
        :return: self intersection automata (AFD)
        """
        newAutomaton = self.__createMultiplication(automata)
        if newAutomaton == None:
            return None

        stateA = self.__getInitialState()
        stateB = automata.__getInitialState()

        initialState = newAutomaton.__getStateById(stateA.getId()+"."+stateB.getId())
        initialState.setInitial(True)
        newAutomaton.__initialState = initialState

        for stateA in self.__listState:
            for stateB in automata.__listState:
                if(stateA.getFinal() and stateB.getFinal()):
                    finalState = newAutomaton.__getStateById(stateA.getId()+"."+stateB.getId())
                    finalState.setFinal(True)
                    newAutomaton.__finalStates.append(finalState)

        newAutomaton.__deletePoint()
        return newAutomaton

    def union(self, automata):
        """
        return a new automaton create by self union automata
        :param automata: automaton for union (AFD)
        :return: self intersection automata (AFD)
        """
        newAutomaton = self.__createMultiplication(automata)
        if newAutomaton == None:
            return None

        stateA = self.__getInitialState()
        stateB = automata.__getInitialState()

        initialState = newAutomaton.__getStateById(stateA.getId()+"."+stateB.getId())
        initialState.setInitial(True)
        newAutomaton.__initialState = initialState

        for stateA in self.__listState:
            for stateB in automata.__listState:
                if(stateA.getFinal() or stateB.getFinal()):
                    finalState = newAutomaton.__getStateById(stateA.getId()+"."+stateB.getId())
                    finalState.setFinal(True)
                    newAutomaton.__finalStates.append(finalState)

        newAutomaton.__deletePoint()
        return newAutomaton

    def complement(self):
        """
        Create a complement automaton
        :return: complement automaton (AFD)
        """
        newAutomaton = copy.deepcopy(self)
        newAutomaton.complete()
        newAutomaton.__finalStates = []

        for state in newAutomaton.__listState:
            state.setFinal(not state.getFinal())
            if state.getFinal() == True:
                newAutomaton.__finalStates.append(state)
        return newAutomaton

    def difference(self, automata):
        """
        return a new automaton create by self difference automata
        :param automata: automaton for difference (AFD)
        :return: self difference automata (AFD)
        """
        automataB = automata.complement();
        return self.union(automataB)

    def load(self, name):
        """
        Load a automaton by JFLAP file
        :param name: JFLAP file (string)
        :return: Automaton by file (AFD)
        """
        try:
            # limpa o automato
            self.__listState = []
            self.__alphabet = []
            self.__transitions = []
            self.__initialState = None
            self.__finalStates = []

            tree = ET.parse(name)
            root = tree.getroot()

            #insere os estado
            for state in root.iter('state'):
                dataState = state.attrib

                #o estado e inicial e final
                if state.find('initial') != None and state.find('final') != None:
                    self.addState(int(dataState['id']), True, True)
                elif state.find('initial') != None:
                    self.addState(int(dataState['id']), True)
                elif state.find('final') != None:
                    self.addState(int(dataState['id']), final=True)
                else:
                    self.addState(int(dataState['id']))

            #insere as transicoes
            for transition in root.iter('transition'):

                #gera um dicionario com os dados de cada transacao
                dataTransition = {}
                for data in transition:
                    dataTransition[data.tag] = data.text

                self.addTransition(int(dataTransition['from']), int(dataTransition['to']), dataTransition['read'])

        except:
            return

    def __prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def save(self, name):
        """
        Save a automaton for JFLAP file
        :param name: name for file (string)
        """
        structure = ET.Element('structure')
        comment = ET.Comment("Create with class AFD by Arthur and Saulo")
        structure.append(comment)
        type = ET.SubElement(structure, 'type')
        type.text = 'fa'
        automaton = ET.SubElement(structure, 'automaton')

        comment = ET.Comment("The list of states.")
        automaton.append(comment)

        listStates = []
        for states in self.__listState:
            state = ET.Element('state', id=states.getId(), name=states.getId())
            if states.getInitial() == True:
                initial = ET.SubElement(state, 'initial')
            if states.getFinal() == True:
                final = ET.SubElement(state, 'final')
            listStates.append(state)

        automaton.extend(listStates)

        comment = ET.Comment("The list of transitions.")
        automaton.append(comment)

        for transitions in self.__transitions:
            transition = ET.SubElement(automaton, 'transition')

            from1 = ET.SubElement(transition, 'from')
            from1.text = str(transitions.getSource())

            to = ET.SubElement(transition, 'to')
            to.text = str(transitions.getDestination())

            read = ET.SubElement(transition, 'read')
            read.text = transitions.getConsume()

        arq = open(name, 'w')
        arq.write(self.__prettify(structure))

    def initial(self):
        """
        Get id for initial state
        :return: id (int)
        """
        return int(self.__getInitialState().getId())

    def move(self, stateP, wordP):
        """
        Move word in automaton starting state
        :param stateP: id fo state starting move (int)
        :param wordP: word to move (string)
        :return: state in word end (int)
        """
        state = self.__getStateById(str(stateP))
        word = wordP

        for char in word:

            listTransition = self.__outputList(state)

            if char not in self.__alphabet:
                return False

            findTransition = False
            for transition in listTransition:
                if transition.getConsume() == char:
                    findTransition = True
                    state = transition.getDestination()
                    break

            if not findTransition:
                return int(state.getId())

        return int(state.getId())

    def finals(self):
        """
        Return a list of final states id
        :return: list (list of int)
        """
        finalsList = []
        for state in self.__listState:
            if state.getFinal():
                finalsList.append(int(state.getId()))
        return finalsList

    def deleteTransition(self, source, target, consume):
        """
        Delete a transition
        :param source: state source of transition (int)
        :param target: state target of transition (int)
        :param consume: word of transition consume (string)
        """
        for transition in self.__transitions:
            if transition.getSource().getId() == str(source) and transition.getDestination().getId() == str(target)\
                    and transition.getConsume() == consume:
                self.__transitions.remove(transition)

    def deleteState(self, id):
        """
        Delete a state by your id
        :param id: state id (int)
        """
        index = 0
        while index < len(self.__transitions):
            if self.__transitions[index].getDestination().getId()== str(id)\
                    or self.__transitions[index].getSource().getId() == str(id):
                self.__transitions.pop(index)
                index -= 1
            index += 1

        for state in self.__listState:
            if state.getId() == str(id):
                self.__listState.remove(state)

        for state in self.__finalStates:
            if state.getId() == str(id):
                self.__finalStates.remove(state)

        if self.__initialState.getId() == str(id):
            self.__initialState = None

    @staticmethod
    def __markStates(equivalent):
        equivalent.setEquivalent(False)
        if(len(equivalent.getDependents()) > 0):
            for eq in equivalent.getDependents():
                if eq != equivalent:
                    AFD.__markStates(eq)

    def equivalentsStates(self):
        """
        Get a equivalents states in this automaton
        :return: list of tuple with id of states (list (tuple (int, int))
        """
        automaton = copy.deepcopy(self)
        automaton.complete()
        equivalent = []

        #generate a matrix
        initial = 1
        for i in xrange(len(automaton.__listState)-1):
            state1 = automaton.__listState[i]
            for j in xrange(initial, len(automaton.__listState)):
                state2 = automaton.__listState[j]
                equivalent1 = Equivalent(state1, state2)
                equivalent.append(equivalent1)
            initial += 1

        #set a non-final not equivalent a final states
        for eq in equivalent:
            states = eq.getStates()
            if states[0].getFinal() != states[1].getFinal():
                eq.setEquivalent(False)

        for eq in equivalent:
            if eq.getEquivalent() != False:
                states = eq.getStates()

                for char in automaton.__alphabet:
                    state0Move = automaton.__getStateById(str(automaton.move(states[0].getId(), char)))
                    state1Move = automaton.__getStateById(str(automaton.move(states[1].getId(), char)))

                    # search a equivalent matrix slot
                    if state0Move.getId() != state1Move.getId():
                        for eqSlot in equivalent:
                            if (eqSlot.getStates()[0].getId() == state0Move.getId() and eqSlot.getStates()[1].getId() == state1Move.getId()) or\
                               (eqSlot.getStates()[0].getId() == state1Move.getId() and eqSlot.getStates()[1].getId() == state0Move.getId()):
                                break

                        #com eqSlot encontrado verifica se estes states sao equivalentes
                        if eqSlot.getEquivalent() == False:
                            eq.setEquivalent(False)
                            break
                        else:
                            eqSlot.getDependents().append(eq)

        #marcar nao equivalentes na lista de dependencia de todos que nao sao equivalentes
        for eq in equivalent:
            if eq.getEquivalent() == False:
                AFD.__markStates(eq)

        #create a return list
        returnList = []
        for eq in equivalent:
            if eq.getEquivalent() == True:
                states = eq.getStates()
                returnTuple = (int(states[0].getId()), int(states[1].getId()))
                returnList.append(returnTuple)

        return returnList

    def __deleteNotReachedStates(self):
        """
        Deletes states that are not reached from the initial state  
        """
        visitedList = []
        stateList = []

        stateList.append(self.__initialState)
        while len(stateList) > 0:
            state = stateList[0]
            outTransitions = self.__outputList(state)

            for transition in outTransitions:
                if transition.getDestination() not in stateList and transition.getDestination() not in visitedList:
                    stateList.append(transition.getDestination())

            visitedList.append(state)
            stateList.remove(state)

        statesSet = set()
        stateVisitedSet = set()

        for state in self.__listState:
            statesSet.add(state.getId())

        for state in visitedList:
            stateVisitedSet.add(state.getId())

        deletes = statesSet.difference(stateVisitedSet)

        for stateDelete in deletes:
            self.deleteState(stateDelete)


    def minimum(self):
        """
        Get a minimum automaton
        :return: minimum automaton (AFD)
        """
        automaton = copy.deepcopy(self)
        automaton.__deleteNotReachedStates()
        automaton.complete()

        statesEquivalents = automaton.equivalentsStates()

        for eq in statesEquivalents:
            state0 = automaton.__getStateById(str(eq[0]))
            state1 = automaton.__getStateById(str(eq[1]))

            if state0 != None or state1 != None:
                for transition in automaton.__transitions:
                    if transition.getDestination() == state1:
                        transition.setDestination(state0)
                automaton.deleteState(int(state1.getId()))

        return automaton
    
    @staticmethod
    def equivalents(automaton1, automaton2):
        """
        Ckeck if a automaton1 and automaton2 is equivalents
        :param automaton1: first automaton (AFD)
        :param automaton2: second automaton (AFD)
        :return: if automaton1 and automaton2 is equivalents (boolean)
        """
        automaton1Copy = copy.deepcopy(automaton1)
        automaton2Copy = copy.deepcopy(automaton2)

        automaton1Copy.complete()
        automaton2Copy.complete()

        #change id for state id + 500 + max id of this automaton
        maxId = automaton2Copy.__getMaxId()
        for states in automaton2Copy.__listState:
            states.setId(str(int(states.getId())+maxId+500))

        automaton1Copy.__listState.extend(automaton2Copy.__listState)
        automaton1Copy.__finalStates.extend(automaton2Copy.__finalStates)
        automaton1Copy.__transitions.extend(automaton2Copy.__transitions)

        eq = automaton1Copy.equivalentsStates()

        initialStates = (int(automaton1Copy.__initialState.getId()), int(automaton2Copy.__initialState.getId()))

        if initialStates in eq:
            return True
        else:
            return False