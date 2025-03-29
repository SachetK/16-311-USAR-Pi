import RPi.GPIO as GPIO
import time

# Set up GPIO
SERVO_PIN = 18  # Change to the GPIO pin you are using
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set up PWM
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz frequency
pwm.start(0)

def set_angle(angle):
    duty_cycle = (angle / 18) + 2  # Convert angle to duty cycle
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        angle = float(input("Enter angle (0-180): "))
        if 0 <= angle <= 180:
            set_angle(angle)
        else:
            print("Please enter a valid angle between 0 and 180.")
except KeyboardInterrupt:
    print("Exiting...")
finally:
    pwm.stop()
    GPIO.cleanup()
