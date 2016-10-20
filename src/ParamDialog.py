from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore


class ParamDialog(QDialog):
    
    def __init__(self):
        super(ParamDialog, self).__init__()
        
        firstLabel = QtGui.QLabel("First Threshold")
        secondLabel = QtGui.QLabel("Second Threshold")
        self.firstEdit = QtGui.QLineEdit()
        self.secondEdit = QtGui.QLineEdit()
        ok_button = QtGui.QPushButton("Apply")
        layout = QtGui.QGridLayout()
        layout.addWidget(firstLabel, 0, 0)
        layout.addWidget(secondLabel, 1, 0)
        layout.addWidget(self.firstEdit, 0, 1)
        layout.addWidget(self.secondEdit, 1, 1)
        layout.addWidget(ok_button, 2, 0)
        self.setLayout(layout)
        
        self.first = None
        self.second = None
        
        ok_button.clicked.connect(self.change)
        
    def change(self):
        self.first = int(self.firstEdit.text())
        self.second = int(self.secondEdit.text())
        self.accept()
        
    def returnParams(self):
        return self.first, self.second
        