from PyQt4 import QtGui, QtCore

class ProcessListModel(QtCore.QAbstractListModel):
    
    def __init__(self, parent = None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__process = []
        
    def rowCount(self, parent):
        return len(self.__process)
    
    def data(self, index, role):
        
        if role == QtCore.Qt.UserRole:
            row = index.row()
            value = self.__process[row]
            
            return value
        
        if role == QtCore.Qt.DisplayRole:
            
            row = index.row()
            value = self.__process[row]
            
            return value.name
        
    def addItem(self, item):
        self.__process.append(item)