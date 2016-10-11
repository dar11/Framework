from AbstractVideoStream import AbstractVideoStream
import cv2
from threading import Thread

class WebcamVideoStream(AbstractVideoStream):
    
    def __init__(self, src=0, resolution=(320,320), framerate=32):
        self.resolution = resolution
        self.stream = cv2.VideoCapture(src)
        self.stream.set(3,resolution[0])
        self.stream.set(4,resolution[1])
        self.stream.set(5, framerate)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def get_resolution(self):
        return self.resolution

    def start(self):
        Thread(target=self.update, args=()).start()
        return self
    
    def update(self):
        while True:
            if self.stopped:
                return
            (self.grabbed, self.frame) = self.stream.read()
            
    def read(self):
        return self.frame
    
    def stop(self):
        self.stream.release()
        self.stopped = True