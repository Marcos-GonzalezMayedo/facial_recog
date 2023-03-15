from camera_gui import camera_gui
from singleton_camera import SingletonCamera
from model import model
import cv2
import PySimpleGUI as sg
from feature_extractor import feature_extractor

#1. Use composition to filter out the unnecesary methods from the user.
#2. Add on the extra methods needed for the camera to be able to draw 
# and add the label to the camera output.

class label_camera_module():

    def __init__(self, where_to_load_model: str, where_to_load_labels: str):
        self.image_arr = None
        self.lastImageSaved = None
        self.model_interface = model()
        self.featureExtractor = feature_extractor('/Users/marcosgonzalez/personal_projects/camera_module/faceCascadeData.xml')
        try:
            self.model_interface.load_model(where_to_load_model, where_to_load_labels)
        except:
            exit(-1)

    def updateFrameManual(self, image_arr):
        image = cv2.imencode(".png", image_arr)[1].tobytes()
        self.gui.setGuiImage(image)

    def runModule(self):
        self.gui = camera_gui(layout = [
            [sg.Text("Camera View", size=(60,1), justification='center'), sg.Button("Exit", 
            size=(10, 1), button_color='red')],
            [sg.Image(filename='', key="image",size=(500, 300))]
        ])
        self.camera = SingletonCamera()
        self.gui.display()

        while True:
            event, values = self.gui.checkEvent()
            return_code, frame = self.camera.getCurrentFrame()
            frame = cv2.resize(frame, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)

            #Perform operation for feature extraction:
            self.featureExtractor.extractFeatures(frame)
            features = self.featureExtractor.getFeaturesExtracted()
            feature_locations = self.featureExtractor.get_feature_coords()

            #Perform operation for feature labelling: -> Need to extract each individual label and coordinate.
            feature_sets = zip(features, feature_locations)
            for feature_set in feature_sets:
                label = self.model_interface.classify_feature(feature_set[0])

                location = feature_set[1]
                x, y = location[0:2]
                w, h = location[2:]

                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            if event == sg.WINDOW_CLOSED or event == "Exit":
                break

            self.updateFrameManual(frame)

        self.killWindow()

    def killWindow(self):
        self.gui.killWindow()
        self.camera.closeCamera()

    def extractLabelAndLocations(self, ):
        pass
    
    