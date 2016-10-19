from AbstractAnalyser import AbstractAnalyser
from AbstractFilter import AbstractFilter
import FeatureExtractor
import cv2
import numpy as np
from sklearn.externals import joblib

class Classifier(AbstractAnalyser):
    
    def __init__(self, name):
        super(Classifier, self).__init__(name)
        self.classifier, self.training_names, self.normalization_parameter, self.train_features, self.train_labels, self.selector, self.scaler = joblib.load("/home/pi/Desktop/Framework/src/classifier.pkl")
        self.last_gesture = ""
        self.name = "Classifier"
    
    def writeLastGesture(self, image):
        cv2.putText(image, self.last_gesture, (0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 2)
        return image
    
    def analyse(self, image, orig):
        image_features = FeatureExtractor.getFeatures(image)
        image_features = np.array([image_features])
        
        image_features = self.scaler.transform(image_features)
        confidence = np.amax(self.classifier.predict_proba(image_features))
        
        if confidence > 0.7:
            self.last_gesture = str([self.training_names[i] for i in self.classifier.predict(image_features)][0])
            orig = self.writeLastGesture(orig)
        
        else:
            self.last_gesture = "Unsure"
            orig = self.writeLastGesture(orig)
            
        return image, orig, self.last_gesture
    
        