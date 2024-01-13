import cv2
import time

from start_camera import capture
from img_processing import filter_img
from line import find_line
from send_serial import get_serial, send_data
from line import find_line
import threading

frame = None

def capture_frames():
    global frame
    cap = capture()
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("Failed to capture frame")
            break

def process_image():
    while True:
        start = time.time()

        global frame
        if frame is not None:
            mask = filter_img(frame)
            find_line(mask)

        end = time.time()
        print("Processing(s):", end - start)


try:
    get_serial()

    # Create threads for frame capture and image processing
    capture_thread = threading.Thread(target=capture_frames)
    processing_thread = threading.Thread(target=process_image)

    # Start both threads
    capture_thread.start()
    processing_thread.start()

    # Wait for both threads to finish
    capture_thread.join()
    processing_thread.join()


except KeyboardInterrupt:
    send_data(0, 0)
    print("Exit")
    cv2.destroyAllWindows() 