import cv2
from numpy import asarray
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore
import time
from util import get_limits

try:
    cap = cv2.VideoCapture("/dev/video0")

    yellow = [0, 255, 255]

    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()
    else:
        print("Open Camera")

    while (True):
        start = time.time()

        ret, frame = cap.read()
        if ret and frame is not None:
            # resize image
            scale_percent = 60 # percent of original size
            width = int(frame.shape[1] * scale_percent / 100)
            height = int(frame.shape[0] * scale_percent / 100)
            dim = (width, height)
            
            resize_img = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA) 

            hsvImage = cv2.cvtColor(resize_img, cv2.COLOR_BGR2HSV)
            lowerLimit, upperLimit = get_limits(color=yellow)

            mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

            # # grayscale
            # gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


            # # threshold image
            # (thresh, thresh_img) = cv2.threshold(gray_img, 168, 255, cv2.THRESH_BINARY)

            # change image to array
            array_img = asarray(mask)

            col = len(array_img[0, :])
            row = len(array_img[:, 0])
            center_x = col/2
            center_y = row/2

            middle_line = []
            x_axis = []
            y_axis = []

            for i in range(0, row-1, 6):
                find_line = []
                index = 0
                for j in array_img[i, :]:
                    if index > 0 and index < col-1:
                        # print(array_img[i, 0])
                        bf_array = array_img[i, index-1]
                        af_array = array_img[i, index+1]
                        # print(index)
                        
                        if j == 255 and bf_array == 255 and af_array == 255:
                            find_line.append(index)
                            # print(bf_array, j, af_array)
                    if j == 255 and index == 0:
                        find_line.append(index)
                        
                    index += 1
                if len(find_line) != 0:
                    first_col = find_line[0]
                    last_col = find_line[-1]
                    mid_col = (first_col+last_col)/2
                    center_zero_x = i - center_y
                    center_zero_y = mid_col - center_x
                    mid_point = [center_zero_x, center_zero_y] #(y,x)
                    # mid_point = [mid_col, i]
                    middle_line.append(mid_point)
                    x_axis.append(center_zero_x)
                    y_axis.append(center_zero_y)
                
            #print(x_axis)
            if len(x_axis) != 0 or len(y_axis) != 0:
                x = np.array(x_axis, dtype=float)
                y = np.array(y_axis, dtype=float)

                a, b = np.polyfit(x, y, 1)
                print(f"true,{a},{b}")

            else:
                print(f"false,NaN,NaN")

            end = time.time()

            print(end-start)

            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break

        else:
            print("Failed to capture frame")

    cap.release()
    cv2.destroyAllWindows() 

except KeyboardInterrupt:
    print("Exit")
    cap.release()
    cv2.destroyAllWindows() 