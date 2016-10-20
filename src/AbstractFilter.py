from abc import ABCMeta, abstractmethod

class AbstractFilter(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, name):
        self.name = name
        self.description = "Not specified"
        self.input = "Not specified"
        self.output = "Not specified"
    
    @abstractmethod
    def execute(self, image, orig):
        return image, orig
    
    @abstractmethod
    def getParameters(self):
        pass
    
    def register(self, parent):
        parent.gui.append_filter(self)
        
    def register_and_activate(self, parent):
        parent.gui.append_filter(self)
        parent.gui.activate_filter(self)
        parent.register_filter(self)
        
    def __eq__(self, other):
        return self.name == other.name