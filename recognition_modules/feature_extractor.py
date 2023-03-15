import cv2
import simple_gui
import os
from image_saver import image_saver

#Handles the feature extraction of images. Takes in cascade model and images from which to extract features.
#TODO: Modulate this so that we get to decide the size of image to modulate to.
class feature_extractor:

    def __init__(self, cascaderPath):
        self.cascadeClassifier = cv2.CascadeClassifier(cascaderPath)
        self.featuresExtracted = []
        self.featureCoordinates = []
        self.featureSize = (82, 82)
        self.featureLocations = None

    def drawRectangle(self, image, x, y, w, h):
        return cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    def set_feature_size(self, feature_size):
        self.featureSize = feature_size

    def get_feature_size(self):
        return self.featureSize
    
    def extractFeatures(self, image):
        """Takes an image array and saves the features internally."""
        self.featuresExtracted.clear()
        self.featureCoordinates.clear()
        imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = self.cascadeClassifier.detectMultiScale(imageGray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

        retrievedImage = None
        for (x, y, w, h) in faces:
            retrievedImage = imageGray[y:y+h, x:x+w]
            grayImage = cv2.resize(retrievedImage, self.featureSize, interpolation = cv2.INTER_AREA)

            #Testing:
            # cv2.imshow("test_feature", retrievedImage)

            self.featuresExtracted.append(grayImage)
            self.featureCoordinates.append((x,y, w, h))

    def get_feature_coords(self):
        return self.featureCoordinates

    def getFeaturesExtracted(self):
        return self.featuresExtracted

#Testing:
if __name__ == "__main__":
    featureLabel = "sage"
    photoPath = os.getcwd() + "/photos3"
    cascaderPath = "faceCascadeData.xml"
    testFeatures = feature_extractor(cascaderPath)
    
    featureImageSaver = image_saver(os.getcwd() + "/" + featureLabel, "feature")
    featureImageSaver.makeDir()

    featureCtr = 0

    for imageName in os.listdir(photoPath):
        currentImage = cv2.imread(photoPath + "/" + imageName)
        testFeatures.extractFeatures(currentImage)
        featureImageSaver.saveImages(testFeatures.getFeaturesExtracted())

        
