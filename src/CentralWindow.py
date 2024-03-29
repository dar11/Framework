import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from WebcamVideoStream import WebcamVideoStream
from AbstractVideoStream import AbstractVideoStream
from AbstractFilter import AbstractFilter
from AbstractAnalyser import AbstractAnalyser
from PiVideoStream import PiVideoStream
from FileVideoStream import FileVideoStream
import cv2
import time
import StandardFilter
import inspect
from Recording import Recorder
from ProcessChain import ProcessChain
from ProcessTabWidget import ProcessTabWidget
from AbstractOutput import AbstractOutput
from Display import Display
from GestureToCubis import GestureToCubis
from InputListModel import InputListModel
from FilterListModel import FilterListModel
from AnalyserListModel import AnalyserListModel
from OutputListModel import OutputListModel
from Classifier import Classifier

class FrameworkCentralWidget(QtGui.QMdiArea):
    
    def __init__(self):
        super(FrameworkCentralWidget, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.fps = 10
        self.cap = None
        self.webcam = WebcamVideoStream(resolution=(960, 720), framerate=10)
        self.picam = PiVideoStream(resolution=(960, 720), framerate=10)
        self.recorder = Recorder(resolution=(960,720))
        self.timer = None
        self.show_image = True
        
        control_layout = QtGui.QGridLayout()
        control_layout.setAlignment(Qt.AlignTop)
        control_subwindow = QtGui.QMdiSubWindow()
        control_subwindow.setWindowTitle("Controls")
        control_widget = QtGui.QWidget()
        control_subwindow.setWidget(control_widget)
        control_widget.setLayout(control_layout)
        
        self.parameter_label = QtGui.QLabel()
        control_layout.addWidget(self.parameter_label, 7, 0)
        
        self.show_image_button = QtGui.QRadioButton("Show Image")
        self.show_image_button.setChecked(True)
        self.show_image_button.toggled.connect(lambda:self.changeImage(self.show_image_button))
        control_layout.addWidget(self.show_image_button, 6, 0)
        
        self.show_orig_button = QtGui.QRadioButton("Show Original")
        self.show_orig_button.toggled.connect(lambda:self.changeImage(self.show_orig_button))
        control_layout.addWidget(self.show_orig_button, 6, 1)
        
        start_button = QtGui.QPushButton("Start")
        start_button.clicked.connect(self.start)
        start_button.setStyleSheet("background-color: rgb(242, 189, 12)")
        control_layout.addWidget(start_button, 4, 0)
        
        add_tab_button = QtGui.QPushButton("Add Process Chain")
        add_tab_button.clicked.connect(self.addChain)
        add_tab_button.setStyleSheet("background-color: rgb(242, 189, 12)")
        control_layout.addWidget(add_tab_button, 5, 0)
        
        stop_button = QtGui.QPushButton("Stop")
        stop_button.clicked.connect(self.stop)
        stop_button.setStyleSheet("background-color: rgb(242, 189, 12)")
        control_layout.addWidget(stop_button, 4, 1)
        
        source_label = QtGui.QLabel("Input")
        control_layout.addWidget(source_label, 0, 0)
        
        self.inputModel = InputListModel([self.webcam, self.picam])
        
        self.inputBox = QtGui.QComboBox(self)
        self.inputBox.activated.connect(self.inputChanged)
        #self.inputBox.addItem("Webcam", self.webcam)
        #self.inputBox.addItem("Picam", self.picam)
        #self.inputBox.addItem("Video File")
        self.inputBox.setModel(self.inputModel)
        control_layout.addWidget(self.inputBox, 0, 1)
        
        filter_label = QtGui.QLabel("Filter")
        control_layout.addWidget(filter_label, 1, 0)
        
        
        self.filterBox = QtGui.QComboBox(self)
        #self.filterBox.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.filterBox.customContextMenuRequested.connect(self.showMenu)
        self.filterBox.activated.connect(self.filterChanged)
        control_layout.addWidget(self.filterBox, 1, 1)
        filterList = []
        for m in inspect.getmembers(StandardFilter, inspect.isclass):
            if m[1].__module__ == 'StandardFilter':
                filter = m[1]()
                #self.filterBox.addItem(m[0], filter)
                filterList.append(filter)
                
        self.filterModel = FilterListModel(filterList)
        self.filterBox.setModel(self.filterModel)
        
        self.analyserModel = AnalyserListModel([Classifier("Classifier")])
        
        analysis_label = QtGui.QLabel("Analyser")
        control_layout.addWidget(analysis_label, 2, 0)
        
        self.analysisBox = QtGui.QComboBox(self)
        self.analysisBox.activated.connect(self.analyserChanged)
        control_layout.addWidget(self.analysisBox, 2, 1)
        self.analysisBox.setModel(self.analyserModel)
        
        output_label = QtGui.QLabel("Output")
        control_layout.addWidget(output_label, 3, 0)
        
        self.outputModel = OutputListModel([Display(self), Recorder(resolution=(960,720)), GestureToCubis()])
        
        self.outputBox = QtGui.QComboBox(self)
        #self.outputBox.addItem("Display", Display(self))
        #self.outputBox.addItem("Writer", Recorder(resolution=(960,720)))
        #self.outputBox.addItem("GestureToCubis", GestureToCubis())
        self.outputBox.activated.connect(self.outputChanged)
        
        self.outputBox.setModel(self.outputModel)
        control_layout.addWidget(self.outputBox, 3, 1)
        
        
        stream_layout = QtGui.QVBoxLayout()
        stream_layout.setAlignment(Qt.AlignCenter)
        stream_subwindow = QtGui.QMdiSubWindow()
        stream_subwindow.setWindowTitle("Output")
        stream_widget = QtGui.QWidget()
        stream_subwindow.setWidget(stream_widget)
        stream_widget.setLayout(stream_layout)
        self.video_frame = QtGui.QLabel()
        self.video_frame.setScaledContents(True)
        stream_layout.addWidget(self.video_frame)
        self.video_frame_2 = QtGui.QLabel()
        stream_layout.addWidget(self.video_frame_2)
        self.video_frame_3 = QtGui.QLabel()
        stream_layout.addWidget(self.video_frame_3)
        
        self.chain_tab_widget = QtGui.QTabWidget()
        chain_layout = QtGui.QVBoxLayout()
        chain_subwindow = QtGui.QMdiSubWindow()
        chain_subwindow.setWindowTitle("Process Chain")
        chain_widget = ProcessTabWidget(self)
        chain_widget.setLayout(chain_layout)
        chain_subwindow.setWidget(self.chain_tab_widget)
        self.chain_tab_widget.addTab(chain_widget, "Default")
        chain_layout.addWidget(chain_widget.process_chain)
        
        self.addSubWindow(chain_subwindow)
        self.addSubWindow(control_subwindow)
        self.addSubWindow(stream_subwindow)
        
        stream_subwindow.show()
        chain_subwindow.show()
        control_subwindow.show()
        self.tileSubWindows()
        
    def showMenu(self, QPos):
        #menu = QtGui.QMenu()
        #param_action = menu.addAction("Change Parameters")
        #action = menu.exec_(self.mapToGlobal(pos))
        #if action == param_action:
        #    print self.filterBox.currentText()
            
        self.filterMenu = QtGui.QMenu()
        param_item = self.filterMenu.addAction("Change Parameter")
        self.filterMenu.connect(param_item, QtCore.SIGNAL("triggered()"), self.changeParameter)
        parentPosition = self.mapToGlobal(QtCore.QPoint(0, 0))        
        self.filterMenu.move(parentPosition + QPos)
        self.filterMenu.show()
        
    def changeParameter(self):
        print "Change Parameter" 
        
    def changeImage(self, b):
        if b.text() == "Show Image":
            self.show_image = True
        elif b.text() == "Show Original":
            self.show_image = False
        
    def addChain(self):
        text, ok = QInputDialog.getText(self, 'Enter Process Name', 'Please enter a name for the process chain!')
        new_tab = ProcessTabWidget(self)
        new_layout = QtGui.QVBoxLayout()
        new_tab.setLayout(new_layout)
        self.chain_tab_widget.addTab(new_tab, text)
        new_layout.addWidget(new_tab.process_chain)
           
    def inputChanged(self, index):
        if self.inputBox.currentText() == "Video File":
            path = QtGui.QFileDialog.getOpenFileName(self, 'Open Fle', '/home')
            self.cap = FileVideoStream(str(path))
        else:
            print self.inputModel.index(index).data(role=QtCore.Qt.UserRole).toPyObject()
            #self.cap = self.inputBox.itemData(index).toPyObject()
            self.cap = self.inputModel.index(index).data(role=QtCore.Qt.UserRole).toPyObject()
        self.chain_tab_widget.currentWidget().process_chain.setSource(self.inputBox.currentText(), self.cap)
        #self.chain_tab_widget.currentWidget().process_chain.addItem(self.cap)
        
    def filterChanged(self, index):
        self.chain_tab_widget.currentWidget().process_chain.addFilter(self.filterBox.currentText())
        
    def addFilter(self, filter):
        if isinstance(filter, AbstractFilter):
            #self.filterBox.addItem(filter.name, filter)
            self.filterModel.addFilter(filter)
        else:
            msg = QMessageBox()
            msg.setText("No Filter found")
            msg.setInformativeText("Filter is not of type AbstractFilter")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
            
    def addAnalyser(self, analyser):
        if isinstance(analyser, AbstractAnalyser):
            #self.analysisBox.addItem(analyser.name, analyser)
            self.analyserModel.addAnalyser(analyser)
        
    def analyserChanged(self, index):
        self.chain_tab_widget.currentWidget().process_chain.addAnalyser(self.analysisBox.currentText())
        
    def outputChanged(self, index):
        self.chain_tab_widget.currentWidget().process_chain.addOutput(self.outputBox.currentText())
        
    def start(self):
        if self.chain_tab_widget.currentWidget().process_chain.count() == 0:
            msg = QMessageBox()
            msg.setText("No processing steps")
            msg.setInformativeText("You have at least to set an input")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
        elif isinstance(self.inputBox.itemData(self.inputBox.findText(self.chain_tab_widget.currentWidget().process_chain.item(0).text())).toPyObject(), AbstractVideoStream):
            time.sleep(2)
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.nextFrameSlot)
            self.timer.start(1000./self.fps)
            self.video_frame.show()
        elif not isinstance(self.inputBox.itemData(self.inputBox.findText(self.chain_tab_widget.currentWidget().process_chain.item(0).text())).toPyObject(), AbstractVideoStream):
            msg = QMessageBox()
            msg.setText("No Source")
            msg.setInformativeText("First item in process chain has to be a video source")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()    
        
    def stop(self):
        if self.timer:
            self.timer.stop()
            self.chain_tab_widget.currentWidget().process_chain.stop()
            self.video_frame.hide()
        else:
            pass
        
    def showParameters(self):
        filter = self.filterBox.itemData(self.filterBox.findText(self.chain_tab_widget.currentWidget().process_chain.currentItem().text())).toPyObject()
        if isinstance(filter, AbstractFilter):
            parameters = filter.getParameters()
            self.parameter_label.setText("Parameters:\n")
            for param in parameters:
                text = self.parameter_label.text()
                text.append(param + "\n")
                self.parameter_label.setText(text)
        
        
    def nextFrameSlot(self):
        if self.chain_tab_widget.currentWidget().process_chain.count() == 0:
            return
        frame, orig = self.chain_tab_widget.currentWidget().process_chain.runChain()
        write_frame = frame.copy()
        
