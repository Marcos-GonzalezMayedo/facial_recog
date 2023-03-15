import cv2
import numpy

def downSampleImage(image):
    return cv2.resize(image, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)