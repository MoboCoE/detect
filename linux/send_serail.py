import serial
import time

def get_serial():
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1.0)  
    
    ser.reset_input_buffer()
    return ser

def send_data(left_speed, right_speed):
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1.0)  
   
    ser.reset_input_buffer()
    message = f"{left_speed},{right_speed}\n"
    ser.write(message.encode('utf-8'))

# note -> add header
