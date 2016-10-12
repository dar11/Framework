from PyQt4.QtGui import *
from PyQt4.QtCore import *

class ProcessItem:
    
    def __init__(self):
        self.successors = []
        

class ProcessChain(QListWidget):
    
    def __init__(self, parent):
        super(ProcessChain, self).__init__()
        self.source = None
        self.filter_count = 0
        self.filters = []
        self.analyser = []
        self.output = []
        self.parent = parent
        self.stream = None
        self.itemClicked.connect(self.removeItem)
        
    def removeItem(self, item):
        self.takeItem(self.row(item))
        self.remove(item)
        
    def setSource(self, source, stream):
        self.source = source
        self.stream = stream
        if self.count() > 0:
            self.takeItem(0)
        self.addItem(source)
        
    def addFilter(self, filter):
        if self.source == None:
            msg = QMessageBox()
            msg.setText("No Source")
            msg.setInformativeText("First item in process chain has to be a video source")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_() 
        if "Display" in self.output:
            self.insertItem(self.count()-1, filter)
            self.filters.append(filter)
            self.filter_count += 1
        else:
            self.addItem(filter)
            self.filter_count += 1
            self.filters.append(filter)
            
    def addOutput(self, output):
        if self.source == None:
            msg = QMessageBox()
            msg.setText("No Source")
            msg.setInformativeText("First item in process chain has to be a video source")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()  
        else:
            self.addItem(output)
            self.output.append(output)
    
    def remove(self, item):
        if item in self.filters:
            self.filter_count -= 1
        self.takeItem(self.row(item))
        
    def runChain(self):
        image = self.stream.read()
        for index in xrange(self.count()):
            if index == 0 or index == self.count()-1:
                continue
            image, suc = self.parent.filterBox.itemData(self.parent.filterBox.findText(self.item(index).text())).toPyObject().execute(image)
        return image        

        
        