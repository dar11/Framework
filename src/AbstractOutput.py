from abc import ABCMeta, abstractmethod

class AbstractOutput(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, name):
        self.name = name
        self.description = "Not specified"
        self.input = "Not specified"
        
    @abstractmethod
    def output(self, image, info):
        pass