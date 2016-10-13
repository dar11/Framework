import cv2
import numpy as np
from AbstractFilter import AbstractFilter

class EdgeFilter(AbstractFilter):
    
    def __init__(self):
        self.name = "EdgeFilter"
    
    def execute(self, image, orig):
        image = cv2.Canny(image, 100, 200)
        return image, orig
    
    def getParameters(self):
        return ["No Parameters"]
    
class HSVFilter(AbstractFilter):
    
    def __init__(self):
        self.name = "HSVFilter"
        
    def execute(self, image, orig):
        if len(image.shape) > 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            return image, orig
        else:
            print "You cant convert a binary image into HSV color space."
            return image, orig
    
    def getParameters(self):
        return ["No Parameters"]
    
class GrayFilter(AbstractFilter):
    
    def __init__(self):
        self.name = "GrayFilter"
        
    def execute(self, image, orig):
        if len(image.shape) > 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return image, orig
        else:
            print "You cant convert a binary image into gray color space."
            return image, orig
        
    def getParameters(self):
        return ["No Parameters"]
    
class YCrCbFilter(AbstractFilter):
    
    def __init__(self):
        self.name = "YCrCbFilter"
        
    def execute(self, image, orig):
        if len(image.shape) > 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
            return image, orig
        else:
            print "You cant convert a binary image into YCrCb color space."
            return image, orig
        
    def getParameters(self):
        return ["No Parameters"]
    
class MinEnclosing(AbstractFilter):
    
    def __init__(self):
        self.name = "MinEnclosing"
        self.center = (0,0)
        self.radius = 0
    
    def execute(self, image, orig):
        temp_cont = image.copy()
        cont_image, contours, hierarchy = cv2.findContours(temp_cont, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return image, orig
        contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(contour)
        self.center = (int(x), int(y))
        self.radius = int(radius)
        cv2.circle(orig, (int(x), int(y)), int(radius), (0,255,0), 1)
        return image, orig
    
    def getParameters(self):
        return ["Center of Circle: " + str(self.center), "Radius of Circle: " + str(self.radius)]
    
class ConvexHull(AbstractFilter):
    
    def __init__(self):
        self.name = "ConvexHull"
        
    def execute(self, image, orig):
        temp_cont = image.copy()
        cont_image, contours, hierarchy = cv2.findContours(temp_cont, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return image, orig
        contour = max(contours, key=cv2.contourArea)
        hull = cv2.convexHull(contour)
        hull = np.array(hull).reshape((-1,1,2)).astype(np.int32)
        cv2.drawContours(orig, [hull], 0, (0,255,0), 1)
        return image, orig
    
    def getParameters(self):
        return ["No Parameters"]
        