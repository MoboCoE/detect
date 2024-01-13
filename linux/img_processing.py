import cv2
from util import get_limits
import time

def filter_img(frame):
    start = time.time()
    yellow = [0, 255, 255]
    # flip
    flip_img = cv2.flip(frame, 0)
    flip_img_hz = cv2.flip(flip_img, 1)

    # resize image
    # scale_percent = 60 # percent of original size
    # width = int(frame.shape[1] * scale_percent / 100)
    # height = int(frame.shape[0] * scale_percent / 100)
    # dim = (width, height)

    # resize_img = cv2.resize(flip_img_hz, dim, interpolation = cv2.INTER_AREA) 

    hsvImage = cv2.cvtColor(flip_img_hz, cv2.COLOR_BGR2HSV)
    lowerLimit, upperLimit = get_limits(color=yellow)

    mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)
    end = time.time()

    # print("image processing time(s):", end-start)

    return mask