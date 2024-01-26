import serial

# open port
def get_serial():
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1.0)  
    ser.reset_input_buffer()
    return ser

# send value's motor data
def send_data(left_speed, right_speed):
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1.0)  
    ser.reset_input_buffer()
    message = f"{right_speed},{left_speed}\n"
    ser.write(message.encode('utf-8'))
