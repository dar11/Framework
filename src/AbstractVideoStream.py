from abc import ABCMeta, abstractmethod

class AbstractVideoStream(object):
    __metaclass__ = ABCMeta
    
    
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def read(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass
    
    @abstractmethod
    def get_resolution(self):
        pass