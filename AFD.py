from __future__ import print_function #use python3 print function
from State import * #use state object
from Transition import * #use transition
import copy #use to copy a object
import xml.etree.ElementTree as ET #XML
from Element_prettify import prettify #formate xml to print

class AFD(object):
    """
    Class that implements an automaton.
    """

    def __init__(self):
        self.__listState = []
        self.__alphabet = []
        self.__transistions = []
        self.__initalState = None
        self.__finalStates = []

    def __getInitialState(self):
        """
        get a initial state
        :return: initial state
        """
        return self.__initalState

    def addState(self, id, initial=False, final=False):
        """
        Function to add a new state in automaton
        :param id: state id (int)
        :param initial: if a state is initial (bool)
        :param final: if a state is final (bool)
        :return: if a state is create or not (bool)
        """
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

        self.__transistions.append(transition)

    def __outputList(self, state):
        listTransistion = []
        for transition in self.__transistions:
            if transition.getSource() == state:
                listTransistion.append(transition)
        return listTransistion

    def accept(self, input):
        state = self.__initalState

        for char in input:

            listTransition = self.__outputList(state)

            if char not in self.__alphabet:
                return False

            findTransition = False
            for transistion in listTransition:
                if transistion.getConsume() == char:
                    findTransition = True
                    state = transistion.getDestination()
                    break

            if findTransition == False:
                return False

        return True if state.getFinal() else False

    def __getStateById(self, stateId):
        for state in self.__listState:
            if state.getId() == stateId:
                return state

    def __createMultiplication(self, automata):
        newAutomaton = AFD()
        for stateA in self.__listState:
            for stateB in automata.__listState:
                newAutomaton.addState(stateA.getId()+"."+stateB.getId())

        for state in newAutomaton.__listState:
            statesSplit = state.getId().split(".")

            stateA = self.__getStateById(statesSplit[0])
            stateB = automata.__getStateById(statesSplit[1])

            listA = self.__outputList(stateA)
            listB = automata.__outputList(stateB)

            for char in self.__alphabet:
                stateDestination = ""
                for transitionA in listA:
                    if transitionA.getConsume() == char:
                        stateDestination += transitionA.getDestination().getId()

                stateDestination += "."

                for transitionB in listB:
                    if transitionB.getConsume() == char:
                        stateDestination += transitionB.getDestination().getId()

                if newAutomaton.__getStateById(stateDestination) == None:
                    return None

                newAutomaton.addTransition(state.getId(), stateDestination, char)

        return newAutomaton

    def intersection(self, automata):
        newAutomaton = self.__createMultiplication(automata)
        if newAutomaton == None:
            return None

        stateA = self.__getInitialState()
        stateB = automata.__getInitialState()

        initialState = newAutomaton.__getStateById(stateA.getId()+"."+stateB.getId())
        initialState.setInitial(True)
        newAutomaton.__initalState = initialState

        for stateA in self.__listState:
            for stateB in automata.__listState:
                if(stateA.getFinal() and stateB.getFinal()):
                    finalState = newAutomaton.__getStateById(stateA.getId()+"."+stateB.getId())
                    finalState.setFinal(True)
                    newAutomaton.__finalStates.append(finalState)

        return newAutomaton

    def union(self, automata):
        newAutomaton = self.__createMultiplication(automata)
        if newAutomaton == None:
            return None

        stateA = self.__getInitialState()
        stateB = automata.__getInitialState()

        initialState = newAutomaton.__getStateById(stateA.getId()+"."+stateB.getId())
        initialState.setInitial(True)
        newAutomaton.__initalState = initialState

        for stateA in self.__listState:
            for stateB in automata.__listState:
                if(stateA.getFinal() or stateB.getFinal()):
                    finalState = newAutomaton.__getStateById(stateA.getId()+"."+stateB.getId())
                    finalState.setFinal(True)
                    newAutomaton.__finalStates.append(finalState)

        return newAutomaton

    def complement(self):
        #faz a copia do objeto, nao referencia
        newAutomaton = copy.deepcopy(self)
        newAutomaton.__finalStates = []

        for state in newAutomaton.__listState:
            state.setFinal(not state.getFinal())
            if state.getFinal() == True:
                newAutomaton.__finalStates.append(state)
        return newAutomaton

    def difference(self, automata):
        automataB = automata.complement();
        return self.union(automataB)

    def load(self, name):
        try:
            # limpa o automato
            self.__listState = []
            self.__alphabet = []
            self.__transistions = []
            self.__initalState = None
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

    def salve(self, name):
        structure = ET.Element('structure')
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

        for transitions in self.__transistions:
            transition = ET.SubElement(automaton, 'transition')

            from1 = ET.SubElement(transition, 'from')
            from1.text = str(transitions.getSource())

            to = ET.SubElement(transition, 'to')
            to.text = str(transitions.getDestination())

            read = ET.SubElement(transition, 'read')
            read.text = transitions.getConsume()

        arq = open(name, 'w')
        arq.write(prettify(structure))