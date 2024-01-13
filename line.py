
def velocity(status, x, y):

    setpoint_slope = 0.02
    slope = x
    base_speed = 50
    max_speed = 200
    k_slope = 15

    if status == "true":
        if -setpoint_slope <= slope <= setpoint_slope:
            right_speed = base_speed
            left_speed = base_speed

        if slope > setpoint_slope:
            right_speed = base_speed + k_slope*slope
            left_speed = base_speed - k_slope*slope


        if slope < -setpoint_slope:
            slope = -slope
            right_speed = base_speed - k_slope*slope
            left_speed = base_speed + k_slope*slope
    
    else:
        right_speed = 0
        left_speed = 0

    # Limit the motor speeds to the maximum value
    left_speed = max(-max_speed, min(max_speed, left_speed))
    right_speed = max(-max_speed, min(max_speed, right_speed))


    return right_speed, left_speed
