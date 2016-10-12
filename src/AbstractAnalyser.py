from abc import ABCMeta, abstractmethod

class AbstractAnalyser(object):
    __metaclass__ = ABCMeta
    
    
    @abstractmethod
    def execute(self, image):
        return image