import cv2
import subprocess
import os

class Recorder:
    
    def __init__(self, resolution):
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('output.avi', self.fourcc, 10.0, resolution)
        
    def write_image(self, image):
        self.out.write(image)
        
    def replay_video(self):
        process = subprocess.Popen(['omxplayer', os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output.avi'))])