import os
import cv2

#Can make this a simple function isntead:
class image_loader:
    def __init__(self, pathToDir, prefix):
        self.prefix = prefix
        self.pathToDir = pathToDir

    def setDir(self, pathToDir):
        self.pathToDir = pathToDir

    def setPrefix(self, prefix):
        self.prefix = prefix

    def loadImages(self):
        images = []
        for image in os.listdir(self.pathToDir):
            if image.find(self.prefix) >= 0:
                currentImage = cv2.imread(self.pathToDir + "/" + image)
                images.append(currentImage)
        
        return images