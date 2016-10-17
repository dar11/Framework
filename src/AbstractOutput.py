from abc import ABCMeta, abstractmethod

class AbstractOutput(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, name):
        self.name = name
        
    @abstractmethod
    def output(self, image):
        pass