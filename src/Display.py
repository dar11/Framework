import cv2
import subprocess
import os
from AbstractOutput import AbstractOutput 
from PyQt4 import QtGui

class Display(AbstractOutput):
    
    def __init__(self, parent, name="Display"):
        self.name = name
        self.description = "Displays the provided Image in the Screen"
        self.input = "An image to be displayed"
        self.parent = parent
        
    def output(self, frame, info):
        frame = cv2.resize(frame, (640, 480))
        if len(frame.shape) <= 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.parent.video_frame.setPixmap(pix)