import socket
from motorgo import Plink

# Initialize Plink
plink = Plink()

# Configure motor channels
left_front_drive_wheel = plink.channel1
left_rear_drive_wheel = plink.channel2
right_front_drive_wheel = plink.channel3
right_rear_drive_wheel = plink.channel4

# Set motor voltage limits
left_front_drive_wheel.motor_voltage_limit = 6.0
right_front_drive_wheel.motor_voltage_limit = 6.0
left_rear_drive_wheel.motor_voltage_limit = 6.0
right_rear_drive_wheel.motor_voltage_limit = 6.0

# Connect to the MotorGo board
plink.connect()

# Define movement functions
def move_forward():
    left_front_drive_wheel.power_command = 1.0
    left_rear_drive_wheel.power_command = 1.0
    right_front_drive_wheel.power_command = 1.0
    right_rear_drive_wheel.power_command = 1.0

def move_backward():
    left_front_drive_wheel.power_command = -1.0
    left_rear_drive_wheel.power_command = -1.0
    right_front_drive_wheel.power_command = -1.0
    right_rear_drive_wheel.power_command = -1.0

def turn_left():
    left_front_drive_wheel.power_command = -1.0
    left_rear_drive_wheel.power_command = -1.0
    right_front_drive_wheel.power_command = 1.0
    right_rear_drive_wheel.power_command = 1.0

def turn_right():
    left_front_drive_wheel.power_command = 1.0
    left_rear_drive_wheel.power_command = 1.0
    right_front_drive_wheel.power_command = -1.0
    right_rear_drive_wheel.power_command = -1.0

def stop_robot():
    left_front_drive_wheel.power_command = 0
    left_rear_drive_wheel.power_command = 0
    right_front_drive_wheel.power_command = 0
    right_rear_drive_wheel.power_command = 0

# Map commands to actions
COMMANDS = {
    "FORWARD": move_forward,
    "BACKWARD": move_backward,
    "LEFT": turn_left,
    "RIGHT": turn_right,
    "STOP": stop_robot,
}

# Set up socket server
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5000        # Port for receiving commands

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Robot server listening on {HOST}:{PORT}")

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
    except:
        print("Client disconnected")

    client_socket.close()
    break
