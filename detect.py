import cv2
from numpy import asarray
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore
from util import get_limits
from line import follow_line


img = cv2.imread("D:\mobile_robot\mobile_robot\camera\img.jpg")

yellow = [0, 255, 255]

# resize image
scale_percent = 50 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
  
resize_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 

hsvImage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lowerLimit, upperLimit = get_limits(color=yellow)

mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

# cv2.imshow("mask", mask)

# # grayscale
# gray_img = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)


# # threshold image
# (thresh, thresh_img) = cv2.threshold(gray_img, 168, 255, cv2.THRESH_BINARY)

# change image to array
array_img = asarray(mask)

# print(array_img)

col = len(array_img[0, :])
row = len(array_img[:, 0])
center_x = col/2
center_y = row/2
# print(col, row)
# print(center_x, center_y)

# print(width, height)
# print(col, row) 275, 206
middle_line = []
x_axis = []
y_axis = []

for i in range(row):
    find_line = []
    index = 0
    for j in array_img[i, :]:
        if index > 0 and index < col-1:
            # print(array_img[i, 0])
            bf_array = array_img[i, index-1]
            af_array = array_img[i, index+1]

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

# print(middle_line)

if len(x_axis) != 0 or len(y_axis) != 0:
    x = np.array(x_axis, dtype=float)
    y = np.array(y_axis, dtype=float)
    
    # delete outlier
    z_scores = zscore(y)

    threshold = 3

    filtered_indices = np.where(np.abs(z_scores) < threshold)
    filtered_x = x[filtered_indices]
    filtered_y = y[filtered_indices]

    plt.scatter(x, y, label='Original Data')

    # find a, b
    if len(filtered_x) != 0 and len(filtered_y) != 0:
        a, b = np.polyfit(filtered_x, filtered_y, 1)
        print(f"true,{a},{b}")
        right_speed, left_speed = follow_line(a, b)
        print(f"Right: {right_speed} Left:{left_speed}")
    else:
        a, b = np.polyfit(x, y, 1)
        print(f"true,{a},{b}")
        right_speed, left_speed = follow_line(a, b)
        print(f"Right: {right_speed} Left:{left_speed}")

    plt.plot(x, a*(x) + b, 'g')
    plt.grid()
    plt.show()

else:
    print(f"false,NaN,NaN")

