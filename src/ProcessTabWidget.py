from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ProcessChain import ProcessChain
from PyQt4 import QtGui, QtCore

class ProcessTabWidget(QWidget):
    
    def __init__(self, parent):
        super(ProcessTabWidget, self).__init__()
        self.process_chain = ProcessChain(parent)
        self.process_chain.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        