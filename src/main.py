import sys
from PyQt4 import QtGui, QtCore
from WebcamVideoStream import WebcamVideoStream
import cv2
from MainWindow import FrameworkMainWindow
from CentralWindow import FrameworkCentralWidget
from MyFilter import MyEdgeFilter

        
def main():
    app = QtGui.QApplication(sys.argv)
    window = FrameworkMainWindow()
    centralWidget = FrameworkCentralWidget()
    myEdgeFilter = MyEdgeFilter("MyEdgeFilter")
    centralWidget.addFilter(myEdgeFilter)
    window.setCentralWidget(centralWidget)
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()