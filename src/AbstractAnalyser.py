from abc import ABCMeta, abstractmethod

class AbstractAnalyser(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, name):
        self.name = name
        self.description = "Not specified"
        self.input = "Not specified"
        self.output = "Not specified"
    
    @abstractmethod
    def analyse(self, image, orig):
        return image, orig, None