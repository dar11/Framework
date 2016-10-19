from PyQt4 import QtGui, QtCore

class InputListModel(QtCore.QAbstractListModel):
    
    def __init__(self, inputs = [], parent = None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__inputs = inputs
        
    def rowCount(self, parent):
        return len(self.__inputs)
    
    def data(self, index, role):
        
        if role == QtCore.Qt.UserRole:
            row = index.row()
            value = self.__inputs[row]
            
            return value
        
        if role == QtCore.Qt.DisplayRole:
            
            row = index.row()
            value = self.__inputs[row]
            
            return value.name