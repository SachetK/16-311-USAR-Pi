from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device, AngularServo
from time import sleep
import socket

Device.pin_factory = PiGPIOFactory()

# Define the camera_servo with angle limits
camera_servo = AngularServo(13, min_angle=0, max_angle=120)
claw_servo = AngularServo(12, min_angle=0, max_angle=120)
# lever_servo = AngularServo(8, min_angle=0, max_angle=120)

camera_servo.angle = 60
claw_servo.angle = 120
# lever_servo.angle = 0

def camera_top():
    camera_servo.angle = 0
    sleep(0.5)

def camera_middle():
    camera_servo.angle = 60
    sleep(0.5)

def camera_bottom():
    camera_servo.angle = 120
    sleep(0.5)

# Map commands to actions
COMMANDS = {
    "CAMERA_TOP": camera_top,
    "CAMERA_MIDDLE": camera_middle,
    "CAMERA_BOTTOM": camera_bottom,
}

# Set up socket server
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5001        # Port for receiving commands

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Robot (camera_servo) server listening on {HOST}:{PORT}")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    try:
        while True:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break  # Client disconnected
            print(f"Received: {data}")
            
            if data in COMMANDS:
                COMMANDS[data]()  # Execute the corresponding function
            else:
                print(f"Unknown command: {data}")
    except Exception as e:
        print("Client disconnected")
        print(f"An error occured: {e}")

    client_socket.close()
