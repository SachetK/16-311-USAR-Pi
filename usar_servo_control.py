from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device, AngularServo
from time import sleep
import socket

Device.pin_factory = PiGPIOFactory()

# Define the servo with angle limits
servo = AngularServo(13, min_angle=00, max_angle=120)
servo_angle = 60
servo.angle = servo_angle

def set_angle(angle):
    """ Move the servo to a specific angle (0-120°). """
    servo.angle = angle
    sleep(0.5)

def increase_angle():
    global servo_angle
    if servo_angle > 0:
        servo_angle -= 10
    servo.angle = servo_angle

def decrease_angle():
    global servo_angle
    if servo_angle < 120:
        servo_angle += 10
    servo.angle = servo_angle

# Map commands to actions
COMMANDS = {
    "CAMERA_UP": increase_angle,
    "CAMERA_DOWN": decrease_angle,
}

# Set up socket server
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5001        # Port for receiving commands

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Robot (servo) server listening on {HOST}:{PORT}")

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
