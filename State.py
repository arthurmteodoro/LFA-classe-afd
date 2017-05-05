class State(object):

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