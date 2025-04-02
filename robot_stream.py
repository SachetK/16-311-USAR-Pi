import base64
import cv2
import zmq
import numpy as np
import time

print("Connecting to camera server")
context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.bind('tcp://*:7123')

camera = cv2.VideoCapture(0)  # init the camera
print("Connected to camera server!")

while True:
    try:
        grabbed, frame = camera.read()  # grab the current frame
        if not grabbed:
           continue

        frame = cv2.resize(frame, (640, 480))  # resize the frame
        encoded, buffer = cv2.imencode('.jpg', frame)
        footage_socket.send(buffer.tobytes())

    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        break
