from __future__ import print_function #utilizar o print como python 3
from State import * #usar o objeto estado
from Transition import * #usar o objeto transasao
import copy #usada para copiar o objeto
import xml.etree.ElementTree as ET #XML
from Element_prettify import prettify #formatar xml para salvar

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

    def union(self, automata):
        newAutomata = self.__createMultiplication__(automata)
        stateA = self.getInitialState()
        stateB = automata.getInitialState()

        initialState = newAutomata.getStateById(stateA.getId()+"."+stateB.getId())
        initialState.setInitial(True)
        newAutomata.__initalState = initialState

        for stateA in self.__listState:
            for stateB in automata.__listState:
                if(stateA.getFinal() or stateB.getFinal()):
                    finalState = newAutomata.getStateById(stateA.getId()+"."+stateB.getId())
                    finalState.setFinal(True)
                    newAutomata.__finalStates.append(finalState)

        return newAutomata

    def complement(self):
        #faz a copia do objeto, nao referencia
        newAutomata = copy.deepcopy(self)
        newAutomata.__finalStates = []

        for state in newAutomata.__listState:
            state.setFinal(not state.getFinal())
            if state.getFinal() == True:
                newAutomata.__finalStates.append(state)
        return newAutomata

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

        print(prettify(structure))

        arq = open(name, 'w')
        arq.write(prettify(structure))