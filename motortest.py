import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit = MotorKit()

kit.motor2.throttle = 1.0
time.sleep(1)
kit.motor2.throttle = 0
