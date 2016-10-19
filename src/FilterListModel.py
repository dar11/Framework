from PyQt4 import QtGui, QtCore

class FilterListModel(QtCore.QAbstractListModel):
    
    def __init__(self, filter = [], parent = None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__filter = filter
        
    def rowCount(self, parent):
        return len(self.__filter)
    
    def data(self, index, role):
        
        if role == QtCore.Qt.UserRole:
            row = index.row()
            value = self.__filter[row]
            
            return value
        
        if role == QtCore.Qt.ToolTipRole:
            row = index.row()
            value = self.__filter[row]
            
            return value.name
        
        if role == QtCore.Qt.DisplayRole:
            
            row = index.row()
            value = self.__filter[row]
            
            return value.name
        
    def addFilter(self, filter):
        self.__filter.append(filter)