from abc import ABCMeta, abstractmethod

class AbstractAnalyser(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def analyse(self, image, orig):
        return image, orig