from numpy import asarray
import numpy as np
from v_motor import velocity
from scipy.stats import zscore
from send_serial import get_serial, send_data
import time

def find_line(mask):
    start = time.time()
    # get_serial()

    # change image to array
    array_img = asarray(mask)

    col = len(array_img[0, :])
    row = len(array_img[:, 0])
    center_x = col/2
    center_y = row/2

    middle_line = []
    x_axis = []
    y_axis = []

    for i in range(0, row-1, 10):
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

        # delete outlier
        z_scores = zscore(y)

        threshold = 3

        filtered_indices = np.where(np.abs(z_scores) < threshold)
        filtered_x = x[filtered_indices]
        filtered_y = y[filtered_indices]

        # find a, b
        if len(filtered_x) != 0 and len(filtered_y) != 0:
            a, b = np.polyfit(filtered_x, filtered_y, 1)
            print(f"true,{a},{b}")
            right_speed, left_speed = velocity("true", a, b)
            print(f"R: {right_speed} L:{left_speed}")

        else:
            a, b = np.polyfit(x, y, 1)
            print(f"true,{a},{b}")
            right_speed, left_speed = velocity("true", a, b)
            print(f"R: {right_speed} L:{left_speed}")

    else:
        print(f"false,NaN,NaN")
        right_speed, left_speed = velocity("false", 0, 0)
        print(f"Right: {right_speed} Left:{left_speed}")
    
    send_data(left_speed, right_speed)

    end = time.time()
    # print("find mid line(s):", end-start)
