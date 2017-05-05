class Transition(object):

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
