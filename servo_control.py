from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device, AngularServo
from time import sleep

Device.pin_factory = PiGPIOFactory()

# Define the servo with angle limits
servo = AngularServo(13, min_angle=00, max_angle=120)

def set_angle(angle):
    """ Move the servo to a specific angle (0-120°). """
    servo.angle = angle
    sleep(0.5)

try:
    while True:
        angle = float(input("Enter angle (0 - 120): "))
        if 0 <= angle <= 120:
            set_angle(angle)
        else:
            print("Please enter a valid angle between 0 and 120.")
except KeyboardInterrupt:
    print("Exiting...")
finally:
    servo.angle = None  # Stop sending signal
