from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui, QtCore


class ParamDialog(QDialog):
    
    def __init__(self, *arg):
        super(ParamDialog, self).__init__()
        self.lineEdits = []
        
        ok_button = QtGui.QPushButton("Apply")
        cancel_button = QtGui.QPushButton("Cancel")
        layout = QtGui.QGridLayout()
        i = 0
        for a in arg:
            label = QtGui.QLabel(a)
            lineEdit = QtGui.QLineEdit()
            lineEdit.setPlaceholderText("0")
            self.lineEdits.append(lineEdit)
            layout.addWidget(label, i, 0)
            layout.addWidget(lineEdit, i, 1)
            i += 1

        layout.addWidget(ok_button, i, 0)
        layout.addWidget(cancel_button, i , 1)
        self.setLayout(layout)
        
        self.returns = []
        self.setWindowTitle("Change Parameter")
        
        ok_button.clicked.connect(self.change)
        cancel_button.clicked.connect(self.cancel)
        
    def cancel(self):
        self.reject()
        
    def change(self):
        for edit in self.lineEdits:
            self.returns.append(int(edit.text()))
        self.accept()
        
    def returnParams(self):
        return self.returns
        