import sys
from PyQt4 import QtGui, QtCore
from WebcamVideoStream import WebcamVideoStream
import cv2
from MainWindow import FrameworkMainWindow
from CentralWindow import FrameworkCentralWidget
from MyFilter import MyEdgeFilter
from HandPre import HandPre
from Classifier import Classifier
from HandAnalyser import HandAnalyser

        
def main():
    app = QtGui.QApplication(sys.argv)
    window = FrameworkMainWindow()
    centralWidget = FrameworkCentralWidget()
    handPre = HandPre("Skin")
    cls = Classifier("Classifier")
    handAnalyser = HandAnalyser("HandAnalyser")
    centralWidget.addFilter(handPre)
    centralWidget.addAnalyser(cls)
    centralWidget.addAnalyser(handAnalyser)
    window.setCentralWidget(centralWidget)
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()