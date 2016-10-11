import cv2
import numpy as np
from AbstractFilter import AbstractFilter

class MyEdgeFilter(AbstractFilter):

    def execute(self, image):
        image = cv2.Canny(image, 50, 100)
        return image, True
    
class MyEdgeFilter2(AbstractFilter):
        
    def execute(self, image):
        image = cv2.Canny(image, 100, 200)
        return image, True
    
class FilterAppEdgeFilter(AbstractFilter):
    
    def execute(self, image):
        if len(image.shape) > 2:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150, apertureSize=3, L2gradient=False)
            edges = cv2.dilate(edges, kernel, iterations=4)
            edges = cv2.erode(edges, None, iterations=4)
            return edges, True
        else:
            return image, False