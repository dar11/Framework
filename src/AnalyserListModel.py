from PyQt4 import QtGui, QtCore

class AnalyserListModel(QtCore.QAbstractListModel):
    
    def __init__(self, analyser = [], parent = None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__analyser = analyser
        
    def rowCount(self, parent):
        return len(self.__analyser)
    
    def data(self, index, role):
        
        if role == QtCore.Qt.UserRole:
            row = index.row()
            value = self.__analyser[row]
            
            return value
        
        if role == QtCore.Qt.DisplayRole:
            
            row = index.row()
            value = self.__analyser[row]
            
            return value.name
        
    def addAnalyser(self, analyser):
        self.__analyser.append(analyser)