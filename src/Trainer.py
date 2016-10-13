import sys
import argparse as ap
import cv2
import numpy as np
import os
import FeatureExtractor
from sklearn.feature_selection import SelectKBest, chi2, f_classif
from sklearn.preprocessing import StandardScaler
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from sklearn.cross_validation import StratifiedKFold
import matplotlib.pyplot as plt
from sklearn.externals import joblib

parser = ap.ArgumentParser()
parser.add_argument("-t", "--trainingSet", required="True")
parser.add_argument("-b", "--best_params", action='store_true')
parser.add_argument("-p", "--plot", action='store_true')
args = vars(parser.parse_args())

should_plot = args["plot"]
calculate_best_params = args["best_params"]
train_path = args["trainingSet"]

training_names = os.listdir(train_path)

image_paths = []
image_labels = []
features = []
normalization_parameter = []
class_id = 0

for training_name in training_names:
    directory = os.path.join(train_path, training_name)
    class_path = [os.path.join(directory, file) for file in os.listdir(directory)]
    image_paths += class_path
    image_labels += [class_id] * len(class_path)
    class_id += 1
    
for image_path in image_paths:
    image = cv2.imread(image_path)
    image = cv2.flip(image, 1)
    features.append(FeatureExtractor.getFeatures(image))
    
features = np.array(features)
labels = np.array(image_labels)
selector = SelectKBest(chi2, k='all')
scaler = StandardScaler().fit(features)
features = scaler.transform(features)

if calculate_best_params:
    C_range = 10. ** np.arange(-10, 10)
    gamma_range = 10. ** np.arange(-10, 10)
    param_grid = dict(gamma=gamma_range, C=C_range)
    grid = GridSearchCV(SVC(), param_grod=param_grid, cv=StratifiedKFold(labels, 5))
    grid.fit(features, labels)
    
    print "Best classifier is :", grid.best_estimator_
    
classifier = SVC(kernel="rbf", gamma=0.1, C=100.0, probability=True, class_weight=None, coef0=0.0, degree=3, shrinking=True, tol=0.001, verbose=False)
classifier.fit(features, labels)
joblib.dump((classifier, training_names, normalization_parameter, features, labels, selector, scaler), "classifier.pkl", compress=3)

if should_plot:
    
    if 'SVC' in str(type(classifier)):
        w = classifier.coef_[0]
        a = -w[0] / w[1]
        xx = np.linspace(-1,1)
        yy = a * xx - classifier.intercept_[0] / w[1]
        
        w2 = classifier.coef_[1]
        a2 = -w2[0] / w2[1]
        yy2 = a2 * xx - classifier.intercept_[1] / w2[1]
        
        w3 = classifier.coef_[2]
        a3 = -w3[0] / w3[1]
        yy3 = a3 * xx -classifier.intercept_[2] / w3[1]
        
        plt.plot(xx, yy, 'r-')
        plt.plot(xx, yy2, 'b-')
        plt.plot(xx, yy3, 'k-')
        
        plt.scatter(features[:, 0], features[:, 1], c=labels, cmap=plt.cm.Paired)
        plt.axis('tight')
        plt.ylim(-1,1)
        plt.show()
        