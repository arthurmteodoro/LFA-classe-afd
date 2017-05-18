class Equivalent(object):

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
