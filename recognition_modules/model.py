import tensorflow as tf
import cv2
from image_loader import image_loader
import os
import numpy as np
import pickle

#Test model for handling simple facial classification:
# Deafult training data size is 82 * 82
def main():
    featurePathMain = os.getcwd() + "/features"

    features = []
    featureLabels = []
    labelTracker = {}
    labelCounter = 0
    directories = next(os.walk(featurePathMain))
    for featureName in directories[1]:
        currentDir = featurePathMain + "/" + featureName
        labelTracker[labelCounter] = featureName
        for featureName in os.listdir(currentDir):
            feature = cv2.imread(currentDir + "/" + featureName, cv2.IMREAD_GRAYSCALE)
            features.append(feature)
            featureLabels.append(labelCounter)

        labelCounter += 1

    test_model = model()
    test_model.load_model("test_model", "test_labels")

    feature_number = 0
    for feature in features:
        label_name = test_model.classify_feature(feature)
        actual_label_name = labelTracker[featureLabels[feature_number]]
        feature_number += 1

        cv2.imshow(label_name , feature)
        cv2.waitKey(0)
        


def test_predictions():
    pass

#1. Needs to handle the creation and training of a simple NN.
#2. Must be able to save the weights for other modules to use.
class model:
    def __init__(self) -> None:
        self.model = None
        self.labelTracker = None

    def load_model(self, model_file_path, load_label_path):
        self.model = tf.keras.models.load_model(model_file_path)
        with open(load_label_path + "/labels.pickle", 'rb') as handle:
            self.labelTracker = pickle.load(handle)


    def save_model(self, save_file_path, save_label_path):
        if self.model is not None:
            self.model.save(save_file_path)
            os.mkdir(save_label_path)
            with open(save_label_path + "/labels.pickle", 'wb') as handle:
                pickle.dump(self.labelTracker, handle, protocol=pickle.HIGHEST_PROTOCOL)

        
    def initialize_model(self, image_size = (82, 82)):
        if self.model is None:
            self.model = tf.keras.models.Sequential([
                tf.keras.layers.Flatten(input_shape=image_size),
                tf.keras.layers.Dense(150, activation='relu'),
                tf.keras.layers.Dense(3),
                tf.keras.layers.Softmax()
            ])

        return
    
    def train_model(self, features_file_path: str, epochs: int):
        if self.model is None:
            return

        features = []
        featureLabels = []
        self.labelTracker = {}
        labelCounter = 0
        directories = next(os.walk(features_file_path))
        for featureName in directories[1]:
            currentDir = features_file_path + "/" + featureName
            self.labelTracker[labelCounter] = featureName
            for featureName in os.listdir(currentDir):
                feature = cv2.imread(currentDir + "/" + featureName, cv2.IMREAD_GRAYSCALE)

                #TESTING:
                # cv2.imshow("Current Feature", feature)
                
                features.append(feature)
                featureLabels.append(labelCounter)

            labelCounter += 1
        
        x_train = np.array(features) / 255.0
        y_train = np.array(featureLabels)
    
        lossFunction = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        self.model.compile(optimizer=tf.keras.optimizers.legacy.Adam(), 
                    loss=lossFunction, 
                    metrics=['accuracy'])

        self.model.fit(x_train, y_train, epochs=epochs)


    def classify_feature(self, feature):
        """
        Returns the label that the model predicts for the given feature. (String)
        """
        feature = np.array(feature) / 255.0
        feature = np.array([feature, ])
        if self.model != None:
            prediction = np.array((self.model(feature))[0])
            predicted_index = np.argmax(prediction)

            if prediction[predicted_index] < 0.5:
                predicted_label = "Unknown"
                
                return predicted_label
            
            predicted_label = self.labelTracker[predicted_index]

            return predicted_label


        

if __name__ == "__main__":
    main()