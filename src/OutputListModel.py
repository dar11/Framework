from PyQt4 import QtGui, QtCore

class OutputListModel(QtCore.QAbstractListModel):
    
    def __init__(self, output = [], parent = None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__output = output
        
    def rowCount(self, parent):
        return len(self.__output)
    
    def data(self, index, role):
        
        if role == QtCore.Qt.UserRole:
            row = index.row()
            value = self.__output[row]
            
            return value
        
        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            value = self.__output[row]
            tooltip = "Name: " + value.name + "\nDescription: " + value.description + "\nInput: " + value.input
            
            return tooltip
        
        if role == QtCore.Qt.DisplayRole:
            
            row = index.row()
            value = self.__output[row]
            
            return value.name