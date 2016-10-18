from abc import ABCMeta, abstractmethod

class AbstractDevice(object):
    
    def __init__(self):
        self.ip = NotImplemented
        