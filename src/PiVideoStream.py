from AbstractVideoStream import AbstractVideoStream
import cv2
from threading import Thread
from picamera.array import PiRGBArray
from picamera import PiCamera

class PiVideoStream(AbstractVideoStream):
    def __init__(self, resolution=(320, 320), framerate=60):
        self.name = "Picam"
        # initialize the camera and stream
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
            format="bgr", use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.stopped = True
        
    def get_resolution(self):
        return self.camera.resolution


    def start(self):
        # start the thread to read frames from the video stream
        self.stopped = False
        t = Thread(target=self.update, args=())
        t.daemon = True
        print "Starting Camera..."
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            # and resource camera resources
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()
                return

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True