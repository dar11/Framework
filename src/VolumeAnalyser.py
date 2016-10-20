from AbstractAnalyser import AbstractAnalyser
from PyQt4 import QtGui
import numpy as np
import cv2
import math

class VolumeAnalyser(AbstractAnalyser):
    
    def __init__(self, name):
        super(VolumeAnalyser, self).__init__(name)
        self.number_of_bins = None
        self.current_upper_left = (0,0)
        self.current_lower_right = (0,0)
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        
        self.regions_of_interest = []
        self.start_search = False
        self.found_regions = False
        self.whole_roi = None
        self.show_select_image = False
        self.selected_region = False
        
        self.max_volume = 0
        

        
    def select_regions(self, event, x, y, flags, param):
        
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.current_upper_left == (0,0):
                self.current_upper_left = (x, y)
            else:
                self.current_lower_right = (x,y)
                self.start_search = True
                self.selected_region = True
                cv2.destroyWindow("Select")
                
    def isAlreadyContained(self, x, y):
        for roi in self.regions_of_interest:
            _x, _y = roi[0]
            if math.fabs(x - _x) > 10 and math.fabs(y - _y) < 10:
                return True
        return False
    
    def deleteShortLines(self, lines):
        to_delete = []
        for i in range(lines.shape[0]):
            for x1, y1, x2, y2 in lines[i]:
                if math.fabs(x1-x2) < 8 or math.fabs(y1-y2) > 20:
                    to_delete.append(i)
        lines = np.delete(lines, to_delete, axis=0)
        return lines
        
            
    def analyse(self, image, orig):
        while self.number_of_bins is None or self.max_volume == 0:
            bins, ok = QtGui.QInputDialog.getInt(QtGui.QWidget(),"Enter number of Bins", "Please enter the number of bins")
            volume, ok2 = QtGui.QInputDialog.getDouble(QtGui.QWidget(),"Enter maximum volume", "Please enter the maximum volume")
            if ok and ok2:
                self.number_of_bins = bins
                self.max_volume = volume
                self.last_procents = [[0] for i in range(int(self.number_of_bins))]
                self.frames = [[] for i in range(int(self.number_of_bins))]
                self.values = [[] for i in range(int(self.number_of_bins))]
                break
            else:
                continue
        if not self.show_select_image:
            cv2.namedWindow("Select")
            cv2.setMouseCallback("Select", self.select_regions)
            self.show_select_image = True
        if not self.selected_region:
            cv2.imshow("Select", orig)
            key = cv2.waitKey(1) & 0xFF
            
        if self.start_search and not self.found_regions:
            cnt_temp = image.copy()
            subregion = cnt_temp[self.current_upper_left[1]:self.current_lower_right[1], self.current_upper_left[0]:self.current_lower_right[0]]
            img, cnts, hier = cv2.findContours(subregion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cnts = sorted(cnts, key=cv2.contourArea, reverse=False)[:5]
            for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02*peri, True)
                if len(approx) == 4 and cv2.contourArea(c) > 2000:
                    correctContour = approx
                    x,y,w,h = cv2.boundingRect(correctContour)
                    contained = self.isAlreadyContained(x, y)
                    if contained:
                        continue
                    
                    self.regions_of_interest.append([(x,y), (x+w, y+h)])
                    cnts.remove(c)
                    if len(self.regions_of_interest) == int(self.number_of_bins):
                        self.found_regions = True
                        self.start_search = False
                        break
                    
        if self.found_regions:
            self.whole_roi = orig[self.current_upper_left[1]:self.current_lower_right[1], self.current_upper_left[0]:self.current_lower_right[0]]
            self.whole_roi_edge = image[self.current_upper_left[1]:self.current_lower_right[1], self.current_upper_left[0]:self.current_lower_right[0]]
            for index, roi in enumerate(self.regions_of_interest):
                procent = 0
                image_roi = self.whole_roi_edge[roi[0][1]+2:roi[1][1]-2, roi[0][0]+2:roi[1][0]-2]
                image_roi_orig = self.whole_roi[roi[0][1]+2:roi[1][1]-2, roi[0][0]+2:roi[1][0]-2]
                cv2.rectangle(self.whole_roi, roi[0], roi[1], (0,255,0), 2)
                
                lines = cv2.HoughLinesP(image_roi, 4, np.pi/180, 80, 30, 10)
                
                if lines is not None:
                    lines = self.deleteShortLines(lines)
                    
                    if lines.shape[0] > 0:
                        y1_values = lines[:,:,1]
                        
                        y1_values_sorted = np.sort(y1_values, axis=None)
                        y1_middle_value = y1_values_sorted[len(y1_values_sorted) / 2]
                        y1_middle_index = np.nonzero(y1_values == y1_middle_value)[0][0]
                        
                        for x1, y1, x2, y2 in lines[y1_middle_index]:
                            diff = float(image_roi.shape[:2][0]) - y1
                            if diff > 5 and diff < image_roi.shape[:2][0] - 10:
                                cv2.line(image_roi_orig, (x1, y1), (x2,y2), (0,0,255), 2)
                                procent = (diff/float(image_roi.shape[:2][0]))*100
                                
                                procent = round(procent, 2)
                                
                                if math.fabs(procent - self.last_procents[index][0]) > 2:
                                    self.last_procents[index][0] = procent
                                    
                millis = self.max_volume * (self.last_procents[index][0] / 100)
                if millis < 0.0:
                    millis = 0.0
                cv2.putText(self.whole_roi, str(millis)+"ml", (roi[0][0], roi[0][1]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                                    
                                
            
        return image, orig, None
        
        