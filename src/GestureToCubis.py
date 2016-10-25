import cv2
import subprocess
import os
from AbstractOutput import AbstractOutput 
from PyQt4 import QtGui
from CubisDevice import CubisDevice
import numpy as np
from enum import Enum

class Gestures(Enum):
    Open_Hand = 1
    Two_Fingers = 2
    Thumb_Left = 3
    Unsure = 4
    Unclassified = 5

class GestureToCubis(AbstractOutput):
    
    def __init__(self, name="GestureToCubis"):
        self.name = name
        self.description = "Calls a function on the balance based in the gesture of the user."
        self.input = "A gesture as string"
        self.current_gesture = Gestures.Unsure
        self.cubis = CubisDevice("172.16.244.75")
        self.gesture_mapping = {"OpenHand" : "self.cubis.rightWindshieldKey", "TwoFingers" : "self.cubis.doTare", "ThumbLeft" : "self.cubis.getWeight"}
        
        
    def output(self, frame, gesture):

        
        if gesture == "OpenHand" and self.current_gesture != Gestures.Open_Hand:
            print "Open Windshield"
            function_to_call = self.gesture_mapping["OpenHand"]
            eval(function_to_call)()
            self.current_gesture = Gestures.Open_Hand
            
        elif gesture == "TwoFingers" and self.current_gesture != Gestures.Two_Fingers:
            function_to_call = self.gesture_mapping["TwoFingers"]
            eval(function_to_call)()
            self.current_gesture = Gestures.Two_Fingers
            
        elif gesture == "ThumbLeft" and self.current_gesture != Gestures.Thumb_Left:
            function_to_call = self.gesture_mapping["ThumbLeft"]
            eval(function_to_call)()
            self.current_gesture = Gestures.Thumb_Left
            
        elif gesture == "Unsure" and self.current_gesture != Gestures.Unsure:
            self.current_gesture = Gestures.Unsure
            
        elif gesture == "Unclassified" and self.current_gesture != Gestures.Unclassified:
            self.current_gesture = Gestures.Unclassified