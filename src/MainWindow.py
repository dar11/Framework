import sys
from PyQt4 import QtGui, QtCore
import os
import subprocess


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
        
    def classifier(self):
        images = str(QtGui.QFileDialog.getExistingDirectory(self, 'Select Images', '/home'))
        if images:
            cmd = 'python ' + str(os.getcwd()) +'/Trainer.py -t ' + images
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = p.communicate()
            print "Completed"
        
    def initUI(self):
        self.setWindowTitle("SartoCV")
        
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.delete)
        
        classifierAction = QtGui.QAction(QtGui.QIcon('ml.png'), '&Classifier', self)
        classifierAction.setShortcut('Ctrl+C')
        classifierAction.setStatusTip('New Classifier')
        classifierAction.triggered.connect(self.classifier)
        
        self.statusBar()
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        
        self.classifier_toolbar = self.addToolBar("Classifier")
        self.classifier_toolbar.addAction(classifierAction)
        
        
        #self.setGeometry(50, 50, 1200, 720)
        self.showMaximized()
        #self.show()