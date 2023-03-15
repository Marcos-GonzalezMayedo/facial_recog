import PySimpleGUI as sg
from camera_module import camera_module
from feature_extractor import feature_extractor
import image_loader
from image_saver import image_saver
from simple_gui import simple_gui
from pop_up_gui import pop_up_gui
from model import model
from label_camera_module import label_camera_module
import os
import cv2

#TODO: Need to finish adding error checking for when users enter path names.
#TODO: Less important but make sure that we have the same syntax variable declaration style throughout the program structure.

def main():
    sg.theme('LightTeal')
    layout = [  [sg.Text("Choose an action to continue:")],
                [sg.Button("Take Photo")],
                [sg.Button("Extract Features")],
                [sg.Button("Train Model")],
                [sg.Button("Run Model")]]

    window = sg.Window("Facial Recognizer", layout)
    
    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Take Photo":
            launchPhotoModule()
        elif event == "Extract Features":
            launchExtractModule()
        elif event == "Train Model":
            launchTrainModule()
        elif event == "Run Model":
            launchDetectorModule()

    window.close()

def launchPhotoModule():
    layout = [[sg.Text("Please enter file path to save photos set: (Include the top level directory)")],
                    [sg.Input(key="USER_RESPONSE")],
                            [sg.Button("CONFIRM"), sg.Button("CANCEL")]]
    
    ask_user_path = pop_up_gui(layout)
    ask_user_path.display()

    while True:
        event, values = ask_user_path.get_window_events()

        if event == sg.WINDOW_CLOSED or event == "CANCEL":
            ask_user_path.killWindow()
            return
        elif event == "CONFIRM":
            where_to_save = values["USER_RESPONSE"]
            ask_user_path.killWindow()
            break

    imageSaver = image_saver(os.getcwd() + "/" + where_to_save, "photo")
    imageSaver.makeDir()
    camera_test = camera_module(imageSaver)
    camera_test.runModule()

    return

def launchExtractModule():
    layout = [[sg.Text("Please enter file path to images for feature extraction:")],
                    [sg.Input(key="USER_RESPONSE_1")],
                            [sg.Text("Please enter directory for which to save features extracted:")],
                                [sg.Input(key="USER_RESPONSE_2")],
                                    [sg.Button("CONFIRM"), sg.Button("CANCEL")]]
    ask_user_paths = pop_up_gui(layout)
    ask_user_paths.display()

    while True:
        event, values = ask_user_paths.get_window_events()

        where_to_extract = None
        where_to_save = None

        if event == sg.WINDOW_CLOSED or event == "CANCEL":
            ask_user_paths.killWindow()
            return
        elif event == "CONFIRM":
            where_to_extract = values["USER_RESPONSE_1"]
            where_to_save = values["USER_RESPONSE_2"]
            ask_user_paths.killWindow()
            break
        
    photo_path = os.getcwd() + "/" + where_to_extract
    cascader_path = "faceCascadeData.xml"
    feature_save_path = os.getcwd() + "/" + where_to_save
    face_fetcher = feature_extractor(cascader_path)

    photos = []
    photo_tracker = {}

    #Load In Images:
    directories = next(os.walk(photo_path))
    for photoDirectory in directories[1]:
        currentDir = photo_path + "/" + photoDirectory
        photo_tracker[photoDirectory] = photos
        for photo in os.listdir(currentDir):
            image = cv2.imread(currentDir + "/" + photo)
            photos.append(image)
            
        photos = []

    #Extract and Save Images:
    features = []
    feature_saver = None
    for label in photo_tracker.keys():
        features.clear()
        feature_saver = image_saver(feature_save_path + "/" + label, "feature")
        feature_saver.makeDir()
        for feature in photo_tracker[label]:
            face_fetcher.extractFeatures(feature)
            features.extend(face_fetcher.getFeaturesExtracted())
        
        feature_saver.saveImages(features)

    return
    

def launchTrainModule():
    layout = [[sg.Text("Please enter file path to root feature folder: ")],
                    [sg.Input(key="USER_RESPONSE_1")],
                        [sg.Text("Please enter file path to model save folder: ")],
                            [sg.Input(key="USER_RESPONSE_2")],
                                [sg.Text("Please enter file path to save labels: ")],
                                    [sg.Input(key="USER_RESPONSE_3")],
                                        [sg.Button("CONFIRM"), sg.Button("CANCEL")]]
    
    ask_user_paths = pop_up_gui(layout)
    ask_user_paths.display()

    where_to_extract = None
    where_to_save_model = None
    where_to_save_labels = None

    while True:
        event, values = ask_user_paths.get_window_events()

        if event == sg.WINDOW_CLOSED or event == "CANCEL":
            ask_user_paths.killWindow()
            return
        elif event == "CONFIRM":
            where_to_extract = os.getcwd() + '/' + values["USER_RESPONSE_1"]
            where_to_save_model = os.getcwd() + '/' + values["USER_RESPONSE_2"]
            where_to_save_labels = os.getcwd() + '/' + values["USER_RESPONSE_3"]
            ask_user_paths.killWindow()
            break

    model_status = model()

    model_status.initialize_model() #Set the default image size to (82x82).

    #TODO: Need to find a way to freeze the frame during the model training:
    layout = [[sg.Text("Please wait for the model to finish training!")]]
    wait_gui = pop_up_gui(layout=layout)
    wait_gui.display()

    model_status.train_model(where_to_extract, 4) #Setting the epochs and the diredtory path for the model.
    model_status.save_model(where_to_save_model, where_to_save_labels)

    wait_gui.killWindow()

    return

def launchDetectorModule():
    #1. Must be pointed to the folder where the weights are saved.
    #2. Must run the normal camera module and disaply the predictions in a rectangular frame.

    #For every image received, will use a feature extractor to get the features,
    #   for every feature, will get the label for it.
    #For every label and feature tuple, it will draw a rectangle and list the user's
    #   name.
    layout = [[sg.Text("Please enter file path to saved model: ")],
                    [sg.Input(key="USER_RESPONSE_1")],
                        [sg.Text("Please enter file path to label file:")],
                            [sg.Input(key="USER_RESPONSE_2")],
                                [sg.Button("CONFIRM"), sg.Button("CANCEL")]]

    ask_user_paths = pop_up_gui(layout)
    ask_user_paths.display()

    where_to_load_model = None
    where_to_load_labels = None

    while True:
        event, values = ask_user_paths.get_window_events()

        if event == sg.WINDOW_CLOSED or event == "CANCEL":
            ask_user_paths.killWindow()
            return
        elif event == "CONFIRM":
            where_to_load_model = os.getcwd() + '/' + values["USER_RESPONSE_1"]
            where_to_load_labels = values["USER_RESPONSE_2"]
            ask_user_paths.killWindow()
            break

    ask_user_paths.killWindow()

    #Have to load the camera in there and apply the label to the image:
    label_cam_module = label_camera_module(where_to_load_model, where_to_load_labels)
    label_cam_module.runModule()

    return

if __name__ == "__main__":
    main()
