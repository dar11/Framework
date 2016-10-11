import cv2
import numpy as np
from AbstractFilter import AbstractFilter

class EdgeFilter(AbstractFilter):
    
    def __init__(self):
        self.name = "EdgeFilter"
    
    def execute(self, image):
        image = cv2.Canny(image, 100, 200)
        return image, True
    
class HSVFilter(AbstractFilter):
    
    def __init__(self):
        self.name = "HSVFilter"
        
    def execute(self, image):
        if len(image.shape) > 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            return image, True
        else:
            print "You cant convert a binary image into HSV color space."
            return image, False
    
class GrayFilter(AbstractFilter):
    
    def __init__(self):
        self.name = "GrayFilter"
        
    def execute(self, image):
        if len(image.shape) > 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return image, True
        else:
            print "You cant convert a binary image into gray color space."
            return image, False
    
class YCrCbFilter(AbstractFilter):
    
    def __init__(self):
        self.name = "YCrCbFilter"
        
    def execute(self, image):
        if len(image.shape) > 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
            return image, True
        else:
            print "You cant convert a binary image into YCrCb color space."
            return image, False