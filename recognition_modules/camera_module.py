import numpy
import cv2
import PySimpleGUI as sg
import os
from singleton_camera import SingletonCamera
from camera_gui import camera_gui
from image_saver import image_saver

class camera_module():

    def __init__(self, imageSaver: image_saver):
        self.image_arr = None
        self.lastImageSaved = None
        self.imageSaver = imageSaver

    def updateFrame(self):
        ret , frame = self.camera.getCurrentFrame()
        image_arr = cv2.resize(frame, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
        image = cv2.imencode(".png", frame)[1].tobytes() #Should probably make this a separate function.
        self.image_arr = image_arr
        self.gui.setGuiImage(image)
                
    def runModule(self):
        self.camera = SingletonCamera()
        self.gui = camera_gui()
        self.gui.display()

        while True:
            event, values = self.gui.checkEvent()
            
            if event == sg.WINDOW_CLOSED or event == "Exit":
                break
            elif event == "Capture":
                self.captureImage()
            self.updateFrame()

        self.killWindow()

    def captureImage(self):
        self.lastImageSaved = self.image_arr
        self.imageSaver.saveImage(self.lastImageSaved)

    def setDirectory(self, directoryPath: str):
        self.directory = directoryPath

    def killWindow(self):
        self.gui.killWindow()
        self.camera.closeCamera()

if __name__ == "__main__":
    whereToSave = "photos"
    imageSaver = image_saver(os.getcwd() + "/" + whereToSave, "photo")
    imageSaver.makeDir()
    camera_test = camera_module(imageSaver)
    camera_test.runModule()