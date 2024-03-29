import cv2
import subprocess
import os
from AbstractOutput import AbstractOutput 

class Recorder(AbstractOutput):
    
    def __init__(self, resolution, name="Recorder"):
        self.name = name
        self.description = "Writes the provided images to a video file"
        self.input = "An image to write to file"
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('output.avi', self.fourcc, 10.0, resolution)
        
    def output(self, image, info):
        self.out.write(image)
        
    def replay_video(self):
        process = subprocess.Popen(['omxplayer', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output.avi'))])