from AbstractFilter import AbstractFilter
import cv2

class MinEnclosing(AbstractFilter):
    
    def __init__(self, name):
        super(MinEnclosing, self).__init__(name)
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