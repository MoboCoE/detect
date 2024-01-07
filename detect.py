import cv2
from numpy import asarray
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore

img = cv2.imread("D:\mobile_robot\mobile_robot\camera\img5.jpg")

# resize image
scale_percent = 60 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
  
resize_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 

# grayscale
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# threshold image
(thresh, thresh_img) = cv2.threshold(gray_img, 168, 255, cv2.THRESH_BINARY)

# change image to array
array_img = asarray(thresh_img)

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
            bf_array = array_img[i, index-1]
            af_array = array_img[i, index+1]
            # print(bf_array, j, af_array)
            
        if j == 0 and bf_array == 0 and af_array == 0:
            find_line.append(index)
            # print(bf_array, j, af_array)
            
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

    # delete outlier
    z_scores = zscore(y)

    threshold = 3

    filtered_indices = np.where(np.abs(z_scores) < threshold)
    filtered_x = x[filtered_indices]
    filtered_y = y[filtered_indices]

    # plt.scatter(x, y, label='Original Data')
    # plt.scatter(filtered_x, filtered_y, label='Filtered Data', color='red')
    # plt.legend()
    # plt.show()

    # find a, b
    a, b = np.polyfit(filtered_x, filtered_y, 1)
    plt.scatter(filtered_x, filtered_y)

    print(f"true,{a},{b}")

    plt.plot(filtered_x, a*(filtered_x) + b, 'r')
    plt.grid()
    plt.show()
else:
    print(f"false,NaN,NaN")

