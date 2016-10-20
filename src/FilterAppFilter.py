from AbstractFilter import AbstractFilter
import cv2
import numpy as np

class FilterAppFilter(AbstractFilter):
    
    def __init__(self, name):
        super(FilterAppFilter, self).__init__(name)
        
    def execute(self, image, orig):
        if len(image.shape) > 2:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150, apertureSize=3, L2gradient=False)
            edges = cv2.dilate(edges, kernel, iterations=4)
            edges = cv2.erode(edges, None, iterations=4)
            return edges, orig
        else:
            return image, orig
        
    def getParameters(self):
        return ["No Parameters"]