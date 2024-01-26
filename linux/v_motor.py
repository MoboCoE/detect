import math
from send_serial import get_serial, send_data
import time
global state
def velocity(status, x, y):
    
    slope = float(x)
    intersect = float(y)
    base_speed = 120
    max_speed = 200
    k_slope = 50
    maxline = 60
    minline = 30
    a = 30

    if status == "true":
        state = 0

        if (slope < 0 and intersect < 0) or (slope > 0 and intersect > 0):
            if -1 < slope < 1 and minline <= intersect <= maxline:
                right_speed = base_speed
                left_speed = base_speed
                print("ตรง")
                print(left_speed, right_speed)
                
                
            elif intersect > maxline or intersect < minline:
                if intersect > maxline:
                    
                    send_data(intersect*10, 0)
                    print("เลี้ยวขวาตรง", intersect)
                    right_speed = 0
                    left_speed = a
                    
                if intersect < minline:
                    if intersect<0:
                        intersect = -intersect-minline
                    send_data(0, intersect*20)
                    print("เลี้ยวซ้ายตรง", intersect)
                    right_speed = a
                    left_speed = 0

        elif slope > 0 and intersect < 0:
            right_speed = 80 + k_slope*slope + (-intersect)/60
            left_speed = 80 - k_slope*slope - (-intersect)/20
            print("เลี้ยวซ้าย")
            print(left_speed, right_speed)

        elif slope < 0 and intersect > 0:
            slope = -slope
            right_speed = 80 - k_slope*slope - intersect/60
            left_speed = 80 + k_slope*slope + intersect/20
            print("เลี้ยวขวา")
            print(left_speed, right_speed)

    else:
        if x != 0 and y != 0:
            right_speed = x
            left_speed = y
            print(left_speed, right_speed)
        else:
            right_speed = 0
            left_speed = 0
            print(left_speed, right_speed)
            
    # Limit the motor speeds to the maximum value
    left_speed = max(-max_speed, min(max_speed, left_speed))
    right_speed = max(-max_speed, min(max_speed, right_speed))

    return right_speed, left_speed
