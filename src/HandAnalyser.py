from AbstractAnalyser import AbstractAnalyser
import cv2
import numpy as np
import math

class HandAnalyser(AbstractAnalyser):
    
    def __init__(self, name):
        super(HandAnalyser, self).__init__(name)
        self.Y_MIN = 0
        self.Y_MAX = 255
        self.Cr_MIN = 133
        self.Cr_MAX = 173
        self.Cb_MIN = 77
        self.Cb_MAX = 127
        
        self.last = 0
        self.palm = 0
        self.max_inscribed_center = None
        self.max_inscribed_radius = 0
        self.min_enclosing_center = None
        self.min_enclosing_radius = None
        self.defects = None
        self.hull = None
        self.control = False
        
        self.kernel = np.ones((1,3), np.uint8)
    
    def getSkin(self, image):
        #image = cv2.flip(image, 1)
        
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
        return skin
    
    def getContours(self, frame):
        image, contours, hierarchy = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours
    
    def getMaxContour(self, contours):
        contour = max(contours, key=cv2.contourArea)
        #contour = sorted(contours, key=cv2.contourArea, reverse=False)[:1]
        return contour
    
    def getMinEnclosingCircle(self, contour):
        (x, y), radius = cv2.minEnclosingCircle(contour)
        self.min_enclosing_center = (int(x), int(y))
        self.min_enclosing_radius = int(radius)
        
    def getMaxInscribedCircle(self, contour, frame):
        x, y, w, h = cv2.boundingRect(contour)
        rows, cols = frame.shape[:2]
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
    
    def getConvexHull(self, contour):
        hull = cv2.convexHull(contour)
        self.hull = hull
        
    def getDefects(self, contour):
        hull = cv2.convexHull(contour, returnPoints=False)
        if hull is not None and len(hull) > 3 and len(contour) > 3:
            defects = cv2.convexityDefects(contour, hull)
            self.defects = defects
            
    def drawMinEnclosingCircle(self, frame):
        cv2.circle(frame, self.min_enclosing_center, self.min_enclosing_radius, (0,255,0), 1)
        return frame
    
    def drawMaxInscribedCircle(self, frame):
        if self.max_inscribed_center is not None and self.max_inscribed_radius is not None:
            cv2.circle(frame, self.max_inscribed_center, self.max_inscribed_radius, (0,0,0), 1)
        return frame
    
    def drawConvexHull(self, frame):
        self.hull = np.array(self.hull).reshape((-1,1,2)).astype(np.int32)
        cv2.drawContours(frame, [self.hull], 0, (0,255,0), 1)
        return frame
    
    def drawDefects(self, contour, frame):
        count_defects = 0
        if contour.size > 100:
            for i in range(self.defects.shape[0]):
                s,e,f,d = self.defects[i,0]
                start = tuple(contour[s][0])
                end = tuple(contour[e][0])
                far = tuple(contour[f][0])
                extLeft = tuple(contour[contour[:,:,0].argmin()][0])
                cv2.circle(frame, extLeft, 5, (96,245,221), 1)
                
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = math.acos((b ** 2 + c ** 2 - a**2) / (2 * b * c)) * 57
                
                distSE = math.sqrt(((end[0] - start[0]) **2) + ((end[1] - start[1]) ** 2))
                distSF = math.sqrt(((start[0] - far[0]) ** 2) + ((start[1] - far[1]) ** 2))
                
                if angle < 80 and distSE > 20 and distSF > 30:
                    count_defects += 1
                    cv2.circle(frame, far, 2, (0,0,255), 1)
                    cv2.line(frame, start, end, (0,127,127), 1)
                    cv2.circle(frame, start, 5, (96,245,221), 1)
                    
        if count_defects == 0:
            cv2.putText(frame, "Eins", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            self.last = 1
            
        elif count_defects == 1:
            cv2.putText(frame, "Zwei", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            self.last = 2
            
        elif count_defects == 2:
            cv2.putText(frame, "Drei", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            self.last = 3
            
        elif count_defects == 3:
            cv2.putText(frame, "Vier", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            self.last = 4
            
        elif count_defects == 4:
            cv2.putText(frame, "Fuenf", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            self.last = 5
            
        return frame    

    def analyse(self, image):
        original = image.copy()
        image = self.getSkin(image)
        contours = self.getContours(image)
        if len(contours) > 0:
            contour = self.getMaxContour(contours)
            self.getDefects(contour)
            self.getMinEnclosingCircle(contour)
            self.getMaxInscribedCircle(contour, image)
            self.getConvexHull(contour)
            
            original = cv2.drawContours(original, [contour], 0, (255, 0, 0), 1)
            original = self.drawConvexHull(original)
            original = self.drawDefects(contour, original)
            original = self.drawMinEnclosingCircle(original)
            original = self.drawMaxInscribedCircle(original)
            
            #original = cv2.rectangle(original, (50,0), (50,320), (255, 0, 0), 2)
            #original = cv2.rectangle(original, (270,0), (270,320), (255, 0, 0), 2)
            
        return original, True
        
    
    