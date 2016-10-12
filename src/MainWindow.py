import sys
from PyQt4 import QtGui, QtCore
import os


class FrameworkMainWindow(QtGui.QMainWindow):
    def __init__(self):
        
        super(FrameworkMainWindow, self).__init__()
        self.initUI()
        
    def delete(self):
        choice = QtGui.QMessageBox.question(self, 'Exit!',
                                            "Exit Application?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Exit")
            os._exit(0)
        else:
            pass
        
    def initUI(self):
        self.setWindowTitle("SartoCV")
        
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.delete)
        
        self.statusBar()
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        
        
        self.setGeometry(50, 50, 1200, 720)
        self.show()