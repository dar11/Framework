from AbstractVideoStream import AbstractVideoStream
import cv2
from threading import Thread

class FileVideoStream(AbstractVideoStream):
    
    def __init__(self, path):
        self.stream = cv2.VideoCapture(path)
        
        
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

    def get_resolution(self):
        pass