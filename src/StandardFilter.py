import cv2
import numpy as np
from AbstractFilter import AbstractFilter
from PyQt4 import QtGui
import math

class EdgeFilter(AbstractFilter):
    
    def __init__(self):
        self.name = "EdgeFilter"
        self.description = "Performs an edge detection on the input image."
        self.input = "Two images of any format."
        self.output = "Returns a binary image and the original image."
        self.first = 100
        self.second = 200
    
    def execute(self, image, orig):
        image = cv2.Canny(image, self.first, self.second)
        return image, orig
    
    def getParameters(self):
        return ["No Parameters"]
    
class HSVFilter(AbstractFilter):
    
    def __init__(self):
        self.name = "HSVFilter"
        self.description = "Performs a color space transformation into the HSV space."
        self.input = "Input image of any format with three channels."
        self.output = "Returns the image in HSV color space and the original image."
        
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
        self.description = "Converts the input image into grayscale."
        self.input = "Input image of any format with three channels."
        self.output = "Returns the image in grayscale format and the original image."
        
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
        self.description = "Performs a color space transformation into the YCrCb space."
        self.input = "Input image of any format with three channels."
        self.output = "Returns the image in YCrCb color space and the original image."
        
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
        self.description = "Calculates the minimum enclosing circle of the maximum contour of the input image."
        self.input = "Binary and original image"
        self.output = "Returns the binary input image and the original image with the minimum enclosing circle drawn on it."
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
        self.description = "Calculates the convex hull of the maximum contour of the input image."
        self.input = "Binary and original image"
        self.output = "Returns the binary input image and the original image with the convex hull drawn on it."
        
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
    
class MaxInscribed(AbstractFilter):
    
    def __init__(self):
        self.name = "MaxInscribed"
        self.description = "Calculates the maximum inscribed circle of the maximum contour of the input image."
        self.input = "Binary and original image"
        self.output = "Returns the binary input image and the original image with the maximum inscribed circle drawn on it."
        self.max_inscribed_center = (0,0)
        self.max_inscribed_radius = 0
        
    def execute(self, image, orig):
        temp_cont = image.copy()
        cont_image, contours, hierarchy = cv2.findContours(temp_cont, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return image, orig
        contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(contour)
        rows, cols = image.shape[:2]
        distance = -1
        maxDistance = -1
        center = None
        if (cv2.contourArea(contour) > 5000):
            for i in xrange(x, x+w, 10):
                for j in xrange(y, y+h, 10):
                    distance = cv2.pointPolygonTest(contour, (i,j), True)
                    if distance > maxDistance:
                        maxDistance = distance
                        center = (i,j)
                        
            maxDistance = int(maxDistance)
            self.max_inscribed_center = center
            self.max_inscribed_radius = maxDistance
            
        cv2.circle(orig, self.max_inscribed_center, self.max_inscribed_radius, (0,0,0), 1)
        return image, orig
    
    def getParameters(self):
        return ["Center of Circle: " + str(self.max_inscribed_center), "Radius of Circle: " + str(self.max_inscribed_radius)]
    
class ColorFilter(AbstractFilter):
    
    def __init__(self):
        self.name = "Color Filter"
        self.description = "Lets the user select a color range the input image will filtered based on."
        self.input = "Input image of any format with three channels."
        self.output = "Returns a binary image with the specified colors displayed as white and everything else as black and the original image."
        self.lowerColorPicked = False
        self.upperColorPicked = False
        self.lowerColor = None
        self.upperColor = None
        
    def execute(self, image, orig):
        if not self.lowerColorPicked:
            color = QtGui.QColorDialog.getColor()
            hsv = color.getHsv()
            print hsv
            self.lowerColor = np.array([hsv[0], hsv[1], hsv[2]])
            self.lowerColorPicked = True
        if not self.upperColorPicked:
            color = QtGui.QColorDialog.getColor()
            hsv = color.getHsv()
            self.upperColor = np.array([hsv[0], hsv[1], hsv[2]])
            self.upperColorPicked = True

        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        image = cv2.inRange(image, self.lowerColor, self.upperColor)

        return image, orig
    
    def getParameters(self):
        return ["Lower Color Values: " + str(self.lowerColor), "Upper Color Values: " + str(self.upperColor)]
    
class Defects(AbstractFilter):
    
    def __init__(self):
        self.name = "Defects"
        self.description = "Calculates the defects of the maximum contour of the input image."
        self.input = "Binary and original image"
        self.output = "Returns the binary input image and the original image with the defects drawn on it."
        
    def execute(self, image, orig):
        temp_cont = image.copy()
        cont_image, contours, hierarchy = cv2.findContours(temp_cont, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            return image, orig
        contour = max(contours, key=cv2.contourArea)
        hull = cv2.convexHull(contour, returnPoints=False)
        if hull is not None and len(hull) > 3 and len(contour) > 3:
            defects = cv2.convexityDefects(contour, hull)
        else:
            return image, orig
        count_defects = 0
        if contour.size > 100:
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(contour[s][0])
                end = tuple(contour[e][0])
                far = tuple(contour[f][0])
                extLeft = tuple(contour[contour[:,:,0].argmin()][0])
                cv2.circle(orig, extLeft, 5, (96,245,221), 1)
                
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = math.acos((b ** 2 + c ** 2 - a**2) / (2 * b * c)) * 57
                
                distSE = math.sqrt(((end[0] - start[0]) **2) + ((end[1] - start[1]) ** 2))
                distSF = math.sqrt(((start[0] - far[0]) ** 2) + ((start[1] - far[1]) ** 2))
                
                if angle < 80 and distSE > 20 and distSF > 30:
                    count_defects += 1
                    cv2.circle(orig, far, 2, (0,0,255), 1)
                    cv2.line(orig, start, end, (0,127,127), 1)
                    cv2.circle(orig, start, 5, (96,245,221), 1)
                    
        if count_defects == 0:
            cv2.putText(orig, "Eins", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            self.last = 1
            
        elif count_defects == 1:
            cv2.putText(orig, "Zwei", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            self.last = 2
            
        elif count_defects == 2:
            cv2.putText(orig, "Drei", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            self.last = 3
            
        elif count_defects == 3:
            cv2.putText(orig, "Vier", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            self.last = 4
            
        elif count_defects == 4:
            cv2.putText(orig, "Fuenf", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            self.last = 5
            
        return image, orig
    
    def getParameters(self):
        return ["No Parameters"]
        