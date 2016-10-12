
import cv2
import numpy as np
from AbstractFilter import AbstractFilter

class HandPre(AbstractFilter):
    
    def __init__(self, name):
        super(HandPre, self).__init__(name)
        self.Y_MIN = 0
        self.Y_MAX = 255
        self.Cr_MIN = 133
        self.Cr_MAX = 173
        self.Cb_MIN = 77
        self.Cb_MAX = 127
        
        self.kernel = np.ones((1,3), np.uint8)
    
    def execute(self, image):
        image = cv2.flip(image, 1)
        
        frameYCrCb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
        for i in range(5):
            skin = cv2.bilateralFilter(frameYCrCb, 3, 9, 9)
            i += 1
        skin = cv2.inRange(frameYCrCb, np.array([self.Y_MIN, self.Cr_MIN, self.Cb_MIN]), np.array([self.Y_MAX, self.Cr_MAX, self.Cb_MAX]))
        for i in range(5):
            skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, self.kernel)
            i += 1
        skin = cv2.morphologyEx(skin, cv2.MORPH_CLOSE, self.kernel)
        skin = cv2.medianBlur(skin, 11)
        return skin, True