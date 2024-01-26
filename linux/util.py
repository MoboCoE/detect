import numpy as np
import cv2

def get_limits(color):

    lowerLimit = np.array([10, 100, 100])
    upperLimit = np.array([80, 255, 255])
    
    return lowerLimit, upperLimit

