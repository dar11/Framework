from abc import ABCMeta, abstractmethod
from PyQt4.QtGui import QMessageBox

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
    
    
    def changeParameters(self):
        msg = QMessageBox()
        msg.setText("No Parameters")
        msg.setInformativeText("There are no parameters for " + self.name + " to change")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_() 
        
    def __eq__(self, other):
        return self.name == other.name