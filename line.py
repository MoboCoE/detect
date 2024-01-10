def follow_line(x, y):
    # Define the center of the image
    image_center_x = 0
    image_center_y = 0

    if x < 0.01:
        x = 0
    if -20 < y < 20:
        y = 0

    # Define motor speed parameters
    base_speed = 50  # Adjust this value based on your robot's characteristics
    max_speed = 200  # Maximum speed for either motor

    # Calculate the error in x (distance from the line to the center)
    error_x =  x - image_center_x

    # Calculate the error in y (distance from the line to the center)
    error_y = y - image_center_y  # Invert y-axis if needed
    print(error_x, error_y)
    # Calculate motor speeds based on the errors
    left_speed = base_speed - 100*error_x + 0.1*error_y
    right_speed = base_speed + 100*error_x - 0.1*error_y

    # Limit the motor speeds to the maximum value
    left_speed = max(-max_speed, min(max_speed, left_speed))
    right_speed = max(-max_speed, min(max_speed, right_speed))

    # Display the calculated speeds (you can remove this in the final implementation)
    # print(f"Left Speed: {left_speed}, Right Speed: {right_speed}")

    # Replace the following lines with code to control your robot's motors
    # For example, you might use a library like GPIO to control a Raspberry Pi's GPIO pins
    # or a motor controller library for an Arduino.
    # SetMotorSpeed(left_speed, right_speed)

    return right_speed, left_speed

# Example usage:
# Replace these values with the actual x, y coordinates from your line detection algorithm