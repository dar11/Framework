from AbstractVideoStream import AbstractVideoStream
import cv2
from threading import Thread
import time

class WebcamVideoStream(AbstractVideoStream):
    
    def __init__(self, src=0, resolution=(320,320), framerate=32):
        self.resolution = resolution
        self.framerate = framerate
        self.src = src
        self.stream = None
        #self.stream = cv2.VideoCapture(src)
        #self.stream.set(3,resolution[0])
        #self.stream.set(4,resolution[1])
        #self.stream.set(5, framerate)
        #(self.grabbed, self.frame) = self.stream.read()
        self.stopped = True

    def get_resolution(self):
        return self.resolution

    def start(self):
        self.stream = cv2.VideoCapture(self.src)
        self.stream.set(3,self.resolution[0])
        self.stream.set(4,self.resolution[1])
        self.stream.set(5, self.framerate)
        self.stopped = False
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        while not self.stopped:
            (self.grabbed, self.frame) = self.stream.read()
            
    def read(self):
        return self.frame
    
    def stop(self):
        #print "Closing Webcam"
        if self.stream is not None:
            self.stream.release()
        self.stopped = True