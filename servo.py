import argparse
import time

import RPi.GPIO as GPIO


def move_servo(axis, degrees):
    servo_pin_x = 13
    servo_pin_y = 15

    servo_pin = servo_pin_x if axis == "x" else servo_pin_y

    degrees = float(degrees)
    # Map 0 - 180 to 0 to 10
    cycle = degrees / 18
    # Correct between 2.5 and 12.5
    cycle = cycle + 2.5

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servo_pin, GPIO.OUT)
    GPIO.setwarnings(False)
    p = GPIO.PWM(servo_pin, 50)

    p.start(cycle)
    time.sleep(0.25)
    p.stop()
    GPIO.cleanup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move a servo.")
    parser.add_argument(
        "--axis", dest="axis", required=True, choices=("x", "y"), help="axis to rotate"
    )
    parser.add_argument(
        "--degrees",
        dest="degrees",
        required=True,
        type=int,
        help="degress to rotate (0 - 180",
    )

    args = parser.parse_args()
    move_servo(args.axis, args.degrees)
