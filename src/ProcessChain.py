from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtCore
from PyQt4 import QtGui
import time
import cv2
from ProcessListModel import ProcessListModel

class ProcessItem:
    
    def __init__(self):
        self.successors = []
        

#class ProcessChain(QListWidget):
class ProcessChain(QListWidget):
    
    def __init__(self, parent):
        super(ProcessChain, self).__init__()
        #self.model = ProcessListModel()
        #self.setModel(self.model)
        self.source = None
        self.filter_count = 0
        self.output_count = 0
        self.filters = []
        self.analyser = []
        self.output = []
        self.parent = parent
        self.stream = None
        self.itemClicked.connect(self.showParameters)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self, QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.removeItem)
        
    #def dragEnterEvent(self, event):
    #    event.accept()
        
    #def dropEvent(self, event):
        #print event.mimeData().text()
    #    event.accept()
        
    #def addItem(self, item):
    #    self.model.addItem(item)
        
    def showParameters(self, item):
        self.parent.showParameters()
        
    def removeItem(self, QPos):
        self.listMenu = QtGui.QMenu()
        menu_item = self.listMenu.addAction("Remove")
        self.listMenu.connect(menu_item, QtCore.SIGNAL("triggered()"), self.remove)
        parentPosition = self.mapToGlobal(QtCore.QPoint(0, 0))        
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show() 
        
    def remove(self):
        currentItem = self.currentItem()
        currentName = self.currentItem().text()
        if currentName in self.filters:
            self.filter_count -= 1
            self.filters.remove(currentName)
        elif currentName in self.output:
            self.output.remove(currentName)
            self.output_count -= 1
        elif currentName in self.analyser:
            self.analyser.remove(currentName)
        self.takeItem(self.row(currentItem))

        
    def setSource(self, source, stream):
        self.source = source
        self.stream = stream
        if self.count() > 0:
            self.takeItem(0)
        self.insertItem(0, source)
        
    def addFilter(self, filter):
        if self.source == None:
            msg = QMessageBox()
            msg.setText("No Source")
            msg.setInformativeText("First item in process chain has to be a video source")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_() 
        if len(self.output) > 0:
            self.insertItem(self.count()-1, filter)
            self.filters.append(filter)
            self.filter_count += 1
        else:
            self.addItem(filter)
            self.filter_count += 1
            self.filters.append(filter)
            
    def addAnalyser(self, analyser):
        if self.source == None:
            msg = QMessageBox()
            msg.setText("No Source")
            msg.setInformativeText("First item in process chain has to be a video source")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_() 
        if len(self.output) > 0:
            self.insertItem(self.count()-1, analyser)
            self.analyser.append(analyser)
        else:
            self.addItem(analyser)
            self.analyser.append(analyser)
            
    def addOutput(self, output):
        if self.source == None:
            msg = QMessageBox()
            msg.setText("No Source")
            msg.setInformativeText("First item in process chain has to be a video source")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()  
        else:
            self.addItem(output)
            self.output_count += 1
            self.output.append(output)
    

        
    def stop(self):
        time.sleep(1)
        
    def runChain(self):
        if self.stream is None:
            return
        if self.stream.stopped:
            self.stream.start()
            time.sleep(2)
        image = self.stream.read()
        image = cv2.flip(image, 1)
        orig = image.copy()
        info = None
        for index in xrange(self.count()):
            if index == 0:
                continue
            if index <= self.filter_count:
                image, orig = self.parent.filterBox.itemData(self.parent.filterBox.findText(self.item(index).text())).toPyObject().execute(image, orig)
            if index > self.filter_count and index < self.count() - self.output_count:
                image, orig, info = self.parent.analysisBox.itemData(self.parent.analysisBox.findText(self.item(index).text())).toPyObject().analyse(image, orig)
            if index >= self.count()-self.output_count:
                if self.parent.show_image:
                    image = image
                else:
                    image = orig
                self.parent.outputBox.itemData(self.parent.outputBox.findText(self.item(index).text())).toPyObject().output(image, info)
        return image, orig        

        
        