import os
import cv2

#Can make this a simple function instead.
class image_saver:
    def __init__(self, pathToSave: str, savePrefix: str):
       self.pathToSave = pathToSave
       self.imageCounter = 0;
       self.savePrefix = savePrefix
       
    def makeDir(self):
        try:
            os.makedirs(self.pathToSave)
        except:
            pass

    def saveImage(self, image):
        cv2.imwrite(self.pathToSave + "/" + self.savePrefix + str(self.imageCounter) + ".png", image)
        self.imageCounter += 1

    def saveImages(self, images):
        for image in images:
            self.saveImage(image)