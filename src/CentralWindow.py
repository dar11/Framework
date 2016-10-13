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

class FrameworkCentralWidget(QtGui.QMdiArea):
    
    def __init__(self):
        super(FrameworkCentralWidget, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.fps = 10
        self.cap = None
        self.webcam = WebcamVideoStream(resolution=(320, 240), framerate=10)
        self.picam = PiVideoStream(resolution=(960, 720), framerate=10)
        self.recorder = Recorder(resolution=(960,720))
        self.timer = None
        
        control_layout = QtGui.QGridLayout()
        control_layout.setAlignment(Qt.AlignTop)
        control_subwindow = QtGui.QMdiSubWindow()
        control_subwindow.setWindowTitle("Controls")
        control_widget = QtGui.QWidget()
        control_subwindow.setWidget(control_widget)
        control_widget.setLayout(control_layout)
        
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
        
        self.inputBox = QtGui.QComboBox(self)
        self.inputBox.activated.connect(self.inputChanged)
        self.inputBox.addItem("Webcam", self.webcam)
        self.inputBox.addItem("Picam", self.picam)
        self.inputBox.addItem("Video File")
        control_layout.addWidget(self.inputBox, 0, 1)
        
        filter_label = QtGui.QLabel("Filter")
        control_layout.addWidget(filter_label, 1, 0)
        
        self.filterBox = QtGui.QComboBox(self)
        self.filterBox.activated.connect(self.filterChanged)
        control_layout.addWidget(self.filterBox, 1, 1)
        
        for m in inspect.getmembers(StandardFilter, inspect.isclass):
            if m[1].__module__ == 'StandardFilter':
                filter = m[1]()
                self.filterBox.addItem(m[0], filter)
        
        analysis_label = QtGui.QLabel("Analyser")
        control_layout.addWidget(analysis_label, 2, 0)
        
        self.analysisBox = QtGui.QComboBox(self)
        self.analysisBox.activated.connect(self.analyserChanged)
        control_layout.addWidget(self.analysisBox, 2, 1)
        
        output_label = QtGui.QLabel("Output")
        control_layout.addWidget(output_label, 3, 0)
        
        self.outputBox = QtGui.QComboBox(self)
        self.outputBox.addItem("Display")
        self.outputBox.addItem("Writer")
        self.outputBox.activated.connect(self.outputChanged)
        control_layout.addWidget(self.outputBox, 3, 1)
        
        
        stream_layout = QtGui.QVBoxLayout()
        stream_layout.setAlignment(Qt.AlignCenter)
        stream_subwindow = QtGui.QMdiSubWindow()
        stream_subwindow.setWindowTitle("Output")
        stream_widget = QtGui.QWidget()
        stream_subwindow.setWidget(stream_widget)
        stream_widget.setLayout(stream_layout)
        self.video_frame = QtGui.QLabel()
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
            self.cap = self.inputBox.itemData(index).toPyObject()
        self.chain_tab_widget.currentWidget().process_chain.setSource(self.inputBox.currentText(), self.cap)
        
    def filterChanged(self, index):
        self.chain_tab_widget.currentWidget().process_chain.addFilter(self.filterBox.currentText())
        
    def addFilter(self, filter):
        if isinstance(filter, AbstractFilter):
            self.filterBox.addItem(filter.name, filter)
        else:
            msg = QMessageBox()
            msg.setText("No Filter found")
            msg.setInformativeText("Filter is not of type AbstractFilter")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
            
    def addAnalyser(self, analyser):
        if isinstance(analyser, AbstractAnalyser):
            self.analysisBox.addItem(analyser.name, analyser)
        
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
        
    def nextFrameSlot(self):
        if self.chain_tab_widget.currentWidget().process_chain.count() == 0:
            return
        frame = self.chain_tab_widget.currentWidget().process_chain.runChain()
        write_frame = frame.copy()
        frame = cv2.resize(frame, (400, 400))
        if len(frame.shape) <= 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)

        if self.chain_tab_widget.currentWidget().process_chain.count() > 0 and self.chain_tab_widget.currentWidget().process_chain.item(self.chain_tab_widget.currentWidget().process_chain.count()-1).text() == "Display":
            self.video_frame.setPixmap(pix)
        elif self.chain_tab_widget.currentWidget().process_chain.count() > 0 and self.chain_tab_widget.currentWidget().process_chain.item(self.chain_tab_widget.currentWidget().process_chain.count()-1).text() == "Writer":
            self.recorder.write_image(write_frame)
        else:
            pass
        
