import cv2
import numpy as np


Y_MIN = 0
Y_MAX = 255
Cr_MIN = 133
Cr_MAX = 173
Cb_MIN = 77
Cb_MAX = 127
kernel = np.ones((1,3), np.uint8)

def getHuMoments(image):
    return cv2.HuMoments(cv2.moments(image)).flatten()

def getFeatures(image):
        
    features = []
    
    contours, binary = getSkinContours(image)
    #image = cv2.Canny(image, 100, 200)
    hu_moments = getHuMoments(binary)
    for hu in hu_moments:
        features.append(hu)
        
    return features

def getSkinContours(image):
    
    w,h = image.shape[:2]
    contour_image = np.zeros((w,h), np.uint8)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    for i in range(5):
        image = cv2.bilateralFilter(image, 3, 9, 9)
    image = cv2.inRange(image, np.array([Y_MIN, Cr_MIN, Cb_MIN]), np.array([Y_MAX, Cr_MAX, Cb_MAX]))
    for i in range(5):
        image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 11)
    
    img, contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        contour = max(contours, key=cv2.contourArea)
        contour_image = cv2.drawContours(contour_image, [contour], -1, 255, 2)
        
    return contours, contour_image
